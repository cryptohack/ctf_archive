FROM sagemath/sagemath:latest

USER root
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt -y dist-upgrade && apt -y install xinetd

RUN sage -pip install pycryptodome

RUN mkdir /app && chown sage /app
WORKDIR /app

COPY kernel_searcher.sage /app/kernel_searcher.sage
COPY entry.sh /app/entry.sh
COPY kernel_searcher.xinetd /etc/xinetd.d/kernel_searcher

RUN chown -R sage /app
RUN chmod +x entry.sh

ENTRYPOINT ["/usr/sbin/xinetd", "-dontfork"]

EXPOSE 1337
