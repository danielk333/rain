import socket
import time

server_address = ('localhost', 10000)
server_open = False
encoding = 'utf-8'
timeout = 5.0
max_len = 256
t0 = time.time()
dt = 0.0
end_char = '\n'

def receive_command(max_len, end_char, encoding, dt, timeout):
    command = ''
    t0 = time.time()
    while len(command) < max_len:
        data_raw = connection.recv(1)
        if data_raw == end_char.encode(encoding):
            break
        elif len(data_raw) > 0:
            command += data_raw.decode(encoding)
        else:
            dt = time.time() - t0
            if dt >= timeout:
                break

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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen()
server_open = True
print(f'Server started on {server_address[0]} with port {server_address[1]}')

while server_open:
    print("I am a WIP server waiting for a friend")
    connection, client_address = sock.accept()
    print(f'I have found a friend at {client_address}!')
    connected = True

    while connected == True:
        command = receive_command(max_len, end_char, encoding, dt, timeout)
        connected, server_open = send_feedback(command, connected, server_open)
