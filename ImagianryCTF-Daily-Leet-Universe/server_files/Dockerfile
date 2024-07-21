FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install socat -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY server.py .

RUN useradd -ms /bin/bash ctf
USER ctf
EXPOSE 1337
ENTRYPOINT ["socat", "TCP-LISTEN:1337,fork,reuseaddr", "EXEC:'python server.py',stderr"]
