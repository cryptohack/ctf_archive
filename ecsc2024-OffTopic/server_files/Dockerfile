FROM cybersecnatlab/socaz:python-3.11-alpine
RUN apk add --no-cache bash

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./chall.py /home/user/chall.py

CMD socaz --timeout 60 --flag-from-env FLAG --bind 1337 --cmd "python3 /home/user/chall.py"
