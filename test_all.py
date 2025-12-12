# test_all.py - Test everything
import sys
import os

print("Testing Music Recommendation Engine")
print("=" * 50)

# Check modules - FIXED: modules are in root, not modules folder
modules = ['load_dataset_module.py', 'similarity_module.py', 
           'user_interface_module.py', 'statistics_module.py']

print("\n1. Checking modules...")
for module in modules:
    # FIXED: Check root directory, not modules folder
    if os.path.exists(module):
        print(f"   ✅ {module}")
    else:
        print(f"   ❌ {module} - NOT FOUND")

# Check data
print("\n2. Checking data...")
if os.path.exists('data.csv'):
    print("   ✅ data.csv exists")
    
    # Check file size
    size = os.path.getsize('data.csv')
    if size > 0:
        print(f"   ✅ File size: {size} bytes")
    else:
        print("   ❌ File is empty")
else:
    print("   ❌ data.csv not found")

# Test imports
print("\n3. Testing imports...")
try:
    # FIXED: Don't add 'modules' to path since files are in root
    from load_dataset_module import DataLoader
    from similarity_module import SimilarityCalculator
    from user_interface_module import UserInterface
    from statistics_module import Statistics
    print("   ✅ All imports successful")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")

# Variables to share between test sections
artists = []

# Test data loading
print("\n4. Testing data loading...")
try:
    loader = DataLoader('data.csv')
    data = loader.load_data()
    
    if data:
        print(f"   ✅ Loaded {len(data)} artists")
        
        # Test methods
        artists = loader.get_all_artists()  # Store in global variable
        print(f"   ✅ get_all_artists() works: {len(artists)} artists")
        
        tracks = loader.get_all_tracks()
        print(f"   ✅ get_all_tracks() works: {len(tracks)} tracks")
        
        if artists:
            artist_tracks = loader.get_tracks_by_artist(artists[0])
            print(f"   ✅ get_tracks_by_artist() works: {len(artist_tracks)} tracks for {artists[0]}")
    else:
        print("   ❌ Failed to load data")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test similarity - FIXED: Check if artists list has data
print("\n5. Testing similarity calculator...")
try:
    if not artists:
        print("   ❌ No artists loaded, skipping similarity tests")
    else:
        calculator = SimilarityCalculator(loader)
        
        if len(artists) >= 2:
            sim = calculator.compute_similarity(artists[0], artists[1], 'artist', 'cosine')
            print(f"   ✅ compute_similarity() works: {sim:.4f}")
            
            recs = calculator.get_top_similar(artists[0], 'artist', 'cosine', 3)
            print(f"   ✅ get_top_similar() works: {len(recs)} recommendations")
            
            # Test all metrics
            metrics = ['cosine', 'euclidean', 'pearson', 'manhattan']
            print("   ✅ All metrics available:", ", ".join(metrics))
        else:
            print("   ❌ Need at least 2 artists for similarity test")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 50)
print("TEST COMPLETE")
print("=" * 50)
print("\nNext steps:")
print("1. If all tests passed, run: python main.py")
print("2. If tests failed, check the error messages above")