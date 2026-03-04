from src.Extractor import LastFMclient
from src.Transformer import DataEnricher
import pandas as pd

# INIT
client = LastFMclient()
enricher = DataEnricher(client)
year_to_test = 2023

# EXTRACTION
top_200_raw_tracks = client.get_top_tracks_yearly(year_to_test, limit=200)

# TRANSFORMATION
enriched_tracks = enricher.enrich_tracks(top_200_raw_tracks)

# PREPARE LOADING
df = pd.DataFrame(enriched_tracks)

# SORT
df = df.sort_values(by='artist_popularity', ascending=True)

# OUTPUT
filename = f"top_200_tracks_{year_to_test}.csv"
df.to_csv(filename, index=False, encoding='utf-8-sig')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
print(df.head(10))
