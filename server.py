import zmq
import zmq.auth
import time
import os
from zmq.auth.thread import ThreadAuthenticator
from load import load_info

server_name = "odyssey"
## TODO 16: Load server details from info file
server_address = ('127.0.0.1', 10000)
server_open = False
encoding = 'utf-8'

home = os.path.dirname(__file__)
dir_pub = os.path.join(home, 'public_keys')
dir_prv = os.path.join(home, 'private_keys')
dir_info = os.path.join(home, 'infra_info')
dir_data = os.path.join(home, 'data')

## TODO 12: Be able to handle changing values of multiple parameters
def change_data(path, file_name, param, value):
    with open(os.path.join(path, f"{file_name}.data"), 'r') as f:
        lines = []
        for line in f:
            if param in line:
                line_to_change = line
                components = line_to_change.split(' : ')
                new_line = components[0] + ' : ' + value + '\n'
                lines.append(new_line)
                break
            else:
                lines.append(line)

    with open(os.path.join(path, f"{file_name}.data"), 'w') as f:
        for item in lines:
            f.write(item)

def load_data(path, file_name, parameter):
    with open(os.path.join(path, f"{file_name}.data"), 'r') as f:
        for line in f:
            if parameter in line:
                components = line.split(' : ')
                value = components[1]
                break

    return value

def receive_message():
    message = socket.recv_json(0)
    print(f'Message received:\n{message}')

    return message

## TODO 11: Make a list of each type of command and separate the responses to these in separate functions
def send_feedback(message, server_open):
    if message["type"] == "admin":
        response = 'Shutting down the server'
        local_time = time.localtime()
        current_time = f'{local_time[3]:02}:{local_time[4]:02}:{local_time[5]:02} Local Time'
        feedback = {"type": message["type"],
                    "response": response,
                    "time": current_time}
        socket.send_json(feedback, 0)
        print(response)
        server_open = False
    elif message["type"] == "request":
        info = load_info(dir_info, f"{server_name}.info")
        for item in info["parameters"]:
            if item["name"] == message["parameter"]:
                value = load_data(dir_data, server_name, message["parameter"])
                feedback = {"type": message["type"],
                            "parameter": message["parameter"],
                            "value": value}
                socket.send_json(feedback, 0)
                break
    elif message["type"] == "command":
        # command = command.split(":")
        info = load_info(dir_info, f"{server_name}.info")
        for item in info["parameters"]:
            if item["name"] == message["parameter"]:
                change_data(dir_data, server_name, message["parameter"], message["new_value"])
                feedback = {"type": "command",
                            "parameter": message["parameter"],
                            "new value": message["new_value"]}
                socket.send_json(feedback, 0)
                break

    return server_open

# Initialising and starting up the server

context = zmq.Context()
auth = ThreadAuthenticator(context)
auth.start()
auth.allow(server_address[0])
auth.configure_curve(domain='*', location=dir_pub)

socket = context.socket(zmq.REP)
server_file_prv = os.path.join(dir_prv, f"{server_name}.key_secret")
server_pub, server_prv = zmq.auth.load_certificate(server_file_prv)
socket.curve_secretkey = server_prv
socket.curve_publickey = server_pub
socket.curve_server = True
socket.bind(f'tcp://{server_address[0]}:{server_address[1]}')
server_open = True
print(f'I am a WIP server open on {server_address[0]} with port {server_address[1]} ready to talk to friends')

while server_open:
    message = receive_message()
    server_open = send_feedback(message, server_open)

auth.stop()
