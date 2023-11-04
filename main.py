import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
REDIRECT_URI=os.getenv("REDIRECT_URI")

scope = "user-library-read"

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def main():
    print(CLIENT_ID)
    print(CLIENT_SECRET)


if __name__ == "__main__":
    main()