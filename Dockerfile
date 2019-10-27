FROM python:3.6

COPY . /app

WORKDIR /app

CMD python spoofident.py
