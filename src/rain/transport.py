def send_request(socket, server_address, message):
    socket.connect(f"tcp://{server_address[0]}:{server_address[1]}")
    socket.send_json(message, 0)

    return


def receive_request(socket):
    message = socket.recv_json(0)
    print(f"Message received:\n{message}")

    return message


def send_response(socket, response):
    socket.send_json(response, 0)

    return


def receive_response(socket, server_address):
    response = socket.recv_json(0)
    socket.disconnect(f"tcp://{server_address[0]}:{server_address[1]}")

    return response
