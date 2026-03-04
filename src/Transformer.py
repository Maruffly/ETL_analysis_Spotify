class DataEnricher:
    def __init__(self, client):
        self.client = client
        
    def enrich_tracks(self, tracks):
        # tack a list of tracks and add artists info.
        # use a local cache to avoid rerequesting a same artist
        enriched_data = []
        artist_cache = {}
        for track in tracks:
            artist_name = track['artist_name']
            # cache handling
            if artist_name not in artist_cache:
                print(f"Enrich artist : {artist_name}")
                artist_info = self.client.get_artist_details(artist_name)
                artist_cache[artist_name] = artist_info if artist_info else {}
            # dict fusion
            full_info = {**track, **artist_cache[artist_name]}
            enriched_data.append(full_info)
        return enriched_data

