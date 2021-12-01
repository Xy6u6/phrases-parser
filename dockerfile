FROM python:3.8

#RUN apt install pip

RUN mkdir -p python_apps/phrases-parser

WORKDIR /python_apps/phrases-parser

COPY . /python_apps/phrases-parser
RUN pip install -r requirements.txt

CMD ["python", "main.py"]