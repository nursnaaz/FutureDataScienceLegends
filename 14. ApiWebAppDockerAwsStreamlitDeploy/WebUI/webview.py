# create a new folder
# copy the pickle file and train-dataset-file to that new folder

# web app development using streamlit
# load the necessary libraries

# try to install by  below command
# !pip install streamlit

import streamlit as st
import numpy as np
import pandas as pd
import joblib

st.title("Promotion Prediction App")

# read the dataset to fill the values in input options of each element
df = pd.read_csv('train_LZdllcl.csv')

# create the input elements
# categorical columns
department = st.selectbox("Department", pd.unique(df['department']))
region = st.selectbox("Region", pd.unique(df['region']))
education = st.selectbox("Education", pd.unique(df['education']))
gender = st.selectbox("Gender", pd.unique(df['gender']))
recruitment_channel = st.selectbox("Recruitment_channel", pd.unique(df['recruitment_channel']))

# non-categorical columns
no_of_trainings = st.number_input("No_of_trainings")
age = st.number_input("Age")
previous_year_rating = st.number_input("Previous_year_rating")
length_of_service = st.number_input("Length_of_service")
KPIs_met_80 = st.number_input("KPIs_met >80%")
awards_won = st.number_input("Enter Awards_won?")
avg_training_score = st.number_input("Avg_training_score")

# map the user inputs to respective column format
inputs = {
'department': department, 
'region': region, 
'education': education, 
'gender': gender,
'recruitment_channel': recruitment_channel, 
'no_of_trainings': no_of_trainings, 
'age': age, 
'previous_year_rating': previous_year_rating,
'length_of_service': length_of_service, 
'KPIs_met >80%': KPIs_met_80, 
'awards_won?': awards_won,
'avg_training_score': avg_training_score 
}

# load the model from the pickle file
model = joblib.load('promote_pipeline_model.pkl')

# action for submit button
if st.button('Predict'):
    X_input = pd.DataFrame(inputs,index=[0])    
    prediction = model.predict(X_input)
    st.write("The predicted value is:")
    st.write(prediction)

#File upload experiment
st.subheader("Please upload a csv file for prediction")
upload_file = st.file_uploader("Choose a csv file", type=['csv'])

if upload_file is not None:
    df = pd.read_csv(upload_file)

    st.write("File uploaded successfully") 
    st.write(df.head(2))

    if st.button("Predict for the uploaded file"):
        df['is_promoted'] = model.predict(df)
        st.write("Prediction completed")
        st.write(df.head(2))
        st.download_button(label="Download Prediction", 
                           data=df.to_csv(index=False), 
                           file_name="predictions.csv", mime="text/csv")


