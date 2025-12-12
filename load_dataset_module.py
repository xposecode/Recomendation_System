"""
load_dataset_module.py - Complete working version
"""

import pandas as pd
import os

class DataLoader:
    def __init__(self, file_path='data.csv'):
        self.file_path = file_path
        self.artist_music = {}
        self.tracks = []
        self.artists = []
        self.loaded = False
    
    def load_data(self):
        """Load and parse the dataset"""
        try:
            print(f"Loading data from {self.file_path}")
            
            if not os.path.exists(self.file_path):
                print(f"File not found: {self.file_path}")
                return None
            
            # Try to read the CSV
            try:
                df = pd.read_csv(self.file_path)
            except Exception as e:
                print(f"Error reading CSV: {e}")
                return None
            
            if df.empty:
                print("CSV file is empty")
                return None
            
            print(f"Found {len(df)} rows, {len(df.columns)} columns")
            
            # Check for required columns
            required = ['acousticness', 'artists', 'danceability', 'energy', 'id',
                       'liveness', 'loudness', 'name', 'popularity', 'speechiness',
                       'tempo', 'valence']
            
            # Create artist_music dictionary
            self.artist_music = {}
            self.tracks = []
            self.artists = []
            
            for index, row in df.iterrows():
                try:
                    # Get track info
                    track_id = str(row.get('id', f'track_{index}'))
                    track_name = str(row.get('name', f'Track {index}'))
                    
                    # Create track dictionary
                    track = {
                        'id': track_id,
                        'name': track_name,
                        'acousticness': float(row.get('acousticness', 0)),
                        'danceability': float(row.get('danceability', 0)),
                        'energy': float(row.get('energy', 0)),
                        'liveness': float(row.get('liveness', 0)),
                        'loudness': float(row.get('loudness', 0)),
                        'popularity': float(row.get('popularity', 0)),
                        'speechiness': float(row.get('speechiness', 0)),
                        'tempo': float(row.get('tempo', 0)),
                        'valence': float(row.get('valence', 0))
                    }
                    
                    self.tracks.append(track)
                    
                    # Parse artists
                    artists_str = str(row.get('artists', 'Unknown'))
                    artists_list = self._parse_artists(artists_str)
                    
                    # Add to artist_music dictionary
                    for artist in artists_list:
                        if artist not in self.artist_music:
                            self.artist_music[artist] = []
                            self.artists.append(artist)
                        
                        self.artist_music[artist].append(track)
                        
                except Exception as e:
                    print(f"Warning: Error processing row {index}: {e}")
                    continue
            
            self.loaded = True
            print(f"Successfully loaded {len(self.artist_music)} artists and {len(self.tracks)} tracks")
            return self.artist_music
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def _parse_artists(self, artists_str):
        """Parse artists string into list"""
        if pd.isna(artists_str) or not artists_str:
            return ['Unknown Artist']
        
        artists_str = str(artists_str).strip()
        
        # Try to parse as list
        if artists_str.startswith('[') and artists_str.endswith(']'):
            try:
                import ast
                artists_list = ast.literal_eval(artists_str)
                if isinstance(artists_list, list):
                    return [str(a).strip() for a in artists_list]
            except:
                pass
        
        # Try comma or semicolon separated
        if ';' in artists_str:
            return [a.strip() for a in artists_str.split(';')]
        elif ',' in artists_str:
            return [a.strip() for a in artists_str.split(',')]
        
        # Single artist
        return [artists_str]
    
    def get_artist_music(self):
        """Get the artist-music dictionary"""
        if not self.loaded:
            self.load_data()
        return self.artist_music
    
    def get_all_artists(self):
        """Get list of all artists"""
        if not self.loaded:
            self.load_data()
        return self.artists
    
    def get_all_tracks(self):
        """Get list of all tracks"""
        if not self.loaded:
            self.load_data()
        return self.tracks
    
    def get_tracks_by_artist(self, artist_name):
        """Get tracks by artist"""
        if not self.loaded:
            self.load_data()
        return self.artist_music.get(artist_name, [])
    
    def get_track_by_id(self, track_id):
        """Get track by ID"""
        if not self.loaded:
            self.load_data()
        
        for track in self.tracks:
            if track['id'] == track_id:
                return track
        return None
    
    def get_tracks_by_name(self, track_name):
        """Get tracks by name"""
        if not self.loaded:
            self.load_data()
        
        results = []
        track_name_lower = track_name.lower()
        
        for track in self.tracks:
            if track['name'].lower() == track_name_lower:
                # Find artist for this track
                for artist, tracks in self.artist_music.items():
                    if track in tracks:
                        results.append((artist, track))
                        break
        
        return results
    
    def search_artists(self, query):
        """Search for artists"""
        if not self.loaded:
            self.load_data()
        
        query = query.lower()
        return [artist for artist in self.artists if query in artist.lower()]