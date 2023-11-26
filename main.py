import sys
import os
from dotenv import load_dotenv
from spotify_utils import get_args, get_spotify_id, get_spotify_authorization, get_playlist_info
from youtube_utils import get_youtube_authorization, get_youtube_song, create_playlist, add_song_to_playlist 

load_dotenv()
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
REDIRECT_URI=os.getenv("REDIRECT_URI")


def main():
    args = sys.argv
    user_input = get_args(args)

    if not user_input:
        print("Invalid argument.")
        print("Usage: python main.py <spotify_playlist_id>")
        return

    spotify_playlist_id = get_spotify_id(user_input)

    if not spotify_playlist_id:
        print("User input is not a valid Spotify playlist URL or ID.")
        return
    
    playlist_url = f"spotify:playlist:{spotify_playlist_id}"
    spotify = get_spotify_authorization(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
   
    # Set proper limit ( limit = floor( ( quota tokens in Youtube API ) /150 ) ). There is 10000 quota tokens by defualt, so normally 66 is the limit for normal user.
    limit = 50 # range 1-10000

    if limit not in range (1, 10_000):
        print("Limit not in range 1-10000")
        return

    playlist_name, songs_dict = get_playlist_info(spotify, playlist_url, limit)

    print(songs_dict)

    youtube = get_youtube_authorization()

    songs_ids = {}

    for i in songs_dict:
        songs_ids[i] = get_youtube_song(songs_dict[i], youtube)

    youtube_playlist_id = create_playlist(playlist_name, youtube)

    for i in songs_ids:
        add_song_to_playlist(youtube_playlist_id, songs_ids[i], youtube)

    
if __name__ == "__main__":
    main()
