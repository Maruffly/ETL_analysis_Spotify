import sys
import os
from src.Extractor import LastFMclient
from src.Transformer import DataEnricher

def test_api():
    print("====| Checking API status |====")

    client = LastFMclient()
    data_artist = client.get_artist_stats("Aphex Twin")

    try:
        # test 1 : simple search
        if data_artist and 'name'in data_artist:
            print(f"Artist : {data_artist['name']}")
            print(f"Playcount : {data_artist['playcount']}")
            print(f"Listeners : {data_artist['listeners']}")
        else:
            print("Artist missing / incorrect format")

        print("====| ACCESS OK |====")
        return True

    except Exception as e:
        print("####| FAILURE |####")
        print(f" ERROR : {e}")
        return False


def test_yearly_tracks():
    print("\n====| Testing Yearly |====")

    client = LastFMclient()
    target_limit = 20
    year_to_test = 2023

    tracks = client.get_top_tracks_yearly(year_to_test, limit=target_limit)
    if not tracks:
        print(f"####| FAILURE: No tracks found in {year_to_test} |####")
        return False
    print(f"Number of extracted tracks : {len(tracks)}")
    if len(tracks) != target_limit:
        print(f"Target was {target_limit}, got {len(tracks)}")

    #check strucutre of first element
    first_track = tracks[0]
    required_keys = ['track_name', 'artist_name', 'track_popularity', 'year']
    is_valid = all(key in first_track for key in required_keys)

    if is_valid:
        print(f"Sample Track: {first_track['track_name']} by {first_track['artist_name']}")
        print(f"Popularity: {first_track['track_popularity']}")
        print(f"Year: {first_track['year']}")

        # check type of popularity
        if isinstance(first_track['track_popularity'], int):
            print("====| OK Popularity is an int |====")
        else:
            print("####| FAILURE: Popularity is NOT an INT |####")
            is_valid = False
    else:
        print("####| FAILURE : Keys are missing in the track dictionary |####")

    if is_valid:
        print("====| YEARLY TRACKS OK |====")
    return is_valid


def test_enrichment():
    print("\n====| Testing Enrichment Class |====")
    client = LastFMclient()
    enricher = DataEnricher(client)

    # simulate duplacated artists
    test_tracks = [
        {'track_name': 'Song A', 'artist_name': 'MGMT', 'year': 2023},
        {'track_name': 'Song B', 'artist_name': 'MGMT', 'year': 2023}
    ]

    # "Enrich artist" log should display once
    results = enricher.enrich_tracks(test_tracks)
    if results and 'listeners' in results[0]:
        print("====| ENRICHMENT OK |====")
        return True
    return False


def test_track_details():
    print("\n====| Testing Track Details |====")

    client = LastFMclient()

    artist_test = "Aphex Twin"
    track_test = "QKThr"

    print(f"Fetching details for: {track_test} by {artist_test}...")
    details = client.get_track_details(artist_test, track_test)

    if not details:
        print("####| FAILURE: No data returned |####")
        return False
    required_keys = ['album_name', 'duration_ms', 'track_listeners']
    missing_keys = [k for k in required_keys if k not in details]

    if missing_keys:
        print(f"####| FAILURE: keys missing  {missing_keys} |####")
        return False

    print(f"Track Details OK:")
    print(f"Album    : {details.get('album_name')}")
    print(f"Duration : {details.get('duration_ms')} ms")
    print(f"Listeners: {details.get('track_listeners')} (track specific)")

    if isinstance(details['duration_ms'], int) and details['duration_ms'] >= 0:
        print("DUration is valid integer.")
    else:
        print("####| WARNING: Duration format |####")
    return True

if __name__ == "__main__":
    api_ok = test_api()
    if api_ok:
        test_yearly_tracks()
        test_enrichment()
