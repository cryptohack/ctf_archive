# Shared base image for Python challenges. Build it before any challenge that uses it:
#   docker build -t ctf-archive/python-base:3.12 base_images/python
# docker_deploy.py does this automatically.
FROM python:3.12-slim-bookworm

RUN apt-get update \
 && apt-get install -y --no-install-recommends socat xinetd \
 && rm -rf /var/lib/apt/lists/* \
 && ln -s /usr/local/bin/python3 /usr/bin/python3

RUN pip install --no-cache-dir pycryptodome==3.23.0 gmpy2==2.3.1

# Unbuffered output so prompts reach players through socat/xinetd pipes,
# and no limit on int <-> str conversion (Python >=3.11 caps it at 4300 digits)
ENV PYTHONUNBUFFERED=1 \
    PYTHONINTMAXSTRDIGITS=0 \
    PIP_NO_CACHE_DIR=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN useradd -m ctf
WORKDIR /app
EXPOSE 1337
