FROM ctf-archive/python-base:3.12
RUN pip install mmh3==5.3.0
COPY source.py .
COPY ctf.xinetd /etc/xinetd.d/ctf
CMD ["xinetd", "-dontfork"]
