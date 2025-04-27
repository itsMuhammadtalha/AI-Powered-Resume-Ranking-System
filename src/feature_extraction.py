from sklearn.feature_extraction.text import TfidfVectorizer

def extract_features(candidate_data):
    # Combine skills and experience for feature extraction
    candidate_data['Combined'] = candidate_data['Skills'] + ' ' + candidate_data['Experience']
    
    # Use TF-IDF Vectorizer to convert text data into numerical vectors
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(candidate_data['Combined'])
    
    return features
