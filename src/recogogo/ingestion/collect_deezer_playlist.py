from recogogo.ingestion.collect_data import collect_playlist_data
import recogogo.ingestion.deezer_api as deezer_api
from collections import deque

def collect_playlists_from_user(user_id):
    user_playlists_info = deezer_api.get_playlist_from_user_info(user_id)
    if not user_playlists_info or "data" not in user_playlists_info:
        print(f"Failed to retrieve playlists for user ID {user_id}.")
        return None

    playlist_ids = [playlist["id"] for playlist in user_playlists_info["data"]]
    for playlist_id in playlist_ids:
        collect_playlist_data(playlist_id)

    return playlist_ids

def collect_playlists_from_search(playlist_name):
    search_results = deezer_api.get_playlist_from_search_info(playlist_name)
    if not search_results or "data" not in search_results:
        print(f"Failed to retrieve search results for playlist name '{playlist_name}'.")
        return None

    playlist_ids = [playlist["id"] for playlist in search_results["data"]]
    for playlist_id in playlist_ids:
        collect_playlist_data(playlist_id)

    return playlist_ids

def deep_collect_playlists_from_users(user_ids, limit=100):
    viewed_user_ids = set(user_ids)
    count = 0
    queue = deque(user_ids)
    
    while len(queue) > 0 and count < limit:
        count += 1
        user_id = queue.popleft()
        collect_playlists_from_user(user_id)
        followers_info = deezer_api.get_deezer_user_followers_info(user_id)
        if not followers_info or "data" not in followers_info:
            continue
        for follower in followers_info.get("data", []):
            follower_id = follower["id"]
            if follower_id not in viewed_user_ids:
                queue.append(follower_id)
                viewed_user_ids.add(follower_id)
    return count

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
    deep_collect_playlists_from_users([2960047984], limit=10000)


    #compteur = 0
    #nb_appel = 0
    #for i in range(0, 1000):
     #   nb_appel += 1
     #   result = collect_playlist_data(i)
      #  if result:
      #      compteur += 1
     #   if nb_appel % 50 == 0:
      #      time.sleep(5)  
