import logging

import zmq.auth
from zmq.auth.thread import ThreadAuthenticator

logger = logging.getLogger(__name__)


class ClientCustomAuth:

    def __init__(self):
        self.key = None

    def callback(self, domain, key: bytes):
        self.key = key.decode("utf8")
        return True


def setup_auth(context, allowed, path_pub):
    ''' Set up the thread used as part of the authentication process

    Parameters
    ----------
    context : zmq.Context
        The ZMQ Context establishing the basis of the communication
    allowed : list of strings
        The hostnames of the clients that are allowed to connect to this server
    path_pub : Posix path
        The path to the folder containing the authorised public keys

    Returns
    -------
    auth : thread
        The thread that the authenticator uses to authenticate conenctions
    '''
    auth = ThreadAuthenticator(context)
    auth.start()
    for item in allowed:
        auth.allow(item)
    auth.configure_curve(domain="*", location=path_pub)
    auth.client_auth = ClientCustomAuth()
    auth.configure_curve_callback(domain="*", credentials_provider=auth.client_auth)

    return auth


def setup_socket(context, host_type):
    ''' Sets the socket type depending on the kind of connection to create

    Parameters
    ----------
    context : zmq.Context
        The ZMQ Context establishing the basis of the communication
    host_type : string
        The type of connection to create: pub, req, rep, sub

    Returns
    -------
    socket : zmq.Socket
        The socket for this desired connection
    '''
    if host_type == "pub":
        socket = context.socket(zmq.PUB)
    elif host_type == "req":
        socket = context.socket(zmq.REQ)
    elif host_type == "rep":
        socket = context.socket(zmq.REP)
    elif host_type == "sub":
        socket = context.socket(zmq.SUB)

    return socket


def auth_server(socket, path_prv, auth):
    ''' Sets up the authentication side to the server connection

    Parameters
    ----------
    socket : zmq.Socket
        The connection socket
    path_prv : Posix path
        The path to the folder containing the server's private key
    auth : thread
        The thread that the authenticator uses to authenticate conenctions
    '''
    try:
        server_file_prv = list(path_prv.glob("*-curve.key_secret"))[0]
    except IndexError:
        logger.error("No private key file in the right format in the "
                     "keypairs folder")
        exit()

    # TODO: Check exceptions for loading certificates
    server_pub, server_prv = zmq.auth.load_certificate(server_file_prv)
    socket.curve_secretkey = server_prv
    socket.curve_publickey = server_pub
    socket.curve_server = True
    auth.server_public_key = server_pub.decode("utf8")
    logger.debug("Server keypair loaded")


def auth_client(socket, server, path_pub, path_prv):
    ''' Sets up the authentication side to the client connection

    Parameters
    ----------
    socket : zmq.Socket
        The connection socket
    server : string
        The name of the server
    path_pub : Posix path
        The path to the folder containg the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containg the client's private key
    '''
    try:
        client_file_prv = list(path_prv.glob("*-curve.key_secret"))[0]
    except IndexError:
        logger.error("No private key file in the right format in the "
                     "keypairs folder")
        exit()

    # TODO: Check exceptions for loading certificates
    client_pub, client_prv = zmq.auth.load_certificate(client_file_prv)
    socket.curve_secretkey = client_prv
    socket.curve_publickey = client_pub
    logger.debug("Client keypair loaded")

    server_file_pub = path_pub.joinpath(f"{server}.key")
    server_pub, _ = zmq.auth.load_certificate(server_file_pub)
    socket.curve_serverkey = server_pub
    logger.debug("Server public key loaded")


def open_connection(socket, address):
    ''' Opens the socket connection on the server side

    Parameters
    ----------
    socket : zmq.Socket
        The connection socket
    address : list of strings
        The hostname and port number of the server
    '''
    socket.bind(f"tcp://{address[0]}:{address[1]}")
    logger.info(f"I am a WIP server open on {address[0]} with port " +
                f"{address[1]} ready to talk to friends")
    logger.debug("Server connection opened")


def setup_server(host_type, address, allowed, path_pub, path_prv):
    ''' The top-level function that organises the initialisation of the server
        connection

    Parameters
    ----------
    host_type : string
        The type of connection to create: publish, request, response, subscribe
    address : list of strings
        The hostname and port of the server
    allowed : list of strings
        The hostnames of the clients that are allowed to connect to this server
    path_pub : Posix path
        The path to the folder containing the public keys of the known clients
    path_prv : Posix path
        The path to the folder containing the server's private key

    Returns
    -------
    auth : thread
        The thread that the authenticator uses to authenticate connections
    socket : zmq.Socket
        The connection socket
    '''
    context = zmq.Context()
    socket = setup_socket(context, host_type)

    auth = setup_auth(context, allowed, path_pub)
    auth_server(socket, path_prv, auth)
    open_connection(socket, address)

    return auth, socket


def setup_client(host_type, server, timeouts, path_pub, path_prv):
    ''' The top-level function that organises the initialisation of the client
        connection

    Parameters
    ----------
    host_type : string
        The type of connection to create: publish, request, response, subscribe
    server : string
        The name of the server
    timeouts : list of strings
        The connection timeouts when interacting with a server
    path_pub : Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key

    Returns
    -------
    socket : zmq.Socket
        The connection socket
    '''
    context = zmq.Context()
    context.setsockopt(zmq.SocketOption.SNDTIMEO, timeouts[0])
    context.setsockopt(zmq.SocketOption.RCVTIMEO, timeouts[1])
    context.setsockopt(zmq.LINGER, 0)
    socket = setup_socket(context, host_type)

    auth_client(socket, server, path_pub, path_prv)

    return socket
