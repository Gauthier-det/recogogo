import requests
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "files"

BASE_URL = "https://api.deezer.com"
last_query = 0
interval = 0.1


def _get(path):
    global last_query
    now = time.monotonic()
    if now - last_query < interval:
        time.sleep(interval - (now - last_query))
    url = f"{BASE_URL}/{path}"
    try:
        response = requests.get(url, timeout=10)
        last_query = time.monotonic()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        last_query = time.monotonic()
        return None
    
    if response.status_code != 200:
        return None
    data = response.json()
    if "error" in data:
        if data["error"]["code"] == 4:
            time.sleep(60)
        return None
    return data

def get_deezer_album_info(album_id):
    return _get(f"album/{album_id}")

def get_deezer_artist_info(artist_id):
    return _get(f"artist/{artist_id}")

def get_deezer_track_info(track_id):
    return _get(f"track/{track_id}")

def get_deezer_playlist_info(playlist_id):
    return _get(f"playlist/{playlist_id}")

def get_playlist_from_search_info(playlist_name):
    return _get(f"search/playlist?q={playlist_name}")

def get_playlist_from_user_info(user_id):
    return _get(f"user/{user_id}/playlists")

def get_deezer_playlist_in_chart_info():
    return _get("chart/0/playlists?limit=1000")

def get_deezer_user_info(user_id):
    return _get(f"user/{user_id}")

def get_deezer_user_followers_info(user_id):
    return _get(f"user/{user_id}/followers")

def download_deezer_track_preview(track_id):
    track_info = get_deezer_track_info(track_id)
    if not track_info or not track_info.get("preview"):
        print(f"Failed to retrieve track info for track ID '{track_id}'.")
        return False
    preview_url = track_info["preview"]
    try:
        response = requests.get(preview_url, timeout=10)
        output_path = RAW_DIR / f"track_{track_id}.mp3"
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            return True
        else:
            print(f"Failed to download preview for track ID '{track_id}'. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request failed while downloading preview for track ID '{track_id}': {e}")
        return False


if __name__ == "__main__":
    download_deezer_track_preview(2679793432)