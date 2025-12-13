"""
main.py
File: Main Application for Music Recommendation System
Author: [Your Name]
Student ID: [Your ID]
Course: [Course Name]
"""

import sys
import os

def main():
    print("=" * 70)
    print("MUSIC RECOMMENDATION SYSTEM - ASSIGNMENT")
    print("=" * 70)
    
    try:
        # Add current directory to path (not modules folder)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        # Import modules - UPDATED: Use correct class names
        from load_dataset_module import DataLoader
        from similarity_module import SimilarityCalculator
        from user_interface_module import MusicAppGUI  # Changed from RecommendationGUI
        
        print("\n1. Loading dataset...")
        
        # Check for data file
        data_file = None
        possible_paths = ['data.csv', 'data/data.csv']
        
        for path in possible_paths:
            if os.path.exists(path):
                data_file = path
                print(f"Found data file: {path}")
                break
        
        if not data_file:
            print("No data file found. Creating sample data...")
            data_file = create_sample_data()
            if not data_file:
                print("Failed to create sample data. Exiting.")
                return
        
        # Load data
        loader = DataLoader(data_file)
        data = loader.read_data()  # Changed from load_data() to read_data()
        
        if not data:
            print("Failed to load data. Creating fresh sample...")
            data_file = create_sample_data()
            loader = DataLoader(data_file)
            data = loader.read_data()
            
            if not data:
                print("Still failed to load data. Exiting.")
                return
        
        print(f"✅ Loaded data for {len(loader.get_all_artists())} artists")
        
        # Show sample info
        artists = loader.get_all_artists()
        if artists:
            print(f"\n🎵 Sample artists in dataset:")
            for i, artist in enumerate(artists[:5], 1):
                tracks = loader.get_songs_by_artist(artist)  # Changed from get_tracks_by_artist()
                print(f"   {i}. {artist} ({len(tracks)} tracks)")
        
        # Create artist features dataframe as per assignment
        df = loader.get_artist_features_dataframe()
        if df is not None:
            print(f"\n📊 Created artist features dataframe: {df.shape[0]} artists × {df.shape[1]} features")
            print(f"📁 Saved to: artist_features.csv")
        
        # Create similarity calculator
        print("\n2. Initializing similarity calculator...")
        calculator = SimilarityCalculator(loader)  # Changed constructor parameter
        print("✅ Calculator ready")
        
        # Show available metrics (NO MANHATTAN as per instructions)
        print("   Available metrics for assignment:")
        print("   • Cosine Similarity")
        print("   • Euclidean Distance")
        print("   • Pearson Correlation")
        print("   (Manhattan excluded as per assignment requirements)")
        
        # Launch GUI
        print("\n3. Launching GUI...")
        print("=" * 70)
        print("ASSIGNMENT TASKS AVAILABLE:")
        print("1. Task 1: Find Top 5 Similar Artists (similarity > 0.8)")
        print("2. Task 2: Get Artist Recommendations (10 random from similar)")
        print("=" * 70 + "\n")
        
        app = MusicAppGUI(loader, calculator)  # Changed from RecommendationGUI
        app.start()  # Changed from run() to start()
        
        print("\n" + "=" * 70)
        print("Application closed.")
        print("=" * 70)
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("\nChecking for required files in current directory:")
        
        # Check which files exist in current directory
        required_files = ['load_dataset_module.py', 'similarity_module.py', 'user_interface_module.py']
        for file in required_files:
            if os.path.exists(file):
                print(f"   ✅ {file}")
            else:
                print(f"   ❌ {file} - NOT FOUND")
        
        print("\nNote: Files should be in the project root, not in a 'modules' folder.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

def create_sample_data():
    """Create sample dataset"""
    try:
        import pandas as pd
        import random
        
        print("Creating sample dataset...")
        
        # Create sample data with realistic artist names
        data = []
        artist_names = [
            "Dani", "Phyu", "Mofe", "Alex", "Taylor",
            "Jordan", "Casey", "Riley", "Morgan", "Quinn"
        ]
        
        # Create 50 tracks with various artists
        for i in range(50):
            # Randomly assign 1-3 artists per track
            num_artists = random.randint(1, 3)
            track_artists = random.sample(artist_names, num_artists)
            
            # Format artists as string
            if len(track_artists) == 1:
                artists_str = track_artists[0]
            else:
                artists_str = ", ".join(track_artists)
            
            data.append({
                'id': f'track_{i:03d}',
                'name': f'Song {i}',
                'artists': artists_str,
                'acousticness': round(random.random(), 3),
                'danceability': round(random.random(), 3),
                'energy': round(random.random(), 3),
                'liveness': round(random.random(), 3),
                'loudness': round(random.uniform(-60, 0), 3),
                'popularity': random.randint(0, 100),
                'speechiness': round(random.random(), 3),
                'tempo': round(random.uniform(60, 200), 3),
                'valence': round(random.random(), 3)
            })
        
        df = pd.DataFrame(data)
        output_file = 'data.csv'
        df.to_csv(output_file, index=False)
        
        print(f"✅ Created sample data with {len(df)} tracks")
        print(f"✅ Artists: {len(artist_names)} unique artists")
        print(f"✅ Saved to: {output_file}")
        
        return output_file
        
    except ImportError:
        print("❌ Pandas not installed. Please install: pip install pandas")
        return None
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return None

if __name__ == "__main__":
    main()