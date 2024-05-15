import zmq.auth
from zmq.auth.thread import ThreadAuthenticator


def setup_auth(context, address, path_pub):
    auth = ThreadAuthenticator(context)
    auth.start()
    auth.allow(address[0])
    auth.configure_curve(domain="*", location=path_pub)

    return auth


def setup_socket(context, host_type):
    if host_type == "publish":
        socket = context.socket(zmq.PUB)
    elif host_type == "request":
        socket = context.socket(zmq.REQ)
    elif host_type == "response":
        socket = context.socket(zmq.REP)
    elif host_type == "subscribe":
        socket = context.socket(zmq.SUB)

    return socket


def auth_server(socket, server, path_prv):
    server_file_prv = path_prv.joinpath(f"{server}.key_secret")
    server_pub, server_prv = zmq.auth.load_certificate(server_file_prv)
    socket.curve_secretkey = server_prv
    socket.curve_publickey = server_pub
    socket.curve_server = True


def auth_client(socket, server, client, path_pub, path_prv):
    client_file_prv = path_prv.joinpath(f"{client}.key_secret")
    client_pub, client_prv = zmq.auth.load_certificate(client_file_prv)
    socket.curve_secretkey = client_prv
    socket.curve_publickey = client_pub

    server_file_pub = path_pub.joinpath(f"{server}.key")
    server_pub, _ = zmq.auth.load_certificate(server_file_pub)
    socket.curve_serverkey = server_pub


def open_connection(socket, address):
    socket.bind(f"tcp://{address[0]}:{address[1]}")
    print(f"I am a WIP publishing server open on {address[0]} " +
          f"with port {address[1]} ready to talk to friends")


def setup_client(host_type, server, client, path_pub, path_prv):
    context = zmq.Context()
    socket = setup_socket(context, host_type)

    auth_client(socket, server, client, path_pub, path_prv)

    return socket


def setup_server(host_type, server, address, path_pub, path_prv):
    context = zmq.Context()
    socket = setup_socket(context, host_type)

    auth = setup_auth(context, address, path_pub)
    auth_server(socket, server, path_prv)
    open_connection(socket, address)

    return auth, socket
