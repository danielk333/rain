def send_request(socket, address, request):
    ''' Sends a request from a client to a server

    Parameters
    ----------
    socket : zmq.Socket
        The connection socket
    address : list of strings
        The hostname and port of the server
    request : JSON
        The request to send to the server
    '''
    socket.connect(f"tcp://{address[0]}:{address[1]}")
    socket.send_json(request, 0)

    return


def receive_request(socket):
    ''' Receives a request from a client

    Parameters
    ----------
    socket : zmq.Socket
        The conenction socket

    Returns
    -------
    request : JSON
        The request sent by the client to the server
    '''
    request = socket.recv_json(0)
    print(f"Message received:\n{request}")

    return request


def send_response(socket, response):
    ''' Sends a response from a server to a client, in response to a request

    Parameters
    ----------
    socket : zmq.Socket
        The connection socket
    response : JSON
        The response to send to the client
    '''
    socket.send_json(response, 0)

    return


def receive_response(socket, address):
    ''' Receives a response from a server, in response to a request

    Parameters
    ----------
    socket : zmq.Socket
        The connection socket
    address : list of strings
        The hostname and port of the server

    Returns
    -------
    response : JSON
        The responsesent by the server to the client
    '''
    response = socket.recv_json(0)
    socket.disconnect(f"tcp://{address[0]}:{address[1]}")

    return response


def receive_subscribe(socket):
    ''' Receives an update due to the change in the value of a parameter the
        client has subscribed to

    Parameters
    ----------
    socket : zmq.Socket
        The connection socket

    Returns
    -------
    update : string
        The update sent by the server
    '''
    update = socket.recv_string()

    return update
