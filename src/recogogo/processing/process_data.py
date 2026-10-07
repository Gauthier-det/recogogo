import gzip
import pandas as pd
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

def check_playlist_validity(playlists):
    for p in playlists:
        if not all(key in p for key in ["id", "title", "nb_tracks", "creation_date"]):
            print(f"Invalid playlist data: {p}")
            return False
        if not all(key in p["tracks"] for key in ["data"]):
            print(f"Invalid playlist tracks data: {p}")
            return False
        for t in p["tracks"]["data"]:
            if not all(key in t for key in ["id", "title", "artist", "album"]):
                print(f"Invalid track data: {t}")
                return False
    return True

def check_track_validity(t):
    if not all(key in t for key in ["id", "title", "artist", "album"]):
        return False
    if not all(key in t["artist"] for key in ["id", "name"]):
        return False
    if not all(key in t["album"] for key in ["id", "title"]):
        return False
    return True

def build_tables(playlists):
    check = check_playlist_validity(playlists)
    if not check:
        raise ValueError("Invalid data")
    playlist_rows, playlist_track_rows, track_rows = [], [], []
    for p in playlists:
        nb_tracks_valid = len(p["tracks"]["data"])
        for t in p["tracks"]["data"]:
            if not check_track_validity(t):
                nb_tracks_valid -= 1
        if nb_tracks_valid < 15:
            continue
        playlist_rows.append({"playlist_id": p["id"], "title": p["title"], "nb_tracks": len(p["tracks"]["data"]), "creation_date": p["creation_date"]})
        for position, t in enumerate(p["tracks"]["data"]):
            if not check_track_validity(t):
                continue
            playlist_track_rows.append({"playlist_id": p["id"], "position": position, "track_id": t["id"]})
            track_rows.append({"track_id": t["id"], "title": t["title"], "artist_id": t["artist"]["id"], "artist_name": t["artist"]["name"], "album_id": t["album"]["id"], "album_title": t["album"]["title"]})
    tracks_df = pd.DataFrame(track_rows).drop_duplicates("track_id")
    playlists_df = pd.DataFrame(playlist_rows)
    playlist_tracks_df = pd.DataFrame(playlist_track_rows)
    return playlists_df, playlist_tracks_df, tracks_df

def load_raw_playlists():
    playlists = []
    for path in RAW_DIR.glob("playlist_*.json.gz"):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            playlists.append(json.load(f))
    return playlists

if __name__ == "__main__":
    playlists = load_raw_playlists()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    playlists_df, playlist_tracks_df, tracks_df = build_tables(playlists)
    playlists_df.to_parquet(PROCESSED_DIR / "playlists.parquet", index=False)
    playlist_tracks_df.to_parquet(PROCESSED_DIR / "playlist_tracks.parquet", index=False)
    tracks_df.to_parquet(PROCESSED_DIR / "tracks.parquet", index=False)
    print(f"{len(playlists)} playlists → {len(tracks_df)} titres uniques")