FROM cybersecnatlab/socaz:ubuntu-jammy AS socaz

FROM sagemath/sagemath:10.6

USER root

RUN mkdir chall
WORKDIR chall

COPY --from=socaz /usr/local/bin/socaz /usr/local/bin/
COPY ./requirements.txt ./
COPY ./chall.sage ./
COPY ./start.sh ./

RUN chmod +x ./start.sh
RUN sage -pip install -r requirements.txt

CMD ["./start.sh"]
