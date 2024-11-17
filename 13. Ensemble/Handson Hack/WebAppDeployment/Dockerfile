FROM python:3.8.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

#ENTRYPOINT ["uvicorn", "mode_app:app", "--host", "0.0.0.0", "--port", "80"]
ENTRYPOINT ["streamlit", "run", "web_app.py", "--server.port=80", "--server.address=0.0.0.0"]

