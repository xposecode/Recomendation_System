"""
main.py - Complete working version
"""

import sys
import os

def main():
    print("=" * 60)
    print("MUSIC RECOMMENDATION ENGINE")
    print("=" * 60)
    
    try:
        # Add modules to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        modules_dir = os.path.join(current_dir, 'modules')
        
        if modules_dir not in sys.path:
            sys.path.insert(0, modules_dir)
        
        # Import modules
        from load_dataset_module import DataLoader
        from similarity_module import SimilarityCalculator
        from user_interface_module import RecommendationGUI
        
        print("\n1. Loading dataset...")
        
        # Check data file
        data_file = 'data.csv'
        if not os.path.exists(data_file):
            print(f"Data file not found: {data_file}")
            create_sample_data()
        
        # Load data
        loader = DataLoader(data_file)
        data = loader.load_data()
        
        if not data:
            print("Failed to load data. Creating fresh sample...")
            create_sample_data()
            loader = DataLoader(data_file)
            data = loader.load_data()
            
            if not data:
                print("Still failed to load data. Exiting.")
                return
        
        print(f"✅ Loaded data for {len(data)} artists")
        
        # Show sample info
        artists = loader.get_all_artists()
        if artists:
            print(f"\n🎵 Sample artists in dataset:")
            for i, artist in enumerate(artists[:5], 1):
                tracks = loader.get_tracks_by_artist(artist)
                print(f"   {i}. {artist} ({len(tracks)} tracks)")
        
        # Create similarity calculator
        print("\n2. Initializing similarity calculator...")
        calculator = SimilarityCalculator(loader)
        print("✅ Calculator ready")
        
        # Launch GUI
        print("\n3. Launching GUI...")
        app = RecommendationGUI(loader, calculator)
        print("✅ GUI loaded successfully")
        print("\n" + "=" * 60)
        print("Application ready! Close the window to exit.")
        print("=" * 60 + "\n")
        
        app.run()
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("\nRequired files in 'modules' folder:")
        print("1. load_dataset_module.py")
        print("2. similarity_module.py")
        print("3. user_interface_module.py")
        print("4. statistics_module.py")
        
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
        
        # Create data directory
        os.makedirs('data', exist_ok=True)
        
        # Create sample data
        data = []
        for i in range(100):
            artist_num = i % 10  # 10 artists
            data.append({
                'id': f'track_{i:03d}',
                'name': f'Song {i}',
                'artists': f'Artist {artist_num}',
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
        df.to_csv('data.csv', index=False)
        print(f"✅ Created sample data with {len(df)} tracks")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")

if __name__ == "__main__":
    main()