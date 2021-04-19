FROM python:3.7-slim

COPY src/ /app/src/
COPY main.py /app
COPY requirements.txt /app
COPY .env /app
COPY *.json /app

WORKDIR /app


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD exec python -m uvicorn main:app --host=0.0.0.0 --port=8000
