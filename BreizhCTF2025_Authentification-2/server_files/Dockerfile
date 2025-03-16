FROM python:3.12.9-slim

WORKDIR /challenge

COPY authentification-2 /challenge
COPY requirements.txt /challenge

RUN pip install -r requirements.txt
ENV FLAG=BZHCTF{encore_et_toujours_de_la_faute_du_stagiaire_350cd55e8bf628ea}

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=1337"]
