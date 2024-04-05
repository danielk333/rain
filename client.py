import zmq
import zmq.auth
import os
from load import load_info
from pprint import pprint

server_name = "odyssey"

server_address = ('127.0.0.1', 10000)
encoding = 'utf-8'
home = os.path.dirname(__file__)

dir_pub = os.path.join(home, 'public_keys')
dir_prv = os.path.join(home, 'private_keys')
dir_info = os.path.join(home, 'infra_info')

def send_command():
    print(f'Please enter the command you would like to send to {server_address[0]}:')
    command = input()
    if command == "request":
        info = load_info(dir_info, f"{server_name}.info")
        pprint(info["parameters"], indent=4, sort_dicts=False)
        print("\nPlease enter the parameter you would like to request\n")
        param = input()
        for item in info["parameters"]:
            if item["name"] == param:
                command = param
    server_file_pub = os.path.join(dir_pub, f"{server_name}.key")
    server_pub, _ = zmq.auth.load_certificate(server_file_pub)
    socket.curve_serverkey = server_pub
    socket.connect(f'tcp://{server_address[0]}:{server_address[1]}')
    socket.send_string(command, 0, True, encoding)

    return command

def receive_data(command):
    feedback = socket.recv_json(0)
    print(f'Server Response:')
    print('{')
    for item in feedback:
        print(f'    {item}: {feedback[item]}')
    print('}')
    socket.disconnect(f'tcp://{server_address[0]}:{server_address[1]}')

    return

# Initialising the client
context = zmq.Context()
socket = context.socket(zmq.REQ)

client_file_prv = os.path.join(dir_prv, "apollo.key_secret")
client_pub, client_prv = zmq.auth.load_certificate(client_file_prv)
socket.curve_secretkey = client_prv
socket.curve_publickey = client_pub

command = send_command()
receive_data(command)
