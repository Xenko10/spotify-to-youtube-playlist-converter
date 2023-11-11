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
    songs_ids = {}

    youtube = connect_to_youtube_api()

    for i in songs_dict:
        songs_ids[i] = get_youtube_song(songs_dict[i], youtube)

    youtube_playlist_id = create_playlist(playlist_name, youtube)

    for i in songs_ids:
        add_song_to_playlist(youtube_playlist_id, songs_ids[i], youtube)

    

if __name__ == "__main__":
    main()