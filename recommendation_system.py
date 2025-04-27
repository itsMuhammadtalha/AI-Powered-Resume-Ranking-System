# src/recommendation_system.py
from sklearn.metrics.pairwise import cosine_similarity
from feature_extraction import extract_features  

def recommend_candidates(candidate_data, candidate_index, top_n=3):
    # Extract features
    features = extract_features(candidate_data)
    
    # Calculate cosine similarity between candidates
    similarity_matrix = cosine_similarity(features)
    
    # Get the similarity scores for the selected candidate
    similarity_scores = list(enumerate(similarity_matrix[candidate_index]))
    
    # Sort candidates based on similarity scores
    sorted_candidates = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # Get the top N similar candidates (excluding the candidate itself)
    recommended_indices = [i[0] for i in sorted_candidates if i[0] != candidate_index][:top_n]
    
    # Create a DataFrame for recommended candidates
    recommended_candidates = candidate_data.iloc[recommended_indices].copy()
    recommended_candidates['Similarity Score'] = [similarity_matrix[candidate_index][i] for i in recommended_indices]
    
    return recommended_candidates