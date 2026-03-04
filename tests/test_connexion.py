import spotipy
from src.ETL import get_spotify_client

def test_api():
    sp = get_spotify_client()
    print("====| Checking API status |====")

    try:
        # test 1 : simple search
        search_res = sp.search(q='MGMT', type='track', market='FR', limit=1)
        if not search_res['tracks']['items']:
            print("####| No Results! |#####")

        track = search_res['tracks']['items'][0]
        track_name = track['name']

        artist_id = track['artists'][0]['id']
        print(f"Search API OK : {track_name} by {artist_id} (MGMT)")


        # test 2 : get details
        ## Complete artist object needed
        artist = sp.artist(artist_id)

        name = artist.get('name')
        popularity = artist.get('popularity', {})
        genres = artist.get('genres', [])

        total_followers = artist.get('followers', {}).get('total', 0)


        print(f"Artist : {artist}")
        print(f"Genres : {genres}")
        print(f"Popularity : {popularity}")
        print(f"Followers : {total_followers}")
        print("====| ACCESS OK |====")
        return True

    except Exception as e:
        print("####| FAILURE |####")
        print(f" ERROR : {e}")
        return False

if __name__ == "__main__":
    test_api()
