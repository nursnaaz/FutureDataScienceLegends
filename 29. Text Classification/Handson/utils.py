# utility functions for text preprocessing

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import string
import numpy as np

# create a function to lowercase, remove punctuations,tokenize , remove stopwords and lemmatization
def preprocess_text(text):

    # lowercase
    text = text.lower()

    # remove punctuations
    text = text.translate(str.maketrans('','',string.punctuation))

    # tokenize
    tokens = word_tokenize(text)

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    #leammatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return ' '.join(tokens)

def get_word2vec_embeddings(tokens, model):
    """
    Generate Word2Vec embeddings for a list of tokens."""

    vectors = [model.wv[word] for word in tokens if word in model.wv]
    return np.mean(vectors, axis=0) if vectors else np.zeros(model.vector_size)

def get_glove_embeddings(tokens, model): #add blk for glove
    vectors = [model[word] for word in tokens if word in model]
    return np.mean(vectors, axis=0) if vectors else np.zeros(100)

def get_fasttext_embeddings(text, model): #add blk for fastext
    return model.get_sentence_vector(text)
