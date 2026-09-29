FROM ctf-archive/python-base:3.12
RUN pip install numpy==2.5.3
COPY challenge.py .
COPY numpymt.xinetd /etc/xinetd.d/numpymt
CMD ["xinetd", "-dontfork"]
