# syntax=docker/dockerfile:1
   
FROM node:18-alpine
COPY . /app
WORKDIR /app
CMD python /app/serv.py
