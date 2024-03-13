import zmq

server_address = ('localhost', 10000)
server_open = False
encoding = 'utf-8'

def receive_command(encoding):
    command = socket.recv_string(0, encoding)
    print(f'Command received: {command}')

    return command

def send_feedback(command, connected, server_open):
    if command == 'echo':
        feedback = command
        socket.send_string(f'Received {feedback}', 0, True, encoding)
    elif command == 'close':
        feedback = 'Closing the connection'
        socket.send_string(f'Received {feedback}', 0, True, encoding)
        connected = False
    elif command == 'shutdown':
        feedback = 'Closing the connection and shutting down the server'
        socket.send_string(f'Received {feedback}', 0, True, encoding)
        print('Shutting down the server')
        connected = False
        server_open = False
    else:
        feedback = command
        socket.send_string(f'Received {feedback}', 0, True, encoding)

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
        command = receive_command(encoding)
        connected, server_open = send_feedback(command, connected, server_open)
