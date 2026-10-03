import requests

BASE_URL = "https://api.deezer.com"

def _get(path):
    url = f"{BASE_URL}/{path}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if "error" in data:
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

def get_deezer_playlist_in_chart_info():
    return _get("chart/0/playlists?limit=1000")

if __name__ == "__main__":
    playlist_in_chart_info = get_deezer_playlist_in_chart_info()
    print(playlist_in_chart_info)