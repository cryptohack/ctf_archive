FROM ubuntu:20.04

RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt -y dist-upgrade && apt -y install xinetd python3 python3-pip
RUN pip install ed25519

COPY chal.py chal.py
COPY magic.xinetd /etc/xinetd.d/magic

EXPOSE 21012

CMD xinetd -dontfork
