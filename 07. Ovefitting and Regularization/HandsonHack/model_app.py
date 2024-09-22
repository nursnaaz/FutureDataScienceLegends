#import necessary libraries
#!pip install fastapi
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()


class Input(BaseModel):
    CONSOLE: object
    YEAR: int
    CATEGORY: object
    PUBLISHER: object
    RATING: object
    CRITICS_POINTS: float
    USER_POINTS: float

class Output(BaseModel):
    SalesInMillions: float

@app.post("/predict")

def predict2(data: Input) -> Output:
    # input
    # dataframe thru list
    X_input = pd.DataFrame([[data.CONSOLE, data.YEAR, data.CATEGORY, data.PUBLISHER, data.RATING, data.CRITICS_POINTS, data.USER_POINTS]])
    X_input.columns = ['CONSOLE', 'YEAR', 'CATEGORY', 'PUBLISHER', 'RATING', 'CRITICS_POINTS', 'USER_POINTS']

    # dataframe thru dictionary (valid)
    #X_input = pd.DataFrame([{'CONSOLE':  data.CONSOLE,'YEAR':  data.YEAR,'CATEGORY':  data.CATEGORY,'PUBLISHER':  data.PUBLISHER,'RATING':  data.RATING,'CRITICS_POINTS':  data.CRITICS_POINTS,'USER_POINTS':  data.USER_POINTS}])
   
    print(X_input)
    # load the model
    model = joblib.load('vgsales_pipeline_model.pkl')

    #predict using the model
    prediction = model.predict(X_input)

    # output
    return Output(SalesInMillions = prediction)


'''
{
  "CONSOLE": "ds",
  "YEAR": 2008,
  "CATEGORY": "role-playing",
  "PUBLISHER": "Nintendo",
  "RATING": "E",
  "CRITICS_POINTS": 2.83,
  "USER_POINTS": 0.30
}
{
  "CONSOLE": "ds",
  "YEAR": 2008,
  "CATEGORY": "role-playing",
  "PUBLISHER": "Nintendo",
  "RATING": "E",
  "CRITICS_POINTS": 2.833333333,
  "USER_POINTS": 0.303703704
}

ID,CONSOLE,YEAR,CATEGORY,PUBLISHER,RATING,CRITICS_POINTS,USER_POINTS,SalesInMillions
2860,ds,2008,role-playing,Nintendo,E,2.8333333333333335,0.3037037037037037,1.7792573645377137

def predict(data: Input) -> Output:
   X_input = pd.DataFrame([{'CONSOLE':  data.CONSOLE,'YEAR':  data.YEAR,'CATEGORY':  data.CATEGORY,'PUBLISHER':  data.PUBLISHER,'RATING':  data.RATING,'CRITICS_POINTS':  data.CRITICS_POINTS,'USER_POINTS':  data.USER_POINTS}])
   print(X_input)
   return Output(SalesInMillions = 222)

curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "CONSOLE": "ds",
  "YEAR": 2010,
  "CATEGORY": "role-playing",
  "PUBLISHER": "Nintendo",
  "RATING": "E",
  "CRITICS_POINTS": 2.83,
  "USER_POINTS": 0.30
}'   

# command to run in terminal: uvicorn model_app:app --reload
'''
