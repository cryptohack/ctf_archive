import base64
import hashlib
import os
import random
import re
import yaml

DOCKER_PORT = 1337

port_mappings = {}
used_ports = []
# CH challenge ports for local development
for port in range(13370, 13401):
    used_ports.append(port)


def challenge_name_to_alias(ctf, year, name):
    alias = f"{name}-{ctf}{year}"
    alias = alias.lower().replace(' ', '_')
    return re.sub('[^\w-]+', '', alias)[:29].strip("_")


# Generate deterministic "random" port for challenge
def get_free_port(chal_alias):
    hashed = hashlib.sha256(chal_alias.encode()).digest()
    port = int.from_bytes(hashed, 'big') % 256**2
    while port in used_ports or port < 1024:
        port += 1
        if port >= 256**2:
            port = 1024
    port_mappings[chal_alias] = port
    used_ports.append(port)
    return port


def get_subfolders(directory):
    subfolders = []
    for f in os.scandir(directory):
        if f.is_dir():
            part = os.path.basename(os.path.normpath(f))
            if not part.startswith("."):
                subfolders.append(part)
    return subfolders

compose_file = ["version: '3'", "services:"]

cwd = os.path.dirname(os.path.realpath(__file__))
for chal in get_subfolders(cwd):
    if os.path.isfile(os.path.join(cwd, chal, "description.yml")):
        with open(os.path.join(cwd, chal, "description.yml")) as f:
            data = yaml.safe_load(f)

        chal_alias = challenge_name_to_alias(data['original_ctf'], data['year'], data['name'])
        print(f"Adding {chal_alias}...")

        if os.path.isdir(os.path.join(cwd, chal, "server_files")): # is dynamic chal
            port = get_free_port(chal_alias)

            compose_file.append(f'  {chal_alias}:')
            compose_file.append(f'    build:')
            compose_file.append(f'      context: {chal}/server_files')
            compose_file.append(f'    ports:')
            compose_file.append(f'      - {port}:{DOCKER_PORT}')
            compose_file.append(f'    restart: always')
            compose_file.append(f'    environment:')
            compose_file.append(f'      - "FLAG={base64.b64decode(data["base64_flag"]).decode().strip()}"')
            compose_file.append(f'    deploy:')
            compose_file.append(f'      resources:')
            compose_file.append(f'        limits:')
            compose_file.append(f'          cpus: "0.3"')
            compose_file.append(f'          memory: 50M')


if __name__ == "__main__":
    compose_file.append("\n")
    to_write = "\n".join(compose_file)

    print(to_write)
    with open('docker-compose.yml', 'w') as f:
        f.write(to_write)

    os.system("docker-compose build --parallel")
    os.system("docker-compose --compatibility up --remove-orphans -d")
