import zmq

server_address = ('localhost', 10000)
server_open = False
encoding = 'utf-8'

def receive_command():
    command = socket.recv_string(0, encoding)
    print(f'Command received: {command}')

    return command

def send_feedback(command, server_open):
    if command == 'echo':
        feedback = command
        socket.send_string(feedback, 0, True, encoding)
    elif command == 'shutdown':
        feedback = 'Shutting down the server'
        socket.send_string(feedback, 0, True, encoding)
        print(feedback)
        server_open = False
    else:
        feedback = command
        socket.send_string(feedback, 0, True, encoding)

    return server_open

# Initialising and starting up the server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f'tcp://{server_address[0]}:{server_address[1]}')
server_open = True
print(f'I am a WIP server open on {server_address[0]} with port {server_address[1]} ready to talk to friends')

while server_open:
    command = receive_command()
    server_open = send_feedback(command, server_open)
