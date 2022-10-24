FROM ubuntu:20.04
RUN export DEBIAN_FRONTEND=noninteractive && apt update -y && apt -y install xinetd python3 python3-pip

RUN useradd ctf

WORKDIR /app

RUN chown ctf /app

COPY challenge.py secret.py .
COPY twist.xinetd /etc/xinetd.d/twist


CMD xinetd -dontfork
