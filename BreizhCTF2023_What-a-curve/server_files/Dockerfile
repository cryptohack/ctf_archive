FROM sagemath/sagemath:9.8 AS builder

USER root

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN useradd -u 666 --home=/challenge -U challenge

WORKDIR /challenge/

COPY chall.sage .

RUN sage --preparse chall.sage && \
    rm chall.sage

USER sage

ENV SOCAT_OPTIONS=",stderr,pty,cfmakeraw,echo=0"

ENTRYPOINT ["sh", "-c", "socat TCP-LISTEN:1337,reuseaddr,fork EXEC:'sage --python chall.sage.py'${SOCAT_OPTIONS}"]
