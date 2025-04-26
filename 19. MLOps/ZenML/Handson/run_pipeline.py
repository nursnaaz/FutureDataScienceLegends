# run_pipeline.py
#################
from zenml import pipeline, step
import sys
from train_pipeline import ml_pipeline

@pipeline
def execute_pipe(mname: str) -> None:
    ml_pipeline(mname)

if __name__ == "__main__":
    if len(sys.argv) == 2:    
        mname = sys.argv[1]
        execute_pipe(mname)
    else:
        print('Usage: python run_pipeline.py <public data url>')
