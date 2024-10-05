FROM --platform=linux/amd64 python:3.8.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $PORT

CMD exec uvicorn model_app:app --port=$PORT --host=0.0.0.0 


#Running docker local build and run

#docker build -t fastapi-lr:1.0 .

#docker run -p 80:80 fastapi-lr:1.0 

# Docker push in docker hub

#docker login

#docker tag fastapi-lr:1.0 nursnaaz/fastapi-lr:1.0

#docker push nursnaaz/fastapi-lr:1.0 

#docker pull nursnaaz/fastapi-lr
