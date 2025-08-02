
import streamlit as st
import pandas as pd
import numpy as np
import joblib

#from utils import preprocess_text

import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

# remove common words like "the,is,and,etc'
nltk.download('stopwords')

# do lemmatization
nltk.download('wordnet')

nltk.download('punkt_tab')

from gensim.models import Word2Vec #addfor w2v
#from utils import preprocess_text , get_word2vec_embeddings #addfor w2v
from utils import preprocess_text, get_word2vec_embeddings, get_glove_embeddings, get_fasttext_embeddings #add glov,ft

from sklearn.metrics.pairwise import cosine_similarity #addfor recom
from textblob import TextBlob #addfor sentiment
from gensim.models import KeyedVectors #add glove
import fasttext

@st.cache_resource
def load_models():

    tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
    lr_model_tfidf = joblib.load('lr_model_tfidf.pkl')
    tgt_names = joblib.load('target_names.pkl')

    data = pd.read_csv('preprocessed_data.csv')

    w2v_model = Word2Vec.load('word2vec.model') #addfor w2v
    lr_model_word2vec = joblib.load('lr_model_word2vec.pkl') #addfor w2v

    gbc_model_tfidf = joblib.load('gbc_model_tfidf.pkl') #addfor gbc
    gbc_model_word2vec = joblib.load('gbc_model_word2vec.pkl') #addfor gbc

    lr_model_glove = joblib.load('lr_model_glove.pkl') #add for glv ft blk
    gbc_model_glove = joblib.load('gbc_model_glove.pkl')
    lr_model_fasttext = joblib.load('lr_model_fasttext.pkl')
    gbc_model_fasttext = joblib.load('gbc_model_fasttext.pkl')

    glove_model = KeyedVectors.load_word2vec_format('glove.6B.50d.txt', binary=False, no_header=True)
    ft_model = fasttext.load_model('fasttext.model')


    X_tfidf = tfidf_vectorizer.transform(data['claened_text'])
    tokenized_texts = [word_tokenize(text) for text in data['claened_text']]

    X_w2v = np.array([get_word2vec_embeddings(text, w2v_model) for text in tokenized_texts]) #addfor w2v

    X_glove = np.array([get_glove_embeddings(text, glove_model) for text in tokenized_texts]) #add blk glv, tf
    X_ft = np.array([get_fasttext_embeddings(" ".join(tokens), ft_model) for tokens in tokenized_texts])
    X_features = {'tfidf': X_tfidf, 'word2vec': X_w2v, 'glove': X_glove, 'fasttext': X_ft}

    #X_features = {'tfidf': X_tfidf}
    #X_features = {'tfidf': X_tfidf, 'word2vec': X_w2v} #addfor w2v



    return(tfidf_vectorizer, lr_model_tfidf, w2v_model, lr_model_word2vec, glove_model, ft_model,
           lr_model_glove, gbc_model_glove, lr_model_fasttext, gbc_model_fasttext,
           gbc_model_tfidf, gbc_model_word2vec, tgt_names, data, X_features) #addfor w2v, glv, ft


tfidf_vectorizer, lr_model_tfidf, w2v_model, lr_model_word2vec, glove_model, ft_model, \
lr_model_glove, gbc_model_glove, lr_model_fasttext, gbc_model_fasttext, \
gbc_model_tfidf, gbc_model_word2vec, tgt_names, data, X_features = load_models() #addfor w2v, glv,ft



st.title('Text App for Forum')


#task = st.sidebar.selectbox('Select Task',["Classification"]) #"Recommendation"
#task = st.sidebar.selectbox('Select Task',["Classification","Recommendation"]) #addfor recom
task = st.sidebar.selectbox('Select Task',["Classification","Recommendation","Sentiment Analysis"]) #addfor sentiment

#feature_type = st.sidebar.selectbox('Select Feature Type',["TFIDF"])
#feature_type = st.sidebar.selectbox("Select Feature Type", ["TFIDF", "Word2Vec"]) #add w2v
feature_type = st.sidebar.selectbox("Select Feature Type", ["TFIDF", "Word2Vec", "GloVe", "FastText"]) #addd glv,ft

user_input = st.text_area("enter text for analysis:",height =150)

if st.button("Analyze"):
  if user_input:
      cleaned_input  = preprocess_text(user_input)
      tokenized_input = word_tokenize(cleaned_input)#add w2v

      if feature_type == "TFIDF":
          X_input = tfidf_vectorizer.transform([cleaned_input])
          lr_model = lr_model_tfidf
          gbc_model = gbc_model_tfidf # add gbc
      elif feature_type == "Word2Vec":  # add w2v blk
            X_input = np.array([get_word2vec_embeddings(tokenized_input, w2v_model)])
            lr_model = lr_model_word2vec
            gbc_model = gbc_model_word2vec # add gbc
      elif feature_type == "GloVe": #add glv blk
            X_input = np.array([get_glove_embeddings(tokenized_input, glove_model)])
            lr_model = lr_model_glove
            gbc_model = gbc_model_glove
      else:  # FastText #add ft blk
            X_input = np.array([get_fasttext_embeddings(cleaned_input, ft_model)])
            lr_model = lr_model_fasttext
            gbc_model = gbc_model_fasttext
      if task ==  "Classification":
          lr_pred = lr_model.predict(X_input)[0]

          print(lr_pred)
          st.subheader('Results:')
          st.write(f'Logistic Regfression Prediction: {tgt_names[lr_pred]}')
          gbc_pred = gbc_model.predict(X_input)[0] #addfor gbc
          st.write(f'GBC Prediction: {tgt_names[gbc_pred]}') #addfor gbc
      elif task == "Recommendation": #addfor recom  blk
          sim_scores = cosine_similarity(X_input, X_features[feature_type.lower()])
          top_indices = sim_scores[0].argsort()[-5:][::-1]
          st.subheader("Top 5 Similar Documents")
          for idx in top_indices:
              st.write(f"**Category**: {data['category_name'][idx]}")
              st.write(f"**Text**: {data['text'][idx]}") #[:200]}...")
              st.write("---")
      elif task == "Sentiment Analysis": #addfor sentiment block
          sentiment = TextBlob(cleaned_input).sentiment.polarity
          st.subheader("Sentiment Analysis Result")
          st.write(f"Sentiment Polarity: {sentiment:.4f}")
          st.write("Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral")
  else:
    st.error('Please enter some text')


