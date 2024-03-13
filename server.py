import socket
import time
import zmq

server_address = ('localhost', 10000)
server_open = False
encoding = 'utf-8'
max_len = 256
end_char = '\n'

def receive_command(max_len, end_char, encoding, dt, timeout):
    command = ''
    while len(command) < max_len:
        data_raw = connection.recv(1)
        if data_raw == end_char.encode(encoding):
            break
        elif len(data_raw) > 0:
            command += data_raw.decode(encoding)

    print(command)
    return command

def send_feedback(command, connected, server_open):
    if command == 'echo':
        feedback = command
        feedback += end_char
        connection.sendall(feedback.encode(encoding))
    if command == 'close':
        feedback = 'Closing the connection'
        feedback += end_char
        connection.sendall(feedback.encode(encoding))
        connected = False
    if command == 'shutdown':
        feedback = 'Closing the connection and shutting down the server'
        feedback += end_char
        connection.sendall(feedback.encode(encoding))
        print('Shutting down the server')
        connected = False
        server_open = False
        connection.close()

    return connected, server_open

# Initialising and starting up the server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f'tcp://{server_address[0]}:{server_address[1]}')
server_open = True
print(f'Server started on {server_address[0]} with port {server_address[1]}')

while server_open:
    print("I am a WIP server ready to talk to a friend")
    # Add something that check whether a connection has been made
    connected = True

    while connected == True:
        # command = receive_command(max_len, end_char, encoding)
        command = socket.recv_string(0, encoding)
        print(command)
        socket.send_string('Received', 0, True, encoding)
        time.sleep(2)
        # connected, server_open = send_feedback(command, connected, server_open)
