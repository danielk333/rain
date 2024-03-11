import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
encoding = 'utf-8'
max_len = 256
end_char = '\n'
dt = 0.0
timeout = 5.0

def send_commands(end_char, encoding):
    command = input()
    data = command + end_char
    sock.sendall(data.encode(encoding))

    return command

def receive_data(max_len, end_char, encoding, dt, timeout):
    data = ''
    t0 = time.time()
    while len(data) < max_len:
        data_raw = sock.recv(1)
        if data_raw == end_char.encode(encoding):
            break
        elif len(data_raw) > 0:
            data += data_raw.decode(encoding)
        else:
            dt = time.time() - t0
            if dt >= timeout:
                break

    return data

def interpret(data, command, connected):
    print(f'Server Response: {data}')
    if command == 'close':
        connected = False
    if command == 'shutdown':
        connected = False
    return connected

print(f'Connecting to {server_address[0]} on port {server_address[1]}')

connection = sock.connect(server_address)
connected = True

while connected:
    command = send_commands(end_char, encoding)
    reception = receive_data(max_len, end_char, encoding, dt, timeout)
    connected = interpret(reception, command, connected)

sys.exit()
