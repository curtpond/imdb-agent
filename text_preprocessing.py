import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

def download_nltk_resources():
    """Download required NLTK resources."""
    resources = ['stopwords', 'wordnet']
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
        except Exception as e:
            print(f"Error downloading {resource}: {e}")

def preprocess_text(text):
    """
    Preprocess text by performing the following steps:
    1. Convert to lowercase
    2. Remove special characters and numbers
    3. Remove extra whitespace
    4. Tokenize
    5. Remove stopwords
    6. Lemmatize
    
    Args:
        text (str): Input text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Simple tokenization by splitting on whitespace
    tokens = text.split()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return ' '.join(tokens)

def create_tfidf_matrix(texts, max_features=1000):
    """
    Create TF-IDF matrix from a list of texts.
    
    Args:
        texts (list): List of text documents
        max_features (int): Maximum number of features for TF-IDF
        
    Returns:
        tuple: (TF-IDF matrix, feature names)
    """
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        stop_words='english',
        ngram_range=(1, 2)
    )
    tfidf_matrix = vectorizer.fit_transform(texts)
    return tfidf_matrix, vectorizer.get_feature_names_out()

def extract_keywords(text, n_keywords=5):
    """
    Extract top keywords from a text using TF-IDF.
    
    Args:
        text (str): Input text
        n_keywords (int): Number of keywords to extract
        
    Returns:
        list: Top keywords
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    
    # Get sorted indices of TF-IDF scores
    scores = tfidf_matrix.toarray()[0]
    sorted_indices = scores.argsort()[::-1]
    
    # Get top keywords
    return [feature_names[idx] for idx in sorted_indices[:n_keywords]]
