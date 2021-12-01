FROM python:3.8

#RUN apt install pip

RUN mkdir -p app/
RUN mkdir -p tmp/parser
WORKDIR /app

COPY ./src .
COPY requirements.txt .


RUN pip install -r requirements.txt


CMD ["python", "main.py"]
