FROM ctf-archive/python-base:3.12
ENV TERM=linux
COPY src/chall.py src/secret.py src/flag.txt src/banner.txt ./
USER ctf
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 chall.py"]
