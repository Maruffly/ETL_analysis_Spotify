import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class LastFMclient:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.base_url = "http://ws.audioscrobbler.com/2.0/"
        if not self.api_key:
            raise ValueError("No API key founded in .env")

    def _get(self, method, params):
        default_params = {
            'method' : method,
            'api_key' : self.api_key,
            'format': 'json'
        }
        params.update(default_params)

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"####| API ERROR |####")
            return None

    def get_artist_metadata(self, artist_name):
        artist_metadata = self._get('artist.getInfo',
                                    {'artist': artist_name})
        return artist_metadata

    def get_track_info(self, artist_name, track_name):
        data = self._get('track.getInfo', {'artist': artist_name,
                                           'track': track_name})
        if not data or 'track' not in data:
            return None

        track = data['track']
        playcount = track.get('playcount') or track.get('stats', {}).get('playcount')
        listeners = track.get('listeners') or track.get('stats', {}).get('listeners')

        track['stats'] = {
            'playcount': playcount,
            'listeners': listeners
        }
        return data

    def get_artist_stats(self, artist_name):
        data = self._get('artist.getInfo', {'artist': artist_name})
        if not data or 'artist' not in data:
            return None

        artist = data['artist']
        stats = artist.get('stats', {})

        # On convertit en int pour l'analyse de données future
        return {
            'name': artist['name'],
            'playcount': int(stats.get('playcount', 0)),
            'listeners': int(stats.get('listeners', 0)),
            'tags': [t['name'] for t in artist.get('tags', {}).get('tag', [])]
        }

    def get_track_stats(self, artist_name, track_name):
        data = self._get('track.getInfo', {'artist': artist_name, 'track': track_name})
        if not data or 'track' not in data:
            return None

        track = data['track']
        # Note : Sur les tracks, le playcount est parfois imbriqué différemment
        return {
            'name': track['name'],
            'artist': artist_name,
            'playcount': int(track.get('playcount', 0)),
            'listeners': int(track.get('listeners', 0)),
            'user_playcount': int(track.get('userplaycount', 0))  # Si authentifié
        }



