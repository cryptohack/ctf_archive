FROM python:3.10-slim-buster
RUN apt update -y && apt install -y xinetd && apt clean && rm -rf /var/lib/apt/lists/*

RUN useradd -d /home/ctf -m ctf
USER ctf

RUN pip3 install --no-cache-dir pycryptodome==3.16.0 gmpy2==2.1.5

COPY server.py /home/ctf/server.py
COPY xinetd /etc/xinetd.d/xinetd

CMD ["/usr/sbin/xinetd", "-dontfork"]
