FROM ctf-archive/python-base:3.12
COPY challenge.py .
COPY real.xinetd /etc/xinetd.d/real
CMD ["xinetd", "-dontfork"]
