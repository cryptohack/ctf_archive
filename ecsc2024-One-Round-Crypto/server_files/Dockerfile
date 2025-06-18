FROM cybersecnatlab/socaz:python-3.11-alpine

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./chall.py /home/user/chall

CMD socaz --timeout 300 --flag-from-env FLAG --bind 1337 --cmd /home/user/chall
