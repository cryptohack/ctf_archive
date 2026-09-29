FROM ctf-archive/python-base:3.12
COPY challenge.py .
COPY chaos.xinetd /etc/xinetd.d/chaos
CMD ["xinetd", "-dontfork"]
