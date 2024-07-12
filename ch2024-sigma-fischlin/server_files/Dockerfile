FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install socat python3 python3-pip -y

RUN pip install pycryptodome

WORKDIR /app
COPY ./chal.py /app
COPY ./params.py /app

EXPOSE 1337

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 chal.py,nofork,stderr"]
