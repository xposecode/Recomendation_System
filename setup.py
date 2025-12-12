# setup.py - Run this first to set up everything
import os
import subprocess
import sys

def setup_project():
    print("Setting up Music Recommendation Engine...")
    print("=" * 50)
    
    # Create folder structure
    folders = ['modules', 'data', 'tests']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✓ Created folder: {folder}")
    
    # Create empty __init__.py in modules
    with open('modules/__init__.py', 'w') as f:
        f.write('')
    print("✓ Created modules/__init__.py")
    
    # Install pandas
    print("\nInstalling pandas...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
        print("✓ pandas installed successfully")
    except:
        print("✗ Could not install pandas. Please run: pip install pandas")
    
    # Check for data.csv
    if not os.path.exists('data.csv'):
        print("\nNo data.csv found. Creating sample data...")
        create_sample_data()
    
    print("\n" + "=" * 50)
    print("Setup complete! Now run: python main.py")
    print("=" * 50)

def create_sample_data():
    try:
        import pandas as pd
        import random
        
        data = []
        for i in range(100):
            data.append({
                'id': f'track_{i:03d}',
                'name': f'Song {i}',
                'artists': f'Artist {i%10}',
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
        print(f"✓ Created sample data with {len(df)} tracks")
        
    except ImportError:
        print("✗ Could not create sample data. pandas not installed.")
    except Exception as e:
        print(f"✗ Error creating sample data: {e}")

if __name__ == "__main__":
    setup_project()