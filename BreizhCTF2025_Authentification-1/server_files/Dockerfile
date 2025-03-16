FROM python:3.12.9-slim

WORKDIR /challenge

COPY authentification-1 /challenge
COPY requirements.txt /challenge

RUN pip install -r requirements.txt
ENV FLAG=BZHCTF{ne_jamais_re-utiliser_le_nonce_e1d6ce70d3d1018c}

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=1337"]
