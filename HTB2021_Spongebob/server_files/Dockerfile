FROM ctf-archive/python-base:3.12
COPY spongebob.py .
COPY spongebob.xinetd /etc/xinetd.d/spongebob
CMD ["xinetd", "-dontfork"]
