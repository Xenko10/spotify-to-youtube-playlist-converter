import sys
from app import *


def main():
    if len(sys.argv) != 2:
        print("Incorrect number of arguments")
        sys.exit(1)

    spotify_id = get_spotify_id(sys.argv[1])

    playlist_id = f"spotify:playlist:{spotify_id}"
    
    sp = authorize()

    playlist_name, song_info, local_songs = get_playlist_info(sp, playlist_id)
    
    for i in song_info:
        print(song_info[i])
    
    if len(local_songs) != 0:
        print(local_songs)

    # get url of first song from Spotify playlist
    result = get_youtube_song(song_info[0])

    create_playlist(playlist_name)

    

if __name__ == "__main__":
    main()