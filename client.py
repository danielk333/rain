import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)

print(f'Connecting to {server_address[0]} on port {server_address[1]}')

sock.connect(server_address)

while True:
    data = input()
    # data += '\n'
    # print(data)
    sock.sendall(data.encode('utf-8'))
    # print(data.encode('utf-8'))

    reception = sock.recv(10)
    reception = reception.decode('utf-8')
    print(f'Server Response: {reception}')
