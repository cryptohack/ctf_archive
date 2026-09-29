FROM ctf-archive/python-base:3.12
COPY chal.py params.py ./
USER ctf
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 chal.py,nofork,stderr"]
