# quick_test.py - Quick test to verify everything works
import sys
import os

# Add modules to path
sys.path.insert(0, 'modules')

try:
    from load_dataset_module import DataLoader
    from similarity_module import SimilarityCalculator
    
    print("Testing Music Recommendation Engine")
    print("=" * 50)
    
    # Check if data exists
    if not os.path.exists('data.csv'):
        print("❌ No data.csv found. Creating sample data...")
        import pandas as pd
        import random
        
        os.makedirs('data', exist_ok=True)
        
        data = []
        for i in range(50):
            data.append({
                'id': f'track_{i:03d}',
                'name': f'Song {i}',
                'artists': f'Artist {i%5}',
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
        
        pd.DataFrame(data).to_csv('data.csv', index=False)
        print("✅ Created sample data")
    
    # Load data
    print("\n1. Loading data...")
    loader = DataLoader('data.csv')
    data = loader.load_data()
    
    if data:
        print(f"✅ Loaded {len(data)} artists")
        
        # Show some artists
        artists = loader.get_all_artists()
        print(f"\n2. Sample artists:")
        for i, artist in enumerate(artists[:3], 1):
            print(f"   {i}. {artist}")
        
        # Test similarity
        print("\n3. Testing similarity calculation...")
        calculator = SimilarityCalculator(loader)
        
        if len(artists) >= 2:
            sim = calculator.compute_similarity(artists[0], artists[1], 'artist', 'cosine')
            print(f"   Cosine similarity between '{artists[0]}' and '{artists[1]}': {sim:.4f}")
        
        # Test recommendations
        print("\n4. Testing recommendations...")
        if artists:
            recs = calculator.get_top_similar(artists[0], 'artist', 'cosine', 3)
            print(f"   Top 3 recommendations for '{artists[0]}':")
            for i, (name, score) in enumerate(recs, 1):
                print(f"   {i}. {name}: {score:.4f}")
        
        print("\n" + "=" * 50)
        print("✅ All tests passed! Now run: python main.py")
        
    else:
        print("❌ Failed to load data")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nMake sure these files exist in 'modules' folder:")
    print("- load_dataset_module.py")
    print("- similarity_module.py")
    print("- statistics_module.py")
except Exception as e:
    print(f"❌ Error: {e}")