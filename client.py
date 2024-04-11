import zmq
import zmq.auth
import os
from load import load_info, load_server
from pprint import pprint

def send_message(message):
    server_file_pub = os.path.join(dir_pub, f"{server_name}.key")
    server_pub, _ = zmq.auth.load_certificate(server_file_pub)
    socket.curve_serverkey = server_pub
    socket.connect(f'tcp://{server_address[0]}:{server_address[1]}')
    socket.send_json(message, 0)

    return

def receive_feedback():
    feedback = socket.recv_json(0)
    print(f'Server Response:')
    pprint(feedback, indent=4, sort_dicts=False)
    socket.disconnect(f'tcp://{server_address[0]}:{server_address[1]}')

    return

home = os.path.dirname(__file__)
dir_pub = os.path.join(home, 'public_keys')
dir_prv = os.path.join(home, 'private_keys')
dir_info = os.path.join(home, 'infra_info')

print("Which server would you like to interact with?")
server_name = input()
client_name = "apollo"

server_address = load_server(dir_info, server_name)

# Initialising the client
context = zmq.Context()
socket = context.socket(zmq.REQ)

client_file_prv = os.path.join(dir_prv, f"{client_name}.key_secret")
client_pub, client_prv = zmq.auth.load_certificate(client_file_prv)
socket.curve_secretkey = client_prv
socket.curve_publickey = client_pub

print(f'Please enter the command you would like to send to {server_address[0]}:')
user_input = input()

if user_input == "admin":
    print("Please enter the admin command you'd like to enter:")
    command = input()
    if command == "shutdown":
        message = {"type": "admin",
                   "command": "shutdown"}
    else:
        print("You have entered an invalid admin command")
        message = None
elif user_input == "request":
    info = load_info(dir_info, f"{server_name}.info")
    pprint(info["parameters"], indent=4, sort_dicts=False)
    print("\nPlease enter the parameter you would like to request:")
    param = input()
    for item in info["parameters"]:
        if item["name"] == param:
            if item["request"] == "true":
                message = {"type": "request",
                           "parameter": param}
                break
            else:
                message = None
                print("This parameter is not requestable")
                break
elif user_input == "command":
    info = load_info(dir_info, f"{server_name}.info")
    pprint(info["parameters"], indent=4, sort_dicts=False)
    print("\nPlease enter the parameter you would like to command:")
    param = input()
    for item in info["parameters"]:
        if item["name"] == param:
            if item["command"] == "true":
                print("Please enter the value you would like to give this parameter:")
                new_value = input()
                message = {"type": "command",
                           "parameter": param,
                           "new_value": new_value}
                break
else:
    message = None
    print("You have not entered a valid message type")

if message:
    send_message(message)
    receive_feedback()
