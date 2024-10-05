from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from os import environ as env
import warnings
warnings.filterwarnings('ignore')

secret_key = env.get('KEY', 'default_secret_key')
print(f"Using secret key: {secret_key}")
print(secret_key)
app = FastAPI()

class Input(BaseModel):
    X : float 
    key: str

class Output(BaseModel):
    y : float
    slope: float
    intercept: float
    status: str

@app.post("/predict")
def predict(data: Input) -> Output:
    if data.key != secret_key:
        return Output(y = -0.0, slope = -0.0, intercept = -0.0, status = "error")
    X_input = np.array([[data.X]])
    model = joblib.load('pipline_lr_deploy.pkl')
    prediction = model.predict(X_input)
    intercept = model.named_steps['model'].intercept_
    slope = model.named_steps['model'].coef_[0]
    return Output(y = prediction, slope = slope, intercept = intercept, status = "Hurray! You have made it")
