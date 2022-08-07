FROM ubuntu:20.04

RUN apt update && apt -y dist-upgrade && apt -y install xinetd python3

RUN useradd ctf

RUN mkdir /app && chown ctf /app
WORKDIR /app

COPY spongebob.py /app/spongebob.py
COPY spongebob.xinetd /etc/xinetd.d/spongebob

RUN chown -R ctf /app

CMD xinetd -dontfork
EXPOSE 55510
