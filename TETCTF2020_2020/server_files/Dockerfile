FROM ctf-archive/python-base:3.12
COPY 2020.py ./
USER ctf
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 2020.py"]
