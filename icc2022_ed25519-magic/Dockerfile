FROM ubuntu:20.04

RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt -y dist-upgrade && apt -y install xinetd python3 python3-pip
RUN pip install ed25519

COPY flag.txt \
  # add your own test flag if running locally
  flag.txt
COPY chal.py chal.py
COPY magic.xinetd /etc/xinetd.d/magic

EXPOSE 13371

CMD xinetd -dontfork
