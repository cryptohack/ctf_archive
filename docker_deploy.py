import base64
import hashlib
import os
import random
import re
import yaml

DOCKER_PORT = 1337

port_mappings = {}
used_ports = []
# CH interactive challenge ports reserved for local development
for port in range(11110, 11120):
    used_ports.append(port)
for port in range(13370, 13500):
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

def generate_compose_file():
    compose_file = ["services:"]

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
                compose_file.append(f'          memory: 150M')
                compose_file.append(f'    healthcheck:')
                compose_file.append(f'      test: /bin/bash -c "exec 3<>/dev/tcp/127.0.0.1/1337 && echo 1 >&3 && timeout 15 head -c1 <&3"')
                compose_file.append(f'      interval: 1200s')
                compose_file.append(f'      retries: 2')
                compose_file.append(f'      start_period: {port % 240}s')

    compose_file.append("\n")
    to_write = "\n".join(compose_file)

    return to_write

generated_compose = generate_compose_file()

if __name__ == "__main__":
    with open('docker-compose.yml', 'w') as f:
        f.write(generated_compose)

    os.system("docker compose up --build --remove-orphans -d")
