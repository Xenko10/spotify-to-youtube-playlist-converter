import sys
from app import *


def main():
    if len(sys.argv) != 2:
        print("Incorrect number of arguments")
        sys.exit(1)

    spotify_id = get_spotify_id(sys.argv[1])
    playlist_id = f"spotify:playlist:{spotify_id}"
    sp = authorize()
   
    # Set proper limit ( limit = floor( ( quora tokens in Youtube API ) /150 ) ). There is 10000 quora tokens by defualt, so normally 66 is the limit for normal user.
    limit = 50 # range 1-10000

    if limit not in range (1, 10000):
        print("Limit not in range 1-10000")
        return

    playlist_name, songs_dict, local_songs = get_playlist_info(sp, playlist_id, limit)
    songs_urls = {}

    youtube = connect_to_youtube_api()

    for i in songs_dict:
        songs_urls[i] = get_youtube_song(songs_dict[i], youtube)

    for i in songs_urls:
        print(songs_urls[i], youtube)

    create_playlist(playlist_name)

    

if __name__ == "__main__":
    main()