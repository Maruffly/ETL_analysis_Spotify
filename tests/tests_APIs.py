import sys
import os
from src.Extractor import LastFMclient
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    print("\n====| Testing Enrichment Logic |====")
    client = LastFMclient()
    # Check with a famous artist
    test_artist = "Daft Punk"

    print(f"Fetching details for: {test_artist}...")
    details = client.get_artist_stats(test_artist)
    print(details)
    if not details:
        print(f"####| FAILURE: Could not fetch details for {test_artist} |####")
        return False
    mock_track = {
        'track_name': 'One More Time',
        'artist_name': test_artist,
        'track_popularity': 1,
        'year': 2000
    }
    # FFusion
    enriched_track = {**mock_track, **details}
    # check requiered fields
    required_fields = ['playcount', 'listeners', 'genres']
    is_valid = all(field in enriched_track for field in required_fields)

    if is_valid:
        print(f"Success: Track '{enriched_track['track_name']}' enriched!")
        print(f"Listeners : {enriched_track['listeners']}")
        print(f"Genres : {', '.join(enriched_track['genres'][:3])}...")
        print(f"Artist Playcount: {enriched_track['playcount']}")
    else:
        missing = [f for f in required_fields if f not in enriched_track]
        print(f"####| FAILURE: Missing fields {missing} |####")
    return is_valid

if __name__ == "__main__":
    api_ok = test_api()
    if api_ok:
        test_yearly_tracks()
        test_enrichment()
