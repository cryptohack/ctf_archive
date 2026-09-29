FROM python:3.12.9-slim

WORKDIR /challenge

COPY authentification-1 /challenge
COPY requirements.txt /challenge

RUN pip install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=1337"]
