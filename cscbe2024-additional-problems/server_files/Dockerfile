FROM python:3.10

COPY server.py ./server.py
COPY requirements.txt ./requirements.txt

RUN pip install -U -r requirements.txt

ENV FLAG="CSC{let5_m0v3_b00tstr4pp1ng_t0_v1.1}"

EXPOSE 1337

CMD [ "python3", "./server.py" ]
