FROM python:3.10

COPY server.py ./server.py
COPY requirements.txt ./requirements.txt

RUN pip install -U -r requirements.txt

EXPOSE 1337

CMD [ "python3", "./server.py" ]
