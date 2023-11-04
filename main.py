import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
REDIRECT_URI=os.getenv("REDIRECT_URI")

def authorize():
    scope = "user-library-read"
    util.prompt_for_user_token(scope,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)
    spotify_oauth = SpotifyOAuth(scope=scope, cache_path=None)
    authorization = spotipy.Spotify(auth_manager=spotify_oauth)
    return authorization


def main():

    if len(sys.argv) != 2:
        print("Incorrect number of arguments")
        sys.exit(1)

    playlist_id = f"spotify:playlist:{sys.argv[1]}"
    
    sp = authorize()

    result = sp.playlist(playlist_id)
    print(f"${result}")
    print (result)
    



if __name__ == "__main__":
    main()