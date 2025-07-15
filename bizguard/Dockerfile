FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-setuptools \
    python3-gevent \
    build-essential \
    libssl-dev \
    libpq-dev \
    libffi-dev \
    gcc \
    libevent-dev \
    vim \
    curl \
    iputils-ping \
    libjpeg-dev
WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app
