FROM cache.ecsc2024.it/cybersecnatlab/socaz:ubuntu-jammy AS socaz

FROM cache.ecsc2024.it/sagemath/sagemath@sha256:a7c4f3d0536aa1e93c106ac31ea2ae035299f9afcfdcb4a549c396374fb926a9

USER root

RUN mkdir chall
WORKDIR chall

COPY --from=socaz /usr/local/bin/socaz /usr/local/bin/
COPY ./requirements.txt ./
COPY ./rsatogether.sage ./
COPY ./start.sh ./

RUN chmod +x ./start.sh
RUN sage -pip install -r requirements.txt

CMD ["./start.sh"]

