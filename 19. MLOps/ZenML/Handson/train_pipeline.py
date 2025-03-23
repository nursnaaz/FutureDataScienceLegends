# train_pipeline.py
#################

from zenml import pipeline
from load_data import ingest_data
from train_model import train_model

@pipeline
def ml_pipeline(mname: str):
    dataset = ingest_data(mname)
    model = train_model(dataset)
