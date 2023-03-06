# syntax=docker/dockerfile:1
   
FROM python:latest
COPY . .
CMD python ./aiapps_website/serv.py
