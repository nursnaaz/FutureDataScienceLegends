import re
import unidecode
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import download
import contractions
import nltk
nltk.download('wordnet')
download('punkt')
download('stopwords')
download('omw-1.4')

def preprocess_text(text):
    # 1. Remove HTML
    text = BeautifulSoup(text, "html.parser").get_text()

    # 2. Remove contradictions - assuming this means handling contractions (e.g., "don't" -> "do not")
    text = contractions.fix(text)
    
    # 3. Remove accented characters
    text = unidecode.unidecode(text)
    
    # 4. Remove non-alphanumeric characters (keeping spaces)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # 5. Convert to lowercase
    text = text.lower()
    
    # 6. Remove stopwords
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    text = ' '.join(filtered_text)
    
    
    # 7. Stemming
    stemmer = PorterStemmer()
    stemmed_text = [stemmer.stem(word) for word in text]
    text = ''.join(stemmed_text)

    # 8. Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_text = [lemmatizer.lemmatize(word) for word in text.split(' ')]
    
    # Optional: Combine stemming and lemmatization
    # It's generally not recommended to use both, but if needed, uncomment the following lines:
    # stemmer = PorterStemmer()
    # stemmed_and_lemmatized_text = [stemmer.stem(word) for word in lemmatized_text]
    # text = ' '.join(stemmed_and_lemmatized_text)
    
    # If only lemmatization is needed:
    text = ' '.join(lemmatized_text)
    
    return text