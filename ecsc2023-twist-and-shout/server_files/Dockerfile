FROM ctf-archive/python-base:3.12
COPY twist_and_shout.py /twist_and_shout.py
COPY twist_and_shout.xinetd /etc/xinetd.d/twist_and_shout
CMD ["xinetd", "-dontfork"]
