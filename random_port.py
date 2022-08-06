import os
import random
import yaml

used_ports = []
for i in range(13370, 13400):
    # CH challenge ports for local development
    used_ports.append(i)

subfolders = [f.path for f in os.scandir(".") if f.is_dir() and not f.path.startswith("./.")]
for chal in subfolders:
    with open(os.path.join(chal, "description.yml")) as f:
        data = yaml.safe_load(f)
    if "port" in data:
        used_ports.append(int(data["port"]))

port = None
while not port or port in used_ports:
    port = random.randint(1024, 65535)

print(port)
