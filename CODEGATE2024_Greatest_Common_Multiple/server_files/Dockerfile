FROM ubuntu:22.04@sha256:965fbcae990b0467ed5657caceaec165018ef44a4d2d46c7cdea80a9dff0d1ea

RUN apt update
RUN apt-get install -y socat python3 python3-pip

ENV TERM=linux

RUN pip install pycryptodome

COPY ./src/chall.py /
COPY ./src/flag.txt /
COPY ./src/banner.txt /
COPY ./src/secret.py /

CMD socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"python3 /chall.py"

EXPOSE 9999