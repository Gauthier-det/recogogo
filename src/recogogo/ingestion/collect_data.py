import gzip
import json
from pathlib import Path

import recogogo.ingestion.deezer_api as deezer_api

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

COLLECTION_TYPE = {
    "album": deezer_api.get_deezer_album_info,
    "artist": deezer_api.get_deezer_artist_info,
    "track": deezer_api.get_deezer_track_info,
    "playlist": deezer_api.get_deezer_playlist_info
}

def collect_data(collection_type, collection_id):
    if collection_type not in COLLECTION_TYPE:
        raise ValueError(f"Invalid collection type: {collection_type}. Expected one of {list(COLLECTION_TYPE)}.")

    path = RAW_DIR / f"{collection_type}_{collection_id}.json.gz"
    if path.exists():
        return path

    collection_info = COLLECTION_TYPE[collection_type](collection_id)
    if not collection_info:
        print(f"Failed to retrieve {collection_type} information for ID {collection_id}.")
        return None

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(collection_info, f)
    print(f"{collection_type.capitalize()} data for ID {collection_id} saved to {path.relative_to(PROJECT_ROOT)}.")
    return path

def collect_playlist_data(playlist_id):
    return collect_data("playlist", playlist_id)

def collect_album_data(album_id):
    return collect_data("album", album_id)

def collect_artist_data(artist_id):
    return collect_data("artist", artist_id)

def collect_track_data(track_id):
    return collect_data("track", track_id)

def collect_chart_playlists():
    chart_playlists_info = deezer_api.get_deezer_playlist_in_chart_info()
    if not chart_playlists_info:
        print("Failed to retrieve chart playlists information.")
        return None

    playlist_ids = [playlist["id"] for playlist in chart_playlists_info["data"]]
    for playlist_id in playlist_ids:
        collect_playlist_data(playlist_id)
    return playlist_ids

if __name__ == "__main__":
    collect_chart_playlists()
