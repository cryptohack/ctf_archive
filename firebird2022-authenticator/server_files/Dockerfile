FROM ctf-archive/python-base:3.12
RUN pip install blake3==1.0.10
COPY *.py ./
USER ctf
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 chall.py"]
