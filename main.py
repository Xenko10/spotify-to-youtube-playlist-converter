import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def authorize():
    scope = "user-library-read"
    spotify_oauth = SpotifyOAuth(scope=scope, cache_path=None)
    authorization = spotipy.Spotify(auth_manager=spotify_oauth)
    return authorization


def main():

    if len(sys.argv) != 2:
        print("Incorrect number of arguments")
        sys.exit(1)

    playlist_id = f"spotify:artist:{sys.argv[1]}"
    
    sp = authorize()

    results = sp.artist_albums(playlist_id, album_type='album')
    albums = results['items']
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])
    



if __name__ == "__main__":
    main()