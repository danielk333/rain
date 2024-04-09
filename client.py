import zmq
import zmq.auth
import os
from load import load_info
from pprint import pprint

## TODO 8: Ask user what server to interact with
server_name = "odyssey"
client_name = "apollo"

## TODO 7: Add server details to the info file
server_address = ('127.0.0.1', 10000)
encoding = 'utf-8'

home = os.path.dirname(__file__)
dir_pub = os.path.join(home, 'public_keys')
dir_prv = os.path.join(home, 'private_keys')
dir_info = os.path.join(home, 'infra_info')

def send_command(command):
    server_file_pub = os.path.join(dir_pub, f"{server_name}.key")
    server_pub, _ = zmq.auth.load_certificate(server_file_pub)
    socket.curve_serverkey = server_pub
    socket.connect(f'tcp://{server_address[0]}:{server_address[1]}')
    socket.send_string(command, 0, True, encoding)

    return

def receive_data(command):
    feedback = socket.recv_json(0)
    ## TODO 6: Replace this with pprint?
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

client_file_prv = os.path.join(dir_prv, f"{client_name}.key_secret")
client_pub, client_prv = zmq.auth.load_certificate(client_file_prv)
socket.curve_secretkey = client_prv
socket.curve_publickey = client_pub

print(f'Please enter the command you would like to send to {server_address[0]}:')
user_input = input()

if user_input == "request":
    info = load_info(dir_info, f"{server_name}.info")
    pprint(info["parameters"], indent=4, sort_dicts=False)
    print("\nPlease enter the parameter you would like to request")
    param = input()
    for item in info["parameters"]:
        if item["name"] == param:
            ## TODO 15: Fix the request and command status checks
            if info["request"] == "true":
                command = param
                break
            else:
                command = None
                print("This parameter is not requestable")
                break
elif user_input == "command":
    info = load_info(dir_info, f"{server_name}.info")
    pprint(info["parameters"], indent=4, sort_dicts=False)
    print("\nPlease enter the parameter you would like to command")
    param = input()
    print("Enter the value you would like to give this parameter")
    new_value = input()
    command = param + ":" + new_value
else:
    command = user_input

if command:
    send_command(command)
    receive_data(command)
