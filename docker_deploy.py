import base64
import os
import re
import yaml


def challenge_name_to_alias(chalname):
    slug = chalname.lower().replace(' ', '_')
    return re.sub('[^\w-]+', '', slug)


subfolders = [f.path for f in os.scandir(".") if f.is_dir() and not f.path.startswith("./.")]

compose_file = ["version: '3'", "services:"]

for chal in subfolders:
    with open(os.path.join(chal, "description.yml")) as f:
        data = yaml.safe_load(f)

    chalname = chal.replace("./", "")

    if "port" in data:
        compose_file.append(f'  {challenge_name_to_alias(chal)}:')
        compose_file.append(f'    build:')
        compose_file.append(f'      context: {chal}/server_files')
        compose_file.append(f'    ports:')
        compose_file.append(f'      - "{data["port"]}:{data["port"]}"')
        compose_file.append(f'    restart: always')
        compose_file.append(f'    environment:')
        compose_file.append(f'      - "FLAG={base64.b64decode(data["base64_flag"]).decode()}"')


with open('docker-compose.yml', 'w') as f:
    f.write("\n".join(compose_file))

os.system("docker-compose up --build -d")
