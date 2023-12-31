import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

def get_args(args):
    if len(args) != 2:
        return
    return args[1]

def get_spotify_id(str):
    spotify_id = ""
    if str[:34]=="https://open.spotify.com/playlist/":
        spotify_id = str[34:56]
    else:
        spotify_id = str[:22]
    if len(spotify_id) == 22:
        return spotify_id
    return 

def get_spotify_authorization(client_id, client_secret, redirect_uri):
    scope = "user-library-read"
    util.prompt_for_user_token(scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    spotify_oauth = SpotifyOAuth(scope=scope, cache_path=None)
    authorization = spotipy.Spotify(auth_manager=spotify_oauth)
    return authorization

def obtain_spotify_playlist_info(spotify, playlist_url, limit):
    playlist = spotify.playlist(playlist_url)
    playlist_name = playlist["name"]
    retrieved_tracks = playlist["tracks"]
    all_tracks = retrieved_tracks["items"]
    
    if limit>100:
        while retrieved_tracks["next"]:
            retrieved_tracks = spotify.next(retrieved_tracks)
            all_tracks.extend(retrieved_tracks["items"])

    return playlist_name, all_tracks
    
def get_spotify_playlist_songs(all_tracks, limit):
    songs = [x["track"] for x in all_tracks]
    songs_dict = {}
    for x, y in enumerate(songs):
        if x==limit:
            break
        
        artists = ""
        for i, j in enumerate(y["artists"]):
            if (j["name"] == ""):
                break
            artists += (j["name"])
            if (len(y["artists"]) - i) != 0:
                artists += ", "

        if artists == "":
            songs_dict[x] = y["name"]
        else:
            songs_dict[x] = y["name"] + " by " + artists

    return songs_dict
