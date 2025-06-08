
import streamlit as st
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')
from keras.models import load_model
import time
import os
import librosa

# Title of the app
st.title('Audio Classification system')

pmodel = load_model('/content/saved_models/audio_classification.keras')

uploaded_file=st.file_uploader("Choose an Audio file",
                               type=[".wav",".mp3"], 
                               accept_multiple_files=False) #"wave",".flac",

#Saving the browsed audio in our local
def Save_audio(upload_audio):
    try:
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        save_path = os.path.join(os.getcwd(), "uploads", upload_audio.name)
        with open(save_path, 'wb') as f:
            f.write(upload_audio.getbuffer())
        return save_path
    except Exception as e:
        print("Error saving file:", e)
        return None

#extract features using librosa(mfcc)
def extract_feature(file):
    data, sample_rates=librosa.load(file)
    mfcc_features=librosa.feature.mfcc(y=data,sr=sample_rates,n_mfcc=40)
    mfcc_scaled_feature=np.mean(mfcc_features.T,axis=0)

    mfcc_scaled_feature = mfcc_scaled_feature.reshape(1, -1)
    print(000,type(mfcc_scaled_feature),mfcc_scaled_feature)
    return mfcc_scaled_feature 


# Add a submit button
if st.button('Submit'):

  extract_features=[]
  if uploaded_file is not None:
      if Save_audio(uploaded_file):
          audio_bytes = uploaded_file.read()
          st.audio(audio_bytes, format="audio/wav")
          # extract_features.append(extract_feature(os.path.join("uploads",uploaded_file.name)))
          extract_features = extract_feature(os.path.join("uploads",uploaded_file.name))
          print(111,extract_features)
          progress_text = "Hold on! Result will shown below."
          my_bar = st.progress(0, text=progress_text)
          for percent_complete in range(100):
              time.sleep(0.02)
              my_bar.progress(percent_complete + 1, text=progress_text) ## to add progress bar untill feature got extracted

          predictions = pmodel.predict(extract_features)
          pred_class = np.argmax(predictions)

          # Map the predicted label index to the actual class label
          class_names = ['Air Conditioner', 'Car Horn', 'Children Playing', 'Dog Bark',
                        'Drilling', 'Engine Idling', 'Gun Shot', 'Jackhammer', 'Siren',
                        'Street Music']
          prediction_class = class_names[pred_class]

          print(prediction_class)

          bold_text = f"<t>{prediction_class}</t>"
          st.write(f'<span style="font-size:20px;">This Uploaded sound clip is {bold_text}</span>', unsafe_allow_html=True)
