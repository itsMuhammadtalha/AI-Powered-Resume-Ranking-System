# src/nlp_utils.py
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
# nltk.download('punkt')

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def tokenize(text):
    # Tokenize the text into words using spaCy
    doc = nlp(text)
    return [token.text.lower() for token in doc]

def calculate_similarity(resume_text, job_description):
    # Create a TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    
    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_matrix[0][0]