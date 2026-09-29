FROM ctf-archive/python-base:3.12
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY authentification-2 ./
USER ctf
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=1337"]
