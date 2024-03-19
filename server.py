import zmq
import zmq.auth
import time
import os
from zmq.auth.thread import ThreadAuthenticator

server_address = ('127.0.0.1', 10000)
server_open = False
encoding = 'utf-8'

home = os.path.dirname(__file__)
dir_pub = os.path.join(home, 'public_keys')
dir_prv = os.path.join(home, 'private_keys')

def receive_command():
    command = socket.recv_string(0, encoding)
    print(f'Command received: {command}')

    return command

def send_feedback(command, server_open):
    if command == 'echo':
        feedback = {"command": command,
                    "response": command}
        socket.send_json(feedback, 0)
    elif command == 'shutdown':
        response = 'Shutting down the server'
        local_time = time.localtime()
        current_time = f'{local_time[3]}:{local_time[4]}:{local_time[5]}'
        feedback = {"command": command,
                    "response": response,
                    "time": current_time}
        socket.send_json(feedback, 0)
        print(response)
        server_open = False
    else:
        feedback = {"command": command,
                    "response": "Invalid command"}
        socket.send_json(feedback, 0)

    return server_open

# Initialising and starting up the server

context = zmq.Context()
auth = ThreadAuthenticator(context)
auth.start()
auth.allow(server_address[0])
auth.configure_curve(domain='*', location=dir_pub)

socket = context.socket(zmq.REP)
server_file_prv = os.path.join(dir_prv, "server.key_secret")
server_pub, server_prv = zmq.auth.load_certificate(server_file_prv)
socket.curve_secretkey = server_prv
socket.curve_publickey = server_pub
socket.curve_server = True
socket.bind(f'tcp://{server_address[0]}:{server_address[1]}')
server_open = True
print(f'I am a WIP server open on {server_address[0]} with port {server_address[1]} ready to talk to friends')

while server_open:
    command = receive_command()
    server_open = send_feedback(command, server_open)

auth.stop()
