import json
import logging
import socket as pys
import zmq


logger = logging.getLogger(__name__)


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
    frame = socket.recv(0, copy=False)
    src_fd = frame.get(zmq.MessageOption.SRCFD)
    src_sock = pys.socket(fileno=src_fd)
    address = src_sock.getpeername()[0]
    src_sock.detach()

    request = json.loads(frame.bytes.decode("utf-8"))
    request["sender"] = address

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
    try:
        response = socket.recv_json(0)
    except zmq.error.Again:
        logger.error("Server not reachable, response timed out")
        raise KeyboardInterrupt
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
    try:
        update = socket.recv_string(0)
    except zmq.error.Again:
        logger.error("Server not reachable, response timed out")
        raise KeyboardInterrupt

    return update
