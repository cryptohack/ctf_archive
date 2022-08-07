FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv socat
RUN python3 -m venv /home/ctfuser/venv

RUN /home/ctfuser/venv/bin/pip uninstall crypto
RUN /home/ctfuser/venv/bin/pip uninstall pycryptodome
RUN /home/ctfuser/venv/bin/pip install pycryptodome gmpy2

WORKDIR /home/ctfuser
COPY *.py /home/ctfuser/
ENV FLAG firebird{wh3n_1n_d0ub7_u5e_latt111c3_r3duc71110n_4lg0r111thm}
CMD socat TCP-LISTEN:19616,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 /home/ctfuser/venv/bin/python3 /home/ctfuser/chall.py"
