# pip install streamlit
# Load libraries
import streamlit as st
import pandas as pd
import requests
import json

import joblib

st.title("Prediction App")
st.write("this is a test")

# read the dataset to fill input options
df = pd.read_csv('data.csv')

# create the input elements
#CONSOLE  = st.text_input("CONSOLE")
CONSOLE = st.selectbox("CONSOLE", pd.unique(df['CONSOLE']))
YEAR = st.number_input("YEAR", step=1, value=df['YEAR'].min())
CATEGORY = st.selectbox("CATEGORY", pd.unique(df['CATEGORY']))
PUBLISHER = st.selectbox("PUBLISHER", pd.unique(df['PUBLISHER']))
RATING = st.selectbox("RATING", pd.unique(df['RATING']))
CRITICS_POINTS = st.number_input("CRITICS_POINTS", step=0.1)
USER_POINTS = st.number_input("USER_POINTS", step=0.1)

# convert the selected inputs user into json
inputs = {
"CONSOLE" : CONSOLE,
"YEAR" : YEAR,
"CATEGORY" : CATEGORY,
"PUBLISHER" : PUBLISHER,
"RATING" :  RATING,
"CRITICS_POINTS" : CRITICS_POINTS,
"USER_POINTS" : USER_POINTS
}


if st.button('Predict'):
    # predict using FastAPI endpoint
    #res = requests.post(url = "http://127.0.0.1:8000/predict", data = json.dumps(inputs))
    #st.json(res.text)

    # predict using pickle file
    model = joblib.load('vgsales_pipeline_model.pkl')
    #X_input = pd.DataFrame([{'CONSOLE':  data.CONSOLE,'YEAR':  data.YEAR,'CATEGORY':  data.CATEGORY,'PUBLISHER':  data.PUBLISHER,'RATING':  data.RATING,'CRITICS_POINTS':  data.CRITICS_POINTS,'USER_POINTS':  data.USER_POINTS}])
    print(type(inputs),inputs)
    #X_input = pd.DataFrame(inputs)
    d = {'CONSOLE': 'ds', 'YEAR': 1997, 'CATEGORY': 'role-playing', 'PUBLISHER': 'Nintendo', 'RATING': 'E', 'CRITICS_POINTS': 10.0, 'USER_POINTS': 10.0}

    X_input = pd.DataFrame(inputs,index=[0])
    prediction = model.predict(X_input)
    st.write(prediction)



# command to run in terminal: streamlit run webview.py    