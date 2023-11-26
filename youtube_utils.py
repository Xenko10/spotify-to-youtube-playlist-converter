import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

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
