import logging
import zmq


logger = logging.getLogger(__name__)


def send_request(socket, hostname, port, request):
    ''' Sends a request from a client to a server

    Parameters
    ----------
    socket : zmq.Socket
        The connection socket
    hostname : string
        The server's hostname (IP address)
    port : string
        The server's port
    request : JSON
        The request to send to the server
    '''
    socket.connect(f"tcp://{hostname}:{port}")
    socket.send_json(request, 0)

    return


def receive_request(socket: zmq.Socket, auth, blocking=True):
    ''' Receives a request from a client

    Parameters
    ----------
    socket : zmq.Socket
        The conenction socket

    Returns
    -------
    request : JSON
        The request sent by the client to the server
    blocking : bool
        Determines if the socket recv should be blocking or not,
        if not blocking the recv will raise `zmq.error.Again` when
        there is no new connections
    '''
    flags = 0 if blocking else zmq.NOBLOCK
    request = socket.recv_json(flags)
    request["sender-key"] = auth.client_auth.key
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


def receive_response(socket, hostname, port, auth):
    ''' Receives a response from a server, in response to a request

    Parameters
    ----------
    socket : zmq.Socket
        The connection socket
    hostname : string
        The server's hostname (IP address)
    port : string
        The server's port
    auth : dict
        Dict with auth information about client and server connection

    Returns
    -------
    response : JSON
        The responsesent by the server to the client
    '''
    response = socket.recv_json(0)
    for key in auth:
        response["sender-key"] = key
    # response["sender-key"] = auth["server_public_key"]
    socket.disconnect(f"tcp://{hostname}:{port}")

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
