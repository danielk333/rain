import sys
import zmq

server_address = ('localhost', 10000)
encoding = 'utf-8'

def send_commands(encoding):
    command = input()
    socket.send_string(command, 0, True, encoding)

    return command

def receive_data(command, connected, encoding):
    feedback = socket.recv_string(0, encoding)
    print(f'Server Response: {feedback}')
    if command == 'close':
        connected = False
    if command == 'shutdown':
        connected = False

    return connected

# Initialising the client and connecting to the server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(f'tcp://{server_address[0]}:{server_address[1]}')
print(f'Connecting to {server_address[0]} on port {server_address[1]}')
connected = True

while connected:
    command = send_commands(encoding)
    connected = receive_data(command, connected, encoding)

sys.exit()
