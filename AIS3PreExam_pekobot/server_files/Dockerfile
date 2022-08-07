FROM python:3.10

RUN apt-get update && apt-get install socat -y
RUN pip install pycryptodome

WORKDIR /app
COPY elliptic_curve.py .
COPY server.py .

RUN useradd -ms /bin/bash ctf
USER ctf
EXPOSE 1337
ENTRYPOINT ["socat", "TCP-LISTEN:1337,fork,reuseaddr", "EXEC:'python server.py',stderr"]
