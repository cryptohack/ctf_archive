FROM ctf-archive/python-base:3.12 AS build
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev
# ed25519 1.5 has no wheels, and its versioneer.py uses configparser APIs removed in Python 3.12
ADD --checksum=sha256:02053ee019ceef0df97294be2d4d5a8fc120fc86e81e08bec1245fc0f9403358 https://files.pythonhosted.org/packages/source/e/ed25519/ed25519-1.5.tar.gz /tmp/
RUN tar xzf /tmp/ed25519-1.5.tar.gz -C /tmp \
 && sed -i 's/SafeConfigParser/ConfigParser/; s/parser.readfp(/parser.read_file(/' /tmp/ed25519-1.5/versioneer.py \
 && pip wheel -w /wheels /tmp/ed25519-1.5

FROM ctf-archive/python-base:3.12
COPY --from=build /wheels /wheels
RUN pip install /wheels/* && rm -rf /wheels
COPY chal.py .
COPY magic.xinetd /etc/xinetd.d/magic
CMD ["xinetd", "-dontfork"]
