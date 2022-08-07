FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv socat
RUN python3 -m venv /home/ctfuser/venv

RUN /home/ctfuser/venv/bin/pip uninstall crypto
RUN /home/ctfuser/venv/bin/pip uninstall pycryptodome
RUN /home/ctfuser/venv/bin/pip install pycryptodome blake3

WORKDIR /home/ctfuser
COPY *.py /home/ctfuser/
ENV FLAG firebird{y0u_d0n7_n33d_t0_pr3c0mpu73_3very7h1n9_4nyw4y}
CMD socat TCP-LISTEN:19615,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 /home/ctfuser/venv/bin/python3 /home/ctfuser/chall.py"
