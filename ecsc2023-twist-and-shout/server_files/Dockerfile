FROM ubuntu:20.04

RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt -y dist-upgrade && apt -y install xinetd python3 python3-pip

COPY twist_and_shout.py twist_and_shout.py
COPY twist_and_shout.xinetd /etc/xinetd.d/twist_and_shout


EXPOSE 1337

CMD xinetd -dontfork
