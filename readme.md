## What is the Spotify to Youtube playlist converter?

Spotify to Youtube playlist converter is an app that helps you create Youtube playlist from your Spotify playlist.

## How to start this app?

1. Common setup. Clone the repository, add API keys and install the dependencies.

- git clone https://github.com/Xenko10/spotify-to-youtube-playlist-converter.git
- cd spotify-to-youtube-playlist-converter
- create .env file with those variables:

SPOTIPY_CLIENT_ID="< spotify client id >"  
SPOTIPY_CLIENT_SECRET="< spotify client secret >"  
SPOTIPY_REDIRECT_URI="< spotify redirect URI >"

- download credentials file from google cloud console ( https://console.cloud.google.com/apis/credentials ), put it in the same directory as this file and change name of that file to client_secret.json
- start setup.bat

2. Usage

- python main.py < spotify url >
