FROM python:latest

RUN mkdir /app
WORKDIR /app

COPY . /app

COPY requirements.txt  /app

RUN pip install --no-cache-dir -r requirements.txt
RUN wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh