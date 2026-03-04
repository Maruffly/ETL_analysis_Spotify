from src.Extractor import LastFMclient
from src.Transformer import DataEnricher
import pandas as pd

# INIT
client = LastFMclient()
enricher = DataEnricher(client)

# EXTRACTION
top_200_raw_tracks = client.get_top_tracks_yearly(2023, limit=200)

# TRANSFORMATION
unique_artists = list(set(t['artist_name'] for t in top_200_raw_tracks))
artist_data = {}
for artist in unique_artists:
    # Utilise ta méthode get_artist_stats testée
    stats = client.get_artist_stats(artist)
    if stats:
        artist_data[artist] = stats

enriched_tracks = enricher.enrich_tracks(top_200_raw_tracks)

# PREPARE LOADING
df = pd.DataFrame(enriched_tracks)
print(df[['track_name', 'artist_name', 'genres', 'listeners']].head())
