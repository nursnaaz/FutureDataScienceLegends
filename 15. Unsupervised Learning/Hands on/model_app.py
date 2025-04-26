
import streamlit as st
import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

import joblib

fp  = 'Customer Data.csv'
df = pd.read_csv(fp)

print('data loaded')

# lopp theu dataframe and assign the link or create the respective fields
selected_values = {}
for column in df.drop(columns=['CUST_ID']).columns:
    selected_values[column] = st.number_input(
    f'Select a value for {column}'
    )

print('elements are created')

pklfile = "mymodel2.pkl"
if st.button('Submit'):
    # load the model
    model = joblib.load(pklfile)
    
    input_data = [list(selected_values.values())]
    
    #prediction
    prediction = model.predict(input_data)
    
    #write the result
    st.write(f"Prediction: the input data belongs to cluster:{prediction}")
    