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

def get_playlist_info(sp, playlist_id):
    playlist = sp.playlist(playlist_id)
    tracks = playlist["tracks"]
    playlist_name = playlist["name"]
    all_tracks = tracks["items"]
    while tracks["next"]:
        tracks = sp.next(tracks)
        all_tracks.extend(tracks["items"])
    
    songs = [x["track"] for x in all_tracks]
    song_info = {}
    local_songs = []

    for x,y in enumerate(songs):
        if not y["is_local"]:
            artists = ""
            k=0
            for i in y["artists"]:
                artists += (i["name"])
                k+=1
                if (len(y["artists"]) - k) != 0:
                    artists += ", "
            song_info[x] = y["name"] + " by " + artists
        else:
            local_songs.append((y["name"],y["id"]))
                
    print(f'Revieved Playlist Info for playlist {playlist_id}')
    return playlist_name, song_info, local_songs 

def main():

    if len(sys.argv) != 2:
        print("Incorrect number of arguments")
        sys.exit(1)

    sys_arg = sys.argv[1]

    spotify_id = ""

    if sys_arg[:34]=="https://open.spotify.com/playlist/":
        spotify_id = sys_arg[34:56]
    else:
        spotify_id = sys.argv[1]


    playlist_id = f"spotify:playlist:{spotify_id}"
    
    sp = authorize()

    playlist_name, song_info, local_songs = get_playlist_info(sp, playlist_id)
    
    for i in song_info:
        print(song_info[i])
    
    if len(local_songs) != 0:
        print(local_songs)
    



if __name__ == "__main__":
    main()