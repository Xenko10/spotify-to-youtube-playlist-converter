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

def get_playlist_info(sp, playlist_id, limit):
    playlist = sp.playlist(playlist_id)
    tracks = playlist["tracks"]
    playlist_name = playlist["name"]
    all_tracks = tracks["items"]
    if limit>100:
        while tracks["next"]:
            tracks = sp.next(tracks)
            all_tracks.extend(tracks["items"])
    
    songs = [x["track"] for x in all_tracks]
    songs_dict = {}
    local_songs = []
    song_number = 0
    for x, y in enumerate(songs):
        if not y["is_local"]:
            artists = ""
            k=0
            for i in y["artists"]:
                artists += (i["name"])
                k+=1
                if (len(y["artists"]) - k) != 0:
                    artists += ", "
            songs_dict[song_number] = y["name"] + " by " + artists
            song_number+=1
        else:
            if y["artists"][0]["name"] != "":
                artists = ""
                k=0
                for i in y["artists"]:
                    artists += (i["name"])
                    k+=1
                    if (len(y["artists"]) - k) != 0:
                        artists += ", "
                songs_dict[song_number] = y["name"] + " by " + artists
                song_number += 1
            else:
                local_songs.append((y["name"],y["id"]))

        if x==limit-1:
            break
    print(f"Received Playlist Info for playlist {playlist_id}")
    return playlist_name, songs_dict
