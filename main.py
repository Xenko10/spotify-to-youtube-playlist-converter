import sys
import os
from dotenv import load_dotenv
from app import get_spotify_id, authorize, get_playlist_info, get_youtube_song, connect_to_youtube_api, create_playlist, add_song_to_playlist

load_dotenv()
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
REDIRECT_URI=os.getenv("REDIRECT_URI")
YOUTUBE_API_KEY=os.getenv("YOUTUBE_API_KEY")

def get_args():
    if len(sys.argv) != 2:
        print("Incorrect number of arguments")
        sys.exit(1)
    return get_spotify_id(sys.argv[1])

def main():
    spotify_id = get_args()

    playlist_id = f"spotify:playlist:{spotify_id}"
    sp = authorize(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
   
    # Set proper limit ( limit = floor( ( quota tokens in Youtube API ) /150 ) ). There is 10000 quota tokens by defualt, so normally 66 is the limit for normal user.
    limit = 50 # range 1-10000

    if limit not in range (1, 10_000):
        print("Limit not in range 1-10000")
        return

    playlist_name, songs_dict = get_playlist_info(sp, playlist_id, limit)
    songs_ids = {}

    print(songs_dict)

    youtube = connect_to_youtube_api()

    for i in songs_dict:
        songs_ids[i] = get_youtube_song(songs_dict[i], youtube)

    youtube_playlist_id = create_playlist(playlist_name, youtube)

    for i in songs_ids:
        add_song_to_playlist(youtube_playlist_id, songs_ids[i], youtube)

    
if __name__ == "__main__":
    main()