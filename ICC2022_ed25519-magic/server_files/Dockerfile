FROM ubuntu:20.04

RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt -y install xinetd python3 python3-pip
RUN pip install ed25519

RUN useradd ctf

WORKDIR /app
RUN chown ctf /app

COPY chal.py .
COPY magic.xinetd /etc/xinetd.d/magic

CMD xinetd -dontfork
