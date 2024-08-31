from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    name: str

#Annotations
@app.get("/hi")
def helloworld():
    return "Hello I am learning FastAPI with noor in inceptez"


@app.post("/hi")
def helloworld():
    return "Hello I am learning FastAPI"
    
@app.get("/person/{person}")
def great_user_get(person):
    return {"Hey Hi Welcome ": person}


@app.post("/person/")
def great_user_post(data: InputData):
    return {"Hey Hi Welcome ": data.name}

# Run the server
# uvicorn main:app --reload