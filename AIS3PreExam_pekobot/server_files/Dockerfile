FROM ctf-archive/python-base:3.12
COPY elliptic_curve.py server.py ./
USER ctf
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 server.py,stderr"]
