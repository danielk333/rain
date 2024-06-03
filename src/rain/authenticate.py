import zmq.auth
from zmq.auth.thread import ThreadAuthenticator


def setup_auth(context, address, path_pub):
    ''' Set up the thread used as part of the authentication process

    Parameters
    ----------
    context : zmq.Context
        The ZMQ Context establishing the basis of the communication
    address : list of strings
        The hostname and port of the server
    path_pub : Posix path
        The path to the folder containing the authorised public keys

    Returns
    -------
    auth : thread
        The thread that the authenticator uses to authenticate conenctions
    '''
    auth = ThreadAuthenticator(context)
    auth.start()
    # TODO 49: Set .allow() from the config
    # auth.allow(address[0])
    auth.configure_curve(domain="*", location=path_pub)

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


def auth_server(socket, path_prv):
    ''' Sets up the authentication side to the server connection

    Parameters
    ----------
    socket : zmq.Socket
        The connection socket
    path_prv : Posix path
        The path to the folder containing the server's private key
    '''
    server_file_prv = list(path_prv.glob("*-curve.key_secret"))[0]
    server_pub, server_prv = zmq.auth.load_certificate(server_file_prv)
    socket.curve_secretkey = server_prv
    socket.curve_publickey = server_pub
    socket.curve_server = True


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
    client_file_prv = list(path_prv.glob("*-curve.key_secret"))[0]
    client_pub, client_prv = zmq.auth.load_certificate(client_file_prv)
    socket.curve_secretkey = client_prv
    socket.curve_publickey = client_pub

    server_file_pub = path_pub.joinpath(f"{server}.key")
    server_pub, _ = zmq.auth.load_certificate(server_file_pub)
    socket.curve_serverkey = server_pub


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
    print(f"I am a WIP server open on {address[0]} with port {address[1]}" +
          "readyto talk to friends")


def setup_client(host_type, server, path_pub, path_prv):
    ''' The top-level function that organises the initialisation of the client
        connection

    Parameters
    ----------
    host_type : string
        The type of connection to create: publish, request, response, subscribe
    server : string
        The name of the server
    path_pub : Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key'

    Returns
    -------
    socket : zmq.Socket
        The connection socket
    '''
    context = zmq.Context()
    socket = setup_socket(context, host_type)

    auth_client(socket, server, path_pub, path_prv)

    return socket


def setup_server(host_type, address, path_pub, path_prv):
    ''' The top-level function that organises the initialisation of the server
        connection

    Parameters
    ----------
    host_type : string
        The type of connection to create: publish, request, response, subscribe
    address : list of strings
        The hostname and port of the server
    path_pub : Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the server's private key'

    Returns
    -------
    auth : thread
        The thread that the authenticator uses to authenticate connections
    socket : zmq.Socket
        The connection socket
    '''
    context = zmq.Context()
    socket = setup_socket(context, host_type)

    auth = setup_auth(context, address, path_pub)
    auth_server(socket, path_prv)
    open_connection(socket, address)

    return auth, socket
