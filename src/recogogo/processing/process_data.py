import gzip
import pandas as pd
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

def build_tables(playlists):
    playlist_rows, playlist_track_rows, track_rows = [], [], []
    for p in playlists:
        playlist_rows.append({"playlist_id": p["id"], "title": p["title"], "nb_tracks": p["nb_tracks"], "creation_date": p["creation_date"]})
        for position, t in enumerate(p["tracks"]["data"]):
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