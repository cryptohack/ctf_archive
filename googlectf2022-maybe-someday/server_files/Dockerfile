FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv socat
RUN python3 -m venv /home/ctfuser/venv

RUN /home/ctfuser/venv/bin/pip uninstall crypto
RUN /home/ctfuser/venv/bin/pip uninstall pycryptodome
RUN /home/ctfuser/venv/bin/pip install pycryptodome

WORKDIR /home/ctfuser
COPY *.py /home/ctfuser/
ENV FLAG CTF{p4dd1n9_or4cl3_w1th_h0mom0rph1c_pr0p3r7y_c0m6in3d_in7o_a_w31rd_m47h_puzz1e}
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 /home/ctfuser/venv/bin/python3 /home/ctfuser/chall.py"
