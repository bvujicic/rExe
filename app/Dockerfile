FROM python:latest

RUN apt-get update && apt-get install -y gettext --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app /static /src /var/log
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --src /src --upgrade

COPY . /app

