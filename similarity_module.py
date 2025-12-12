"""
similarity_module.py - Complete working version
"""

import math

class SimilarityCalculator:
    def __init__(self, data_loader):
        self.loader = data_loader
        print("SimilarityCalculator initialized")
    
    def _get_track_features(self, identifier):
        """Get features for a track by ID or name"""
        # Try by ID first
        track = self.loader.get_track_by_id(identifier)
        
        # If not found by ID, try by name
        if not track:
            tracks = self.loader.get_tracks_by_name(identifier)
            if tracks:
                track = tracks[0][1]  # Take first match
        
        if not track:
            return None
        
        # Return feature vector
        return [
            track['acousticness'],
            track['danceability'],
            track['energy'],
            track['liveness'],
            track['loudness'],
            track['popularity'],
            track['speechiness'],
            track['tempo'],
            track['valence']
        ]
    
    def _get_artist_features(self, artist_name):
        """Get average features for an artist"""
        tracks = self.loader.get_tracks_by_artist(artist_name)
        if not tracks:
            return None
        
        # Initialize feature accumulators
        features = {
            'acousticness': [], 'danceability': [], 'energy': [],
            'liveness': [], 'loudness': [], 'popularity': [],
            'speechiness': [], 'tempo': [], 'valence': []
        }
        
        # Collect features from all tracks
        for track in tracks:
            for feature in features:
                features[feature].append(track[feature])
        
        # Calculate averages
        avg_features = []
        for feature in ['acousticness', 'danceability', 'energy', 'liveness',
                       'loudness', 'popularity', 'speechiness', 'tempo', 'valence']:
            if features[feature]:
                avg_features.append(sum(features[feature]) / len(features[feature]))
            else:
                avg_features.append(0)
        
        return avg_features
    
    def euclidean_similarity(self, item1, item2, item_type='track'):
        """Euclidean distance similarity"""
        if item_type == 'track':
            vec1 = self._get_track_features(item1)
            vec2 = self._get_track_features(item2)
        else:
            vec1 = self._get_artist_features(item1)
            vec2 = self._get_artist_features(item2)
        
        if not vec1 or not vec2:
            return 0
        
        # Calculate Euclidean distance
        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))
        return 1 / (1 + distance)
    
    def cosine_similarity(self, item1, item2, item_type='track'):
        """Cosine similarity"""
        if item_type == 'track':
            vec1 = self._get_track_features(item1)
            vec2 = self._get_track_features(item2)
        else:
            vec1 = self._get_artist_features(item1)
            vec2 = self._get_artist_features(item2)
        
        if not vec1 or not vec2:
            return 0
        
        # Calculate dot product and magnitudes
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        mag1 = math.sqrt(sum(a ** 2 for a in vec1))
        mag2 = math.sqrt(sum(b ** 2 for b in vec2))
        
        if mag1 == 0 or mag2 == 0:
            return 0
        
        return dot_product / (mag1 * mag2)
    
    def pearson_similarity(self, item1, item2, item_type='track'):
        """Pearson correlation similarity"""
        if item_type == 'track':
            vec1 = self._get_track_features(item1)
            vec2 = self._get_track_features(item2)
        else:
            vec1 = self._get_artist_features(item1)
            vec2 = self._get_artist_features(item2)
        
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0
        
        n = len(vec1)
        
        # Calculate means
        mean1 = sum(vec1) / n
        mean2 = sum(vec2) / n
        
        # Calculate numerator and denominator
        numerator = sum((a - mean1) * (b - mean2) for a, b in zip(vec1, vec2))
        denom1 = math.sqrt(sum((a - mean1) ** 2 for a in vec1))
        denom2 = math.sqrt(sum((b - mean2) ** 2 for b in vec2))
        
        if denom1 == 0 or denom2 == 0:
            return 0
        
        correlation = numerator / (denom1 * denom2)
        # Convert from [-1, 1] to [0, 1]
        return (correlation + 1) / 2
    
    def manhattan_similarity(self, item1, item2, item_type='track'):
        """Manhattan distance similarity"""
        if item_type == 'track':
            vec1 = self._get_track_features(item1)
            vec2 = self._get_track_features(item2)
        else:
            vec1 = self._get_artist_features(item1)
            vec2 = self._get_artist_features(item2)
        
        if not vec1 or not vec2:
            return 0
        
        # Calculate Manhattan distance
        distance = sum(abs(a - b) for a, b in zip(vec1, vec2))
        return 1 / (1 + distance)
    
    def compute_similarity(self, item1, item2, item_type='track', metric='cosine'):
        """Compute similarity using specified metric"""
        metrics = {
            'euclidean': self.euclidean_similarity,
            'cosine': self.cosine_similarity,
            'pearson': self.pearson_similarity,
            'manhattan': self.manhattan_similarity
        }
        
        if metric not in metrics:
            print(f"Unknown metric: {metric}. Using cosine.")
            metric = 'cosine'
        
        return metrics[metric](item1, item2, item_type)
    
    def get_top_similar(self, query_item, item_type='track', metric='cosine', top_n=5):
        """Get top N similar items"""
        try:
            results = []
            
            if item_type == 'artist':
                # Compare with all artists
                artists = self.loader.get_all_artists()
                for artist in artists:
                    if artist != query_item:
                        similarity = self.compute_similarity(
                            query_item, artist, 'artist', metric
                        )
                        if similarity > 0:
                            results.append((artist, similarity))
            
            else:  # track
                # Compare with all tracks
                tracks = self.loader.get_all_tracks()
                for track in tracks:
                    if track['id'] != query_item and track['name'] != query_item:
                        similarity = self.compute_similarity(
                            query_item, track['id'], 'track', metric
                        )
                        if similarity > 0:
                            results.append((track['name'], similarity))
            
            # Sort by similarity (descending)
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:top_n]
            
        except Exception as e:
            print(f"Error finding similar items: {e}")
            return []