import socket
import sys
import time
import zmq

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
encoding = 'utf-8'
max_len = 256
end_char = '\n'

def send_commands(end_char, encoding):
    command = input()
    socket.send_string(command, 0, encoding)
    # data = command + end_char
    # sock.sendall(data.encode(encoding))

    return command

def receive_data(max_len, end_char, encoding):
    data = ''
    while len(data) < max_len:
        data_raw = sock.recv(1)
        if data_raw == end_char.encode(encoding):
            break
        elif len(data_raw) > 0:
            data += data_raw.decode(encoding)

    return data

def interpret(data, command, connected, encoding):
    print(f'Server Response: {data}')
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
    # command = send_commands(end_char, encoding)
    socket.send_string('Test', 0, True, encoding)
    print(socket.recv_string(0, encoding))
    # reception = receive_data(max_len, end_char, encoding)
    # connected = interpret(reception, command, connected)

sys.exit()
