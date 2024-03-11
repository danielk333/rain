import socket
import time

server_address = ('localhost', 10000)
server_open = False
encoding = 'utf-8'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen()
server_open = True
print(f'Server started on {server_address[0]} with port {server_address[1]}')

while server_open:
    print("I am a WIP server waiting for a friend")
    connection, client_address = sock.accept()
    print(f'I have found a friend at {client_address}!')

    # data = connection.recv(1)
    # data.decode('utf-8')
    # print(data)

    timeout = 5.0
    max_len = 256
    t0 = time.time()
    dt = 0.0
    end_char = '\n'
    while dt < timeout:
        dt = time.time() - t0

        data = ''
        while len(data) < max_len:
            data_raw = connection.recv(1)
            if data_raw == end_char.encode(encoding):
                break
            elif len(data_raw) > 0:
                data += data_raw.decode(encoding)
            else:
                dt = time.time() - t0
                if dt >= timeout:
                    break
            print(data)

            if data == 'echo':
                msg = data
                connection.sendall(msg.encode(encoding))
                data = ''
            if data == 'close':
                msg = 'Closing the connection'
                connection.sendall(msg.encode(encoding))
                # connection.close()
                data = ''
