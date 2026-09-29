FROM ctf-archive/python-base:3.12
COPY challenge.py .
COPY twist.xinetd /etc/xinetd.d/twist
CMD ["xinetd", "-dontfork"]
