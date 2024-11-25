# create a api endpoints using fastapi
#!pip install uvicorn
#!pip install fastapi


#load libraries
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib

import warnings
warnings.filterwarnings('ignore')

# create object the FastAPI
app = FastAPI()

# to pass the input features
class Input(BaseModel):
    department:object
    region                   : object
    education                : object
    gender                   : object
    recruitment_channel      : object
    no_of_trainings           : int
    age                       : int
    previous_year_rating    : float
    length_of_service         : int
    KPIs_met_80             : int
    awards_won               : int
    avg_training_score        : int


# to pass the output
class Output(BaseModel):
    is_promoted : int

'''
# addition of two columns and return the value in the third column
def add(data: Input) -> Output:
    Output.col3 = data.col1 + data.col2
'''

@app.post("/predict")
def predict(data: Input) -> Output:
    
    X_input = pd.DataFrame([[data.department,data.region,data.education,data.gender,data.recruitment_channel,data.no_of_trainings,
data.age,data.previous_year_rating,data.length_of_service,data.KPIs_met_80,data.awards_won,data.avg_training_score]]
)
    X_input.columns = ['department', 'region', 'education', 'gender', 'recruitment_channel', 'no_of_trainings', 'age', 
'previous_year_rating','length_of_service', 'KPIs_met >80%', 'awards_won?','avg_training_score']
    
    # load the model
    model = joblib.load('promote_pipeline_model.pkl')

    # predict using model
    prediction = model.predict(X_input)

    # result/output
    return Output(is_promoted = prediction)

