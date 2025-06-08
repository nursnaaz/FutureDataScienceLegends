
'''
import streamlit as st
import  numpy as np
import pandas as pd

import joblib
from keras.models import load_model

import warnings
warnings.filterwarnings('ignore')

st.title('Housing PricePrediction')

def predict():
  pass

fp = '/content/HousesInfo.txt'
df = pd.read_csv(fp, sep=' ', header=None)
df.columns = ['bedrooms', 'bathrooms', 'area', 'zipcode', 'price']

selected_values = {}
for column in df.drop(columns=['price']).columns:
  selected_values[column] = st.number_input(
      f'Select a value for {column}')
'''
import streamlit as st
import numpy as np
import pandas as pd

import joblib
import warnings
warnings.filterwarnings('ignore')
from tensorflow.keras.models import load_model

# Title of the app
st.title("Housing Price Prediction")

# Instructions
st.write("""Select the housing features you'd like to predict:""")

# Load the pickled models and keras model
pscaler = joblib.load('/content/scaler.pkl')
pencoder = joblib.load('/content/encoder.pkl')
pmodel = load_model('/content/hp_nn_model.keras')

# Function to predict
#@st.cache_resource
def predict(imodel, _iscaler, _iencoder, ifeatures):
    # encode the features
    #for ft in ifeatures:
    #  if ifeatures[ft].
    print(ifeatures, type(ifeatures))
    ind_cols =  ["bedrooms", "bathrooms", "area", "zipcode"]
    cat_col = ['zipcode']
    num_col = ['bedrooms','bathrooms','area']
    tmp_df = pd.DataFrame(ifeatures,columns=ind_cols)
    encoded_features = pd.DataFrame(_iencoder.transform(tmp_df[cat_col]))

    # Scale the features
    scaled_features = pd.DataFrame(_iscaler.transform(tmp_df[num_col]))
    print(type(scaled_features),scaled_features)
    print(type(encoded_features),encoded_features)
    tmp_fin_data = pd.concat([scaled_features,encoded_features], axis=1)
    print(tmp_fin_data)

    # Predict using the Neural Network model
    prediction = imodel.predict(tmp_fin_data)

    return prediction

#fp = '/content/drive/MyDrive/Customer Data.csv'
fp='/content/HousesInfo.txt'
cols = ["bedrooms", "bathrooms", "area", "zipcode", "price"]
df = pd.read_csv(fp, sep=" ", header=None, names=cols)

# Loop through each column and display a selectbox with the minimum value as the default
selected_values = {}
for column in df.drop(columns=['price']).columns:
    # Get the minimum value of the column
    min_value = df[column].min()

    if column=='zipcode':

      # Display a selectbox for the column with the minimum value as the default
      selected_values[column] = st.selectbox(
          f'Select a value for {column}',
          df[column].unique().tolist(),
          index=df[column].tolist().index(min_value)  # Set the default to the minimum value
      )

    else:
      # Check if the column's dtype is an integer type
      if np.issubdtype(df[column].dtype, np.integer):
          step = 1  # Integer step
      else:
          step = 0.5  # Float step

      # Display a number input box for the column with the minimum value as the default
      selected_values[column] = st.number_input(
          f'Select a value for {column}',
        min_value=min_value,  # minimum allowed value
        value=min_value,      # default value set to the minimum value
        #step=1 if pd.api.types.is_integer_dtype(df[column]) else 0.01  # Step size depending on data type
        #step=1 if isinstance(df[column].dtype,'Int64') else 0.01
        step = step
      )

# Add a submit button
if st.button('Submit'):
    # Load your trained model (replace 'your_model.joblib' with your model's file path)
    #model = joblib.load('kmeans_model.pkl')
    #model = load_model('/content/hp_nn_model.keras')

    # Prepare the data for prediction (ensure the data matches the model's expected input format)
    input_data = [list(selected_values.values())]  # Convert selected values to list for prediction
    #print(input_data)
    # Use the model to predict
    #prediction = model.predict(pd.DataFrame(input_data))
    # Get the prediction
    prediction = predict(pmodel, pscaler, pencoder, input_data)

    # Display the prediction result
    st.subheader("Prediction:")
    st.write(f"The predicted house price is: {prediction}")  # Assuming the model returns a single prediction
