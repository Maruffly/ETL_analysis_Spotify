import sys
import os
from src.Extractor import LastFMclient
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_api():
    print("====| Checking API status |====")

    client = LastFMclient()
    data_artist = client.get_artist_metadata("Aphex Twin")
    data_track = client.get_track_info("Aphex Twin", "Syro")

    try:
        # test 1 : simple search
        if data_artist and 'artist'in data_artist:
            artist = data_artist['artist']
            stats = artist.get('stats', {})

            print(f"Artist : {artist['name']}")
            print(f"Playcount : {stats.get('playcount')}")
            print(f"Listeners : {stats.get('listeners')}")
        else:
            print("Artist missing / incorrect format")

        if data_track and 'track' in data_track:
            track = data_track['track']
            track_playcount = track.get('playcount')
            track_listeners = track.get('listeners')

            print(f"Track ID : {track['name']}")
            print(f"Track Playcount : {track_playcount}")
            print(f"Track Listeners : {track_listeners}")

        print("====| ACCESS OK |====")
        return True

    except Exception as e:
        print("####| FAILURE |####")
        print(f" ERROR : {e}")
        return False

if __name__ == "__main__":
    test_api()
