# syntax=docker/dockerfile:1
   
FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install flask
RUN pip install -U pip setuptools wheel
RUN pip install spacy
RUN pip install waitress
RUN python -m spacy download en_core_web_sm
CMD python aiapps_website/serv.py
