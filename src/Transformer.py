import time

class DataEnricher:
    def __init__(self, client):
        self.client = client
        self.artist_cache = {}

    def enrich_tracks(self, tracks):
        # tack a list of tracks and add artists info.
        # use a local cache to avoid rerequesting a same artist
        enriched_data = []
        for track in tracks:
            artist_name = track['artist_name']
            # cache handling
            if artist_name not in self.artist_cache:
                print(f"Enrich artist : {artist_name}")
                artist_info = self.client.get_artist_stats(artist_name)
                self.artist_cache[artist_name] = artist_info if artist_info else {}
                time.sleep(0.2)
            # dict fusion
            all_infos = {**track, **self.artist_cache[artist_name]}
            enriched_data.append(all_infos)
        return enriched_data

