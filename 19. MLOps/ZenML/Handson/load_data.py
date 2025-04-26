# load_data.py
#################

from zenml import step
import pandas as pd

@step
def ingest_data(mname: str)  -> pd.DataFrame:
    #df_pth = "https://raw.githubusercontent.com/nursnaaz/FutureDataScienceLegends/refs/heads/main/04.%20Linear%20Regression/Model%20Deployement/FastAPI/linear_regression_data.csv"
    df_pth = mname
    lcl_pth = "./IngestedData.csv"
    df = pd.read_csv(df_pth)
    df.to_csv(lcl_pth, index=False)

    return df


