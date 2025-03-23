
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
from zenml import step
#from zenml.client import Client
import mlflow
#experiment_tracker = Client().active_stack.experiment_tracker
#print(experiment_tracker.name)
#@step(enable_cache=False, experiment_tracker=experiment_tracker.name)
@step
def train_model(data: pd.DataFrame) -> pd.DataFrame:
    X = data[['X']]
    y = data[['y']]
    X_train, X_test, y_train, y_test = train_test_split(X,y,train_size=0.7, random_state=42)
    model = LinearRegression()
    model.fit(X_train,y_train)
    y_pred = pd.DataFrame(model.predict(X_test))
    rmse = root_mean_squared_error(y_test, y_pred)
    mlflow.log_metric("rmse",rmse)
    mlflow.sklearn.log_model(model,"mymodel")
    #print(y_pred, type(y_pred))
    return y_pred