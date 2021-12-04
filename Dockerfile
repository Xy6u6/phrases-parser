FROM python:3.8

#RUN apt install pip

RUN mkdir -p app/
WORKDIR /app

COPY ./src .
COPY requirements.txt .
COPY ./tmp/gcp_acc.json ./tmp/

RUN pip install -r requirements.txt


CMD ["python", "main.py"]
