import os
import time

from authenticate import load_server, setup_publish
from actions import load_data
from decompose import load_groups

home = os.path.dirname(__file__)
home = home.removesuffix("/src/rain")
dir_pub = os.path.join(home, "public_keys")
dir_prv = os.path.join(home, "private_keys")
dir_info = os.path.join(home, "infra_info")
dir_data = os.path.join(home, "data")

server_name = "odyssey"
server_address = load_server(dir_info, server_name)
server_open = False

possible_sub = []
groups = load_groups(dir_info, server_name)
for group in groups:
    for iter in range(len(group["parameters"])):
        if group["parameters"][iter]["subscribe"] == "true":
            possible_sub.append(group["parameters"][iter]["name"])

auth, socket, server_open = setup_publish(server_name, server_address, dir_pub, dir_prv)

while server_open:
    time.sleep(2)
    for param in possible_sub:
        value = load_data(dir_data, server_name, param)
        response = {"type": "sub",
                    "parameters": param,
                    "value": value}
        socket.send_string(f"{param}: {value}")
