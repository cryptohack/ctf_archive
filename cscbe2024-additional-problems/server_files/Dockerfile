FROM ctf-archive/python-base:3.12 AS build
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev
COPY requirements.txt ./
RUN pip wheel -w /wheels -r requirements.txt

FROM ctf-archive/python-base:3.12
COPY --from=build /wheels /wheels
RUN pip install /wheels/* && rm -rf /wheels
COPY server.py ./
USER ctf
CMD ["python3", "server.py"]
