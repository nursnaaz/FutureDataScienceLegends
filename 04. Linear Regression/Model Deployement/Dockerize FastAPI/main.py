from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

class Input(BaseModel):
    X : float

class Output(BaseModel):
    y : float
    slope: float
    intercept: float

@app.post("/predict")
def predict(data: Input) -> Output:
    X_input = np.array([[data.X]])
    model = joblib.load('pipline_lr_deploy.pkl')
    prediction = model.predict(X_input)
    intercept = model.named_steps['model'].intercept_
    slope = model.named_steps['model'].coef_[0]
    return Output(y = prediction, slope = slope, intercept = intercept)
    
    