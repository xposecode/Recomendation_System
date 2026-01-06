"""
load_dataset_module.py
File: Data Loading and Management Module
Author: [Your Name]
Student ID: [Your ID]
Course: [Course Name]
"""

import pandas as pd
import os

class DataLoader:
    
    def __init__(self, file_name='data.csv'):
        self.data_file = file_name
        self.artist_to_tracks = {}
        self.all_songs = []
        self.all_artists = []
        self.data_ready = False
        self.artist_features_df = None
    
    def read_data(self):
        """Main function to load and process data from CSV"""
        try:
            print(f"Reading data from {self.data_file}")
            
            if not os.path.exists(self.data_file):
                print(f"File not found: {self.data_file}")
                return None
            
            try:
                data_frame = pd.read_csv(self.data_file)
            except Exception as read_error:
                print(f"Error reading CSV: {read_error}")
                return None
            
            if data_frame.empty:
                print("CSV file is empty")
                return None
            
            print(f"Data shape: {len(data_frame)} rows, {len(data_frame.columns)} columns")
            
            self.artist_to_tracks = {}
            self.all_songs = []
            self.all_artists = []
            
            row_counter = 0
            for _, current_row in data_frame.iterrows():
                try:
                    song_id = str(current_row.get('id', f'song_{row_counter}'))
                    song_name = str(current_row.get('name', f'Song {row_counter}'))
                    
                    # Create song dictionary - using original column names
                    song_info = {
                        'id': song_id,
                        'name': song_name,
                        'acousticness': float(current_row.get('acousticness', 0)),
                        'danceability': float(current_row.get('danceability', 0)),
                        'energy': float(current_row.get('energy', 0)),
                        'liveness': float(current_row.get('liveness', 0)),
                        'loudness': float(current_row.get('loudness', 0)),
                        'popularity': float(current_row.get('popularity', 0)),
                        'speechiness': float(current_row.get('speechiness', 0)),
                        'tempo': float(current_row.get('tempo', 0)),
                        'valence': float(current_row.get('valence', 0))
                    }
                    
                    self.all_songs.append(song_info)
                    
                    # Parse artists - exact format from instructions
                    artists_str = str(current_row.get('artists', ''))
                    artist_names = self._parse_artists(artists_str)
                    
                    # Add this song to each artist's list
                    for artist in artist_names:
                        if artist not in self.artist_to_tracks:
                            self.artist_to_tracks[artist] = []
                            self.all_artists.append(artist)
                        
                        self.artist_to_tracks[artist].append(song_info)
                        
                except Exception as row_error:
                    continue
                
                row_counter += 1
            
            self.data_ready = True
            print(f"Loaded {len(self.artist_to_tracks)} artists and {len(self.all_songs)} songs")
            
            # Create artist features dataframe as per assignment
            self.create_artist_features_dataframe()
            
            return self.artist_to_tracks
            
        except Exception as general_error:
            print(f"Error in data loading: {general_error}")
            return None
    
    def _parse_artists(self, artists_str):
        """Parse artist string exactly like in assignment example"""
        if pd.isna(artists_str) or not artists_str or artists_str == '':
            return ['Unknown']
        
        artists_str = str(artists_str).strip()
        
        # Handle comma-separated artists (like "Dani, Phyu")
        if ',' in artists_str:
            artists = [artist.strip() for artist in artists_str.split(',')]
            return [artist for artist in artists if artist]
        
        # Handle single artist
        return [artists_str]
    
    def create_artist_features_dataframe(self):
        """Create dataframe with average features for each artist"""
        if not self.artist_to_tracks:
            return None
        
        # Feature columns to average (based on assignment example)
        feature_columns = ['acousticness', 'danceability', 'energy', 'liveness', 
                          'loudness', 'popularity', 'speechiness', 'tempo', 'valence']
        
        data_rows = []
        
        for artist, tracks in self.artist_to_tracks.items():
            if not tracks:
                continue
            
            # Initialize sums for each feature
            feature_sums = {feature: 0 for feature in feature_columns}
            
            # Sum all features from all tracks this artist appears in
            for track in tracks:
                for feature in feature_columns:
                    feature_sums[feature] += track[feature]
            
            # Calculate averages
            feature_averages = {}
            for feature in feature_columns:
                feature_averages[feature] = feature_sums[feature] / len(tracks)
            
            # Create row for this artist
            row = {'Artist_name': artist}
            row.update(feature_averages)
            data_rows.append(row)
        
        if data_rows:
            # Create dataframe and rename columns like in assignment
            self.artist_features_df = pd.DataFrame(data_rows)
            
            # Rename columns to Feature1, Feature2, etc. for assignment
            feature_columns = [col for col in self.artist_features_df.columns if col != 'Artist_name']
            new_column_names = {'Artist_name': 'Artist_name'}
            
            for i, feature in enumerate(feature_columns, 1):
                new_column_names[feature] = f'Feature{i}'
            
            self.artist_features_df = self.artist_features_df.rename(columns=new_column_names)
            
            print(f"Created artist features dataframe with {len(self.artist_features_df)} artists")
            print(f"Features: {len(feature_columns)} features per artist")
            
            # Save to CSV as per assignment
            self.artist_features_df.to_csv('artist_features.csv', index=False)
            print("Saved artist features to artist_features.csv")
            
            # Display sample as shown in assignment
            print("\nSample of artist features dataframe (like assignment example):")
            print(self.artist_features_df.head(5).to_string())
        
        return self.artist_features_df
    
    def get_artist_features_dataframe(self):
        """Get the artist features dataframe"""
        if self.artist_features_df is None:
            self.create_artist_features_dataframe()
        return self.artist_features_df
    
    def get_artist_features_vector(self, artist_name):
        """Get feature vector for an artist (for similarity calculations)"""
        if self.artist_features_df is None:
            self.create_artist_features_dataframe()
        
        if self.artist_features_df is None:
            return None
        
        artist_row = self.artist_features_df[self.artist_features_df['Artist_name'] == artist_name]
        
        if artist_row.empty:
            return None
        
        # Get all feature values as list (excluding Artist_name column)
        feature_vector = []
        for col in self.artist_features_df.columns:
            if col != 'Artist_name':
                feature_vector.append(artist_row[col].values[0])
        
        return feature_vector
    
    def get_all_artists(self):
        """Returns list of all artists"""
        if not self.data_ready:
            self.read_data()
        return self.all_artists
    
    def get_all_songs(self):
        """Returns list of all songs"""
        if not self.data_ready:
            self.read_data()
        return self.all_songs
    
    def get_songs_by_artist(self, artist_name):
        """Get all songs by specific artist (including collaborations)"""
        if not self.data_ready:
            self.read_data()
        return self.artist_to_tracks.get(artist_name, [])
    
    def get_artist_data(self):
        """Main data getter"""
        if not self.data_ready:
            self.read_data()
        return self.artist_to_tracks
    
    def calculate_average_example(self):
        """Example calculation from assignment instructions"""
        print("\n" + "="*60)
        print("EXAMPLE CALCULATION FROM ASSIGNMENT:")
        print("="*60)
        
        # Simulate the example from assignment
        example_data = [
            {'Artist_name': 'Dani', 'Track_name': 'Song1', 'Feature1': 1, 'Feature2': 6},
            {'Artist_name': 'Dani', 'Track_name': 'Song2', 'Feature1': 2, 'Feature2': 6},
            {'Artist_name': 'Dani', 'Track_name': 'Song3', 'Feature1': 1, 'Feature2': 6},
            {'Artist_name': 'Phyu', 'Track_name': 'Song4', 'Feature1': 6, 'Feature2': 1},
            {'Artist_name': 'Dani, Phyu', 'Track_name': 'Song5', 'Feature1': 5, 'Feature2': 3},
            {'Artist_name': 'Dani, Phyu, Mofe', 'Track_name': 'Song6', 'Feature1': 4, 'Feature2': 4},
        ]
        
        print("\nOriginal data (from assignment):")
        for row in example_data:
            print(f"  {row['Artist_name']:20} | {row['Track_name']:10} | Feature1: {row['Feature1']} | Feature2: {row['Feature2']}")
        
        # Calculate averages like in assignment
        print("\nCalculating average for Dani:")
        print("  Songs with Dani: Song1, Song2, Song3, Song5, Song6")
        print("  Feature1: (1 + 2 + 1 + 5 + 4) / 5 = 13 / 5 = 2.6")
        print("  Feature2: (6 + 6 + 6 + 3 + 4) / 5 = 25 / 5 = 5.0")
        print("  Result: Dani = [2.6, 5.0]")
        
        print("\nCalculating average for Phyu:")
        print("  Songs with Phyu: Song4, Song5, Song6")
        print("  Feature1: (6 + 5 + 4) / 3 = 15 / 3 = 5.0")
        print("  Feature2: (1 + 3 + 4) / 3 = 8 / 3 ≈ 2.67")
        print("  Result: Phyu = [5.0, 2.67]")
        
        print("\nThis is how our program calculates artist features!")

def test_data_loader():
    """Quick test to verify the module works"""
    print("Testing DataLoader...")
    loader = DataLoader('data.csv')
    data = loader.read_data()
    
    if data:
        print("Test passed!")
        print(f"Number of artists: {len(loader.get_all_artists())}")
        print(f"Number of songs: {len(loader.get_all_songs())}")
        
        df = loader.get_artist_features_dataframe()
        if df is not None:
            print(f"\nArtist features dataframe shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            
            # Show how to use the dataframe
            if len(df) > 0:
                sample_artist = df.iloc[0]['Artist_name']
                print(f"\nSample artist '{sample_artist}' feature vector:")
                vector = loader.get_artist_features_vector(sample_artist)
                print(f"  Features: {vector}")
    else:
        print("Test failed - no data loaded")

if __name__ == "__main__":
    test_data_loader()