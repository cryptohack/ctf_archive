FROM sagemath/sagemath:9.7
RUN sudo apt update -y && sudo apt install -y xinetd && sudo apt clean && sudo rm -rf /var/lib/apt/lists/*

RUN sage -pip install --no-cache-dir pycryptodome==3.16.0

COPY server.sage /home/sage/server.sage
COPY xinetd /etc/xinetd.d/xinetd

CMD ["/usr/sbin/xinetd", "-dontfork"]
