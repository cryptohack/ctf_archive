FROM cybersecnatlab/socaz:python-3.11-alpine AS socaz

FROM sagemath/sagemath:10.6

USER root

RUN mkdir chall
WORKDIR chall

COPY --from=socaz /usr/local/bin/socaz /usr/local/bin/
COPY ./chall.sage ./
COPY ./start.sh ./

RUN chmod +x ./start.sh

CMD ["./start.sh"]
