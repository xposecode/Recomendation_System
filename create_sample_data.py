# create_data.py - Create proper sample dataset
import pandas as pd
import numpy as np
import random

def create_sample_dataset(filename='data.csv', num_tracks=200):
    """Create a realistic music dataset"""
    
    # List of sample artists
    artists = [
        'Taylor Swift', 'Ed Sheeran', 'Drake', 'Ariana Grande', 'Billie Eilish',
        'Post Malone', 'Dua Lipa', 'The Weeknd', 'Bruno Mars', 'Coldplay',
        'Imagine Dragons', 'Maroon 5', 'Kendrick Lamar', 'Rihanna', 'Beyoncé',
        'Justin Bieber', 'Shawn Mendes', 'Harry Styles', 'Lady Gaga', 'Kanye West',
        'Adele', 'Sam Smith', 'Sia', 'Lana Del Rey', 'Frank Ocean',
        'John Legend', 'Halsey', 'Selena Gomez', 'Miley Cyrus', 'Katy Perry'
    ]
    
    # List of sample track names
    track_templates = [
        '{} Dreams', 'Electric {}', 'Midnight {}', '{} in the Dark',
        'Golden {}', 'Lost {}', 'Summer {}', 'Winter {}', '{} Waves',
        'Silent {}', 'Dancing {}', 'Crying {}', 'Laughing {}', 'Flying {}',
        'Broken {}', 'Healing {}', 'Whispering {}', 'Screaming {}',
        'Gentle {}', 'Wild {}'
    ]
    
    # Generate realistic data
    data = []
    
    for i in range(num_tracks):
        # Select 1-3 random artists
        num_artists = random.randint(1, 3)
        track_artists = random.sample(artists, num_artists)
        
        # Create track name
        track_template = random.choice(track_templates)
        track_word = random.choice(['Love', 'Heart', 'Soul', 'Fire', 'Water',
                                   'Air', 'Earth', 'Sky', 'Moon', 'Sun',
                                   'Star', 'Ocean', 'River', 'Mountain', 'Forest'])
        track_name = track_template.format(track_word)
        
        # Generate realistic feature values
        # Popular songs tend to have higher danceability and energy
        is_popular = random.random() < 0.3  # 30% chance of being popular
        
        if is_popular:
            danceability = random.uniform(0.6, 0.95)
            energy = random.uniform(0.7, 0.98)
            popularity = random.randint(70, 100)
        else:
            danceability = random.uniform(0.3, 0.8)
            energy = random.uniform(0.3, 0.85)
            popularity = random.randint(10, 70)
        
        # Generate correlated features
        # High energy often correlates with lower acousticness
        acousticness = max(0.0, 1.0 - energy * random.uniform(0.8, 1.2))
        
        # Valence (positivity) often correlates with danceability
        valence = danceability * random.uniform(0.8, 1.2)
        valence = min(1.0, max(0.0, valence))
        
        # Create track data
        track_data = {
            'id': f'spotify:track:{random.randint(1000000000, 9999999999)}',
            'name': track_name,
            'artists': str(track_artists),  # Store as string representation of list
            'acousticness': round(acousticness, 4),
            'danceability': round(danceability, 4),
            'energy': round(energy, 4),
            'liveness': round(random.uniform(0.0, 0.8), 4),  # Live recordings are rare
            'loudness': round(random.uniform(-25.0, -5.0), 4),  # Standard loudness range
            'popularity': popularity,
            'speechiness': round(random.uniform(0.0, 0.5), 4),  # Most music has low speechiness
            'tempo': round(random.uniform(60.0, 180.0), 4),  # BPM range
            'valence': round(valence, 4)
        }
        
        data.append(track_data)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Ensure all required columns are present
    required_columns = [
        'acousticness', 'artists', 'danceability', 'energy', 'id',
        'liveness', 'loudness', 'name', 'popularity', 'speechiness',
        'tempo', 'valence'
    ]
    
    # Save to CSV
    df.to_csv(filename, index=False)
    
    # Print dataset info
    print(f"✅ Created dataset with {len(df)} tracks")
    print(f"✅ File saved to: {filename}")
    print(f"✅ Columns: {', '.join(df.columns)}")
    print(f"✅ Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    # Show sample data
    print("\n📊 Sample data (first 3 rows):")
    print(df.head(3).to_string())
    
    # Show statistics
    print("\n📈 Dataset Statistics:")
    print(f"   Number of unique artists: {len(set([art for arts in df['artists'] for art in eval(arts)]))}")
    print(f"   Average popularity: {df['popularity'].mean():.1f}")
    print(f"   Average danceability: {df['danceability'].mean():.3f}")
    print(f"   Average energy: {df['energy'].mean():.3f}")
    
    return df

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    import os
    os.makedirs('data', exist_ok=True)
    
    # Create the dataset
    df = create_sample_dataset()
    
    # Test loading the dataset
    print("\n🧪 Testing data loading...")
    test_df = pd.read_csv('data.csv')
    print(f"✅ Test load successful: {len(test_df)} rows loaded")
    
    # Show available artists
    print("\n🎵 Sample artists in dataset:")
    all_artists = set()
    for artist_str in test_df['artists'].head(10):
        artists_list = eval(artist_str)
        all_artists.update(artists_list)
    
    print("   " + ", ".join(list(all_artists)[:10]) + "...")