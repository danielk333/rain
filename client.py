import zmq

server_address = ('localhost', 10000)
encoding = 'utf-8'

def send_command():
    print(f'Please enter the command you would like to send to {server_address[0]}:')
    command = input()
    socket.connect(f'tcp://{server_address[0]}:{server_address[1]}')
    socket.send_string(command, 0, True, encoding)

    return command

def receive_data(command):
    feedback = socket.recv_string(0, encoding)
    print(f'Server Response: {feedback}')

    return

# Initialising the client and connecting to the server
context = zmq.Context()
socket = context.socket(zmq.REQ)

command = send_command()
receive_data(command)
