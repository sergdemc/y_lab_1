FROM python:3.10-slim

COPY requirements.txt /tmp/requirements.txt

RUN apt-get update && apt-get install -y postgresql-client build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
RUN pip install -r /tmp/requirements.txt
RUN adduser --disabled-password app-user
USER app-user

COPY app /app

WORKDIR /app
ENV PYTHONPATH="${PYTHONPATH}:/app"
EXPOSE 8000
