from recogogo.ingestion.deezer_api import get_deezer_playlist_info, download_deezer_track_preview
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

def collect_audio_from_playlist(playlist_id):
    playlist_info = get_deezer_playlist_info(playlist_id)
    if not playlist_info or "tracks" not in playlist_info:
        print(f"Failed to retrieve tracks for playlist ID {playlist_id}.")
        return None

    track_ids = [track["id"] for track in playlist_info["tracks"]["data"]]
    for track_id in track_ids:
        download_deezer_track_preview(track_id)

    return track_ids

def collect_audio_from_saved_playlists(limit=10):
    parquet_playlist_file_path = PROCESSED_DIR / "playlists.parquet"
    playlists_df = pd.read_parquet(parquet_playlist_file_path)
    playlist_ids = playlists_df["playlist_id"].tolist()
    for playlist_id in playlist_ids:
        collect_audio_from_playlist(playlist_id)

if __name__ == "__main__":
    collect_audio_from_saved_playlists()