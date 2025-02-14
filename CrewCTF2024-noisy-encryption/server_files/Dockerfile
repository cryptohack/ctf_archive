FROM python:3.10-slim-buster
RUN apt update -y && apt install -y xinetd && apt clean && rm -rf /var/lib/apt/lists/*

RUN useradd -d /home/ctf -m ctf
USER ctf

RUN pip3 install --no-cache-dir sympy==1.13.3

COPY xinetd /etc/xinetd.d/xinetd
COPY server.py /home/ctf/server.py

CMD ["/usr/sbin/xinetd", "-dontfork"]
