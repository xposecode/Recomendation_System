"""
similarity_module.py
File: Similarity Calculations for Music Recommendation
Author: [Your Name]
Student ID: [Your ID]
Course: [Course Name]
"""

import math
import pandas as pd
import random

class SimilarityCalculator:
    
    def __init__(self, data_manager):
        self.data = data_manager
        self.artist_features_df = None
        print("Similarity calculator created")
    
    def get_artist_feature_vector(self, artist_name):
        """Get feature vector for an artist using Feature1, Feature2, etc."""
        if self.artist_features_df is None:
            self.artist_features_df = self.data.get_artist_features_dataframe()
        
        if self.artist_features_df is None:
            return None
        
        artist_row = self.artist_features_df[self.artist_features_df['Artist_name'] == artist_name]
        
        if artist_row.empty:
            return None
        
        # Get all Feature columns (Feature1, Feature2, etc.)
        feature_vector = []
        for col in self.artist_features_df.columns:
            if col.startswith('Feature'):
                feature_vector.append(artist_row[col].values[0])
        
        return feature_vector
    
    def euclidean_distance(self, vector1, vector2):
        """Calculate Euclidean distance between two vectors"""
        if not vector1 or not vector2 or len(vector1) != len(vector2):
            return float('inf')
        
        total = 0
        for i in range(len(vector1)):
            diff = vector1[i] - vector2[i]
            total += diff * diff
        
        return math.sqrt(total)
    
    def cosine_similarity(self, vector1, vector2):
        """Calculate cosine similarity between two vectors"""
        if not vector1 or not vector2 or len(vector1) != len(vector2):
            return 0
        
        dot = 0
        mag1 = 0
        mag2 = 0
        
        for i in range(len(vector1)):
            dot += vector1[i] * vector2[i]
            mag1 += vector1[i] * vector1[i]
            mag2 += vector2[i] * vector2[i]
        
        if mag1 == 0 or mag2 == 0:
            return 0
        
        mag1 = math.sqrt(mag1)
        mag2 = math.sqrt(mag2)
        
        return dot / (mag1 * mag2)
    
    def pearson_correlation(self, vector1, vector2):
        """Calculate Pearson correlation between two vectors"""
        if not vector1 or not vector2 or len(vector1) != len(vector2):
            return 0
        
        n = len(vector1)
        
        mean1 = sum(vector1) / n
        mean2 = sum(vector2) / n
        
        top = 0
        bottom1 = 0
        bottom2 = 0
        
        for i in range(n):
            diff1 = vector1[i] - mean1
            diff2 = vector2[i] - mean2
            top += diff1 * diff2
            bottom1 += diff1 * diff1
            bottom2 += diff2 * diff2
        
        if bottom1 == 0 or bottom2 == 0:
            return 0
        
        corr = top / (math.sqrt(bottom1) * math.sqrt(bottom2))
        
        # Convert from -1..1 to 0..1 for similarity
        similarity = (corr + 1) / 2
        return similarity
    
    def find_top_similar_artists(self, artist_name, similarity_metric='cosine', top_n=5):
        """Task 1: Find top 5 similar artists (similarity > 0.8)"""
        if self.artist_features_df is None:
            self.artist_features_df = self.data.get_artist_features_dataframe()
        
        if self.artist_features_df is None:
            return []
        
        target_vector = self.get_artist_feature_vector(artist_name)
        if target_vector is None:
            print(f"Artist '{artist_name}' not found in dataframe")
            return []
        
        similarity_list = []
        
        for _, row in self.artist_features_df.iterrows():
            current_artist = row['Artist_name']
            
            if current_artist == artist_name:
                continue  # Skip the same artist
            
            # Get feature vector for current artist
            current_vector = []
            for col in self.artist_features_df.columns:
                if col.startswith('Feature'):
                    current_vector.append(row[col])
            
            # Calculate similarity based on selected metric
            if similarity_metric == 'cosine':
                similarity = self.cosine_similarity(target_vector, current_vector)
            elif similarity_metric == 'euclidean':
                distance = self.euclidean_distance(target_vector, current_vector)
                similarity = 1 / (1 + distance) if distance != float('inf') else 0
            elif similarity_metric == 'pearson':
                similarity = self.pearson_correlation(target_vector, current_vector)
            else:
                print(f"Unknown metric: {similarity_metric}. Using cosine.")
                similarity = self.cosine_similarity(target_vector, current_vector)
            
            # Only include if similarity > 0.8 as per assignment
            if similarity > 0.8:
                similarity_list.append([current_artist, similarity])
        
        if similarity_list:
            # Create dataframe and sort
            scores_df = pd.DataFrame(similarity_list, columns=['Artist', 'Similarity'])
            scores_df = scores_df.sort_values('Similarity', ascending=False)
            
            # Return top N results
            top_results = scores_df.head(top_n)
            
            return list(top_results.itertuples(index=False, name=None))
        else:
            return []
    
    def get_artist_recommendations(self, artist_name, similarity_metric='cosine', num_rec=10):
        """Task 2: Get random recommendations from similar artists"""
        if self.artist_features_df is None:
            self.artist_features_df = self.data.get_artist_features_dataframe()
        
        if self.artist_features_df is None:
            return []
        
        target_vector = self.get_artist_feature_vector(artist_name)
        if target_vector is None:
            print(f"Artist '{artist_name}' not found in dataframe")
            return []
        
        all_similar = []
        
        for _, row in self.artist_features_df.iterrows():
            current_artist = row['Artist_name']
            
            if current_artist == artist_name:
                continue
            
            current_vector = []
            for col in self.artist_features_df.columns:
                if col.startswith('Feature'):
                    current_vector.append(row[col])
            
            if similarity_metric == 'cosine':
                similarity = self.cosine_similarity(target_vector, current_vector)
            elif similarity_metric == 'euclidean':
                distance = self.euclidean_distance(target_vector, current_vector)
                similarity = 1 / (1 + distance) if distance != float('inf') else 0
            elif similarity_metric == 'pearson':
                similarity = self.pearson_correlation(target_vector, current_vector)
            else:
                similarity = self.cosine_similarity(target_vector, current_vector)
            
            if similarity > 0:
                all_similar.append((current_artist, similarity))
        
        if not all_similar:
            return []
        
        # Sort by similarity
        all_similar.sort(key=lambda x: x[1], reverse=True)
        
        # Take top 30 for sampling pool
        top_artists = all_similar[:30]
        
        if len(top_artists) <= num_rec:
            return top_artists
        else:
            # Random selection weighted by similarity
            artists, scores = zip(*top_artists)
            weights = [score for score in scores]
            
            total_weight = sum(weights)
            if total_weight > 0:
                norm_weights = [w/total_weight for w in weights]
                
                selected_indices = random.choices(
                    range(len(top_artists)),
                    weights=norm_weights,
                    k=num_rec
                )
                
                # Get unique selections
                unique_indices = list(set(selected_indices))
                recommendations = [top_artists[i] for i in unique_indices]
                
                # Sort by similarity for display
                recommendations.sort(key=lambda x: x[1], reverse=True)
                return recommendations
            else:
                return random.sample(top_artists, min(num_rec, len(top_artists)))
    
    def show_calculation_example(self):
        """Show example calculation from assignment"""
        print("\n" + "="*60)
        print("SIMILARITY CALCULATION EXAMPLE:")
        print("="*60)
        
        # Example vectors from assignment
        dani_vector = [2.6, 5.0]    # Dani = [2.6, 5]
        phyu_vector = [5.0, 2.67]   # Phyu = [5, 2.67]
        mofe_vector = [4.0, 4.0]    # Mofe = [4, 4]
        
        print(f"\nArtist vectors from assignment example:")
        print(f"  Dani: {dani_vector}")
        print(f"  Phyu: {phyu_vector}")
        print(f"  Mofe: {mofe_vector}")
        
        print(f"\nCosine similarity between Dani and Phyu:")
        similarity = self.cosine_similarity(dani_vector, phyu_vector)
        print(f"  Result: {similarity:.4f}")
        
        print(f"\nEuclidean distance between Dani and Phyu:")
        distance = self.euclidean_distance(dani_vector, phyu_vector)
        print(f"  Distance: {distance:.4f}")
        print(f"  Similarity: {1/(1+distance):.4f}")
        
        print(f"\nPearson correlation between Dani and Phyu:")
        correlation = self.pearson_correlation(dani_vector, phyu_vector)
        print(f"  Correlation: {correlation:.4f}")

def test_similarity_calculator():
    """Test the similarity calculator functions"""
    print("Testing SimilarityCalculator...")
    
    # Create a simple example
    calculator = SimilarityCalculator(None)
    
    # Test with example vectors from assignment
    vector1 = [2.6, 5.0]
    vector2 = [5.0, 2.67]
    
    print(f"\nTest vectors: {vector1} and {vector2}")
    print(f"Cosine similarity: {calculator.cosine_similarity(vector1, vector2):.4f}")
    print(f"Euclidean distance: {calculator.euclidean_distance(vector1, vector2):.4f}")
    print(f"Pearson correlation: {calculator.pearson_correlation(vector1, vector2):.4f}")
    
    print("\nModule structure test passed!")
    print("Contains required assignment functions:")
    print("1. find_top_similar_artists() - Task 1")
    print("2. get_artist_recommendations() - Task 2")

if __name__ == "__main__":
    test_similarity_calculator()