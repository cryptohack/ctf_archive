FROM python:3

RUN apt-get update && apt-get install -y \
  xinetd \
  && rm -rf /var/lib/apt/lists/*

RUN useradd ctf
RUN mkdir /ctf
WORKDIR /ctf

RUN chown ctf /ctf

COPY key_recovery.xinetd /etc/xinetd.d/key_recovery
COPY key_recovery.py .

CMD xinetd -dontfork