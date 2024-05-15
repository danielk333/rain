def send_request(socket, address, message):
    socket.connect(f"tcp://{address[0]}:{address[1]}")
    socket.send_json(message, 0)

    return


def receive_request(socket):
    message = socket.recv_json(0)
    print(f"Message received:\n{message}")

    return message


def send_response(socket, response):
    socket.send_json(response, 0)

    return


def receive_response(socket, address):
    message = socket.recv_json(0)
    socket.disconnect(f"tcp://{address[0]}:{address[1]}")

    return message


def receive_subscribe(socket):
    message = socket.recv_string()

    return message
