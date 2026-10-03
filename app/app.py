from recogogo.ingestion import deezer_api
from recogogo.ingestion.collect_data import collect_playlist_data

def main() : 
    album_id = "302127"  
    album_info = deezer_api.get_deezer_album_info(album_id)
    if album_info:
        print(f"Album Title: {album_info['title']}")
        print(f"Artist: {album_info['artist']['name']}")
        print(f"Release Date: {album_info['release_date']}")
        collect_playlist_data(album_id)
    else:
        print("Failed to retrieve album information.")
    

if __name__ == "__main__":
    main()