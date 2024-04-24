import os
import json


def load_info(path, file_name):
    with open(os.path.join(path, file_name), "r") as f:
        data = f.read()
        # TODO 9: Also find the end of the parameters
        for char in range(len(data)):
            if data[char] == '{':
                if data[char+1] == '\n':
                    data = data[char:len(data)]
                    break
        info = json.loads(data)
    return info


def load_server(path, server_name):
    server_address = []
    with open(os.path.join(path, f"{server_name}.info"), "r") as f:
        for line in f:
            if "Server" in line:
                ip_address = line.split(': ')[1]
                ip_address = ip_address[0:len(ip_address)-1]
                server_address.append(ip_address)
            elif "Port" in line:
                port = line.split(': ')[1]
                port = port[0:len(port)-1]
                server_address.append(port)

    return server_address
