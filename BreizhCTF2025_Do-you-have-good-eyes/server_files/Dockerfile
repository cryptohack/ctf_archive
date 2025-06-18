FROM sagemath/sagemath:10.6 AS builder

USER root

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN useradd -u 666 --home=/challenge -U challenge

WORKDIR /challenge/

COPY do-you-have-good-eyes/ .
ENV FLAG="BZHCTF{trop_de_structure_tue_la_structure_79c145775373a9b8}"

RUN sage --preparse chal.sage && \
    rm chal.sage

USER sage

ENV SOCAT_OPTIONS=",stderr,pty,cfmakeraw,echo=0"

ENTRYPOINT ["sh", "-c", "socat TCP-LISTEN:1337,reuseaddr,fork EXEC:'sage --python chal.sage.py'${SOCAT_OPTIONS}"]

