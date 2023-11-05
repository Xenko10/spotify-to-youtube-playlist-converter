import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import os
from dotenv import load_dotenv
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

load_dotenv()
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
REDIRECT_URI=os.getenv("REDIRECT_URI")
YOUTUBE_API_KEY=os.getenv("YOUTUBE_API_KEY")

def get_spotify_id(str):
    if str[:34]=="https://open.spotify.com/playlist/":
        return str[34:56]
    else:
        return str[:22]

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
    print(f"Received Playlist Info for playlist {playlist_id}")
    return playlist_name, song_info, local_songs 

def connect_to_youtube_api():
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube

youtube = connect_to_youtube_api()

def get_youtube_song(song):
    request = youtube.search().list(
        q=song,part='snippet'
    )
    response = request.execute()

    return f"https://www.youtube.com/watch?v={response['items'][0]['id']['videoId']}"

def create_playlist(playlist_name):
    request = youtube.playlists().insert(part = "snippet", body={"snippet": {"title":playlist_name}}
    )
    response = request.execute()


