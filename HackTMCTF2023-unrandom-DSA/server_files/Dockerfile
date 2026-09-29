FROM ctf-archive/python-base:3.12
RUN pip install pycryptodome==3.16.0
COPY xinetd /etc/xinetd.d/xinetd
COPY server.py /home/ctf/server.py
USER ctf
CMD ["xinetd", "-dontfork"]
