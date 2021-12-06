FROM python:3.8

#RUN apt install pip

RUN mkdir -p app/
WORKDIR /app

COPY ./src .
COPY requirements.txt .
COPY ./red-parity-333415-f0c7b39b3433.json ./tmp/gcp-acc.json

RUN pip install -r requirements.txt


CMD ["python", "main.py"]
