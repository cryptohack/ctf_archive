FROM ctf-archive/python-base:3.12
WORKDIR /ctf
COPY key_recovery.py .
COPY key_recovery.xinetd /etc/xinetd.d/key_recovery
CMD ["xinetd", "-dontfork"]
