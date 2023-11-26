import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def get_spotify_id(str):
    if str[:34]=="https://open.spotify.com/playlist/":
        return str[34:56]
    else:
        return str[:22]

def authorize(client_id, client_secret, redirect_uri):
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

def connect_to_youtube_api():
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    api_service_name = "youtube"
    api_version = "v3"
    # make sure to download client_secret.json from google cloud console and put it in the same directory as this file
    client_secrets_file = "client_secret.json" # change your file to this name
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube

def get_youtube_song(song, youtube):
    request = youtube.search().list(
        q=song,part="snippet",type="video",maxResults=1
    )
    response = request.execute()

    return response["items"][0]["id"]["videoId"]

def create_playlist(playlist_name, youtube):
    request = youtube.playlists().insert(part = "snippet", body={"snippet": {"title":playlist_name}}
    )
    response = request.execute()

    print(f"Created playlist {playlist_name} with id {response['id']}")

    return response["id"]

def add_song_to_playlist(youtube_playlist_id, song_id, youtube):
    request = youtube.playlistItems().insert(part = "snippet", body={"snippet": {"playlistId":youtube_playlist_id, "resourceId": {"kind": "youtube#video", "videoId": song_id}}}
    )
    response = request.execute()

    print(f"Added song {song_id} to playlist {youtube_playlist_id}")

    return response["id"]
