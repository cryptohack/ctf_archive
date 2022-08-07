import base64
import hashlib
import os
import random
import re
import yaml

DOCKER_PORT = 1337

used_ports = []
# CH challenge ports for local development
for port in range(13370, 13401):
    used_ports.append(port)


def challenge_name_to_alias(chalname):
    slug = chalname.lower().replace(' ', '_')
    return re.sub('[^\w-]+', '', slug)


# Generate deterministic "random" port for challenge
def get_free_port(chal_alias):
    port = None
    while not port:
        hashed = hashlib.sha256(chal_alias.encode()).digest()
        port = int.from_bytes(hashed, 'big') % 256**2
        while port in used_ports or port < 1024:
            port += 1
            if port >= 256**2:
                port = 1024
    return port


def get_subfolders(directory):
    subfolders = []
    for f in os.scandir(directory):
        if f.is_dir() and not f.path.startswith("./."):
            subfolders.append(f.path.replace("./", ""))
    return subfolders

compose_file = ["version: '3'", "services:"]

for chal in get_subfolders("."):
    with open(os.path.join(chal, "description.yml")) as f:
        data = yaml.safe_load(f)

    chal_alias = challenge_name_to_alias(chal)

    if os.path.isdir(os.path.join(chal, "server_files")): # is dynamic chal
        port = get_free_port(chal_alias)

        compose_file.append(f'  {chal_alias}:')
        compose_file.append(f'    build:')
        compose_file.append(f'      context: {chal}/server_files')
        compose_file.append(f'    ports:')
        compose_file.append(f'      - {port}:{DOCKER_PORT}')
        compose_file.append(f'    restart: always')
        compose_file.append(f'    environment:')
        compose_file.append(f'      - "FLAG={base64.b64decode(data["base64_flag"]).decode()}"')

compose_file.append("\n")
to_write = "\n".join(compose_file)

print(to_write)
with open('docker-compose.yml', 'w') as f:
    f.write(to_write)

os.system("docker-compose up --build -d")
