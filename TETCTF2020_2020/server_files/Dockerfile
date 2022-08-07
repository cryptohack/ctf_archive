FROM python:3.9
WORKDIR /app

RUN useradd -m chall
RUN apt update
RUN apt install -y socat

COPY 2020.py .

RUN chmod +r 2020.py

USER chall

ENTRYPOINT socat tcp-l:2020,fork,reuseaddr exec:"python 2020.py"