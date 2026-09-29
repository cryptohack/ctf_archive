FROM ctf-archive/python-base:3.12
COPY source.py .
COPY ctf.xinetd /etc/xinetd.d/ctf
CMD ["xinetd", "-dontfork"]
