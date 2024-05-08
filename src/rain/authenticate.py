import zmq.auth
from zmq.auth.thread import ThreadAuthenticator

from .decompose import load_groups


def load_server(path, server_name):
    server_address = []
    with open(path.joinpath(f"{server_name}.info"), "r") as f:
        for line in f:
            if "Server" in line:
                ip_address = line.split(': ')[1]
                ip_address = ip_address[0:len(ip_address)-1]
                server_address.append(ip_address)
            elif "Port" in line:
                port = line.split(': ')[1]
                port = port[0:len(port)-1]
                server_address.append(port)

    return server_address


def subscribable_params(server_name, dir_info):
    possible_sub = []
    groups = load_groups(dir_info, server_name)
    for group in groups:
        for iter in range(len(group["parameters"])):
            if group["parameters"][iter]["subscribe"] == "true":
                possible_sub.append(group["parameters"][iter]["name"])

    return possible_sub


def setup_auth(context, server_address, dir_pub):
    auth = ThreadAuthenticator(context)
    auth.start()
    auth.allow(server_address[0])
    auth.configure_curve(domain="*", location=dir_pub)

    return auth


def setup_socket(context, host_type):
    if host_type == "server":
        socket = context.socket(zmq.REP)
    elif host_type == "client":
        socket = context.socket(zmq.REQ)
    elif host_type == "publish":
        socket = context.socket(zmq.PUB)
    elif host_type == "subscribe":
        socket = context.socket(zmq.SUB)

    return socket


def auth_server(socket, server_name, dir_prv):
    server_file_prv = dir_prv.joinpath(f"{server_name}.key_secret")
    server_pub, server_prv = zmq.auth.load_certificate(server_file_prv)
    socket.curve_secretkey = server_prv
    socket.curve_publickey = server_pub
    socket.curve_server = True


def auth_client(socket, server_name, client_name, dir_pub, dir_prv):
    client_file_prv = dir_prv.joinpath(f"{client_name}.key_secret")
    client_pub, client_prv = zmq.auth.load_certificate(client_file_prv)
    socket.curve_secretkey = client_prv
    socket.curve_publickey = client_pub

    server_file_pub = dir_pub.joinpath(f"{server_name}.key")
    server_pub, _ = zmq.auth.load_certificate(server_file_pub)
    socket.curve_serverkey = server_pub


def open_connection(socket, server_address):
    socket.bind(f"tcp://{server_address[0]}:{server_address[1]}")
    print(f"I am a WIP publishing server open on {server_address[0]} " +
          f"with port {server_address[1]} ready to talk to friends")


def setup(host_type, server_name, server_address, client_name, filters, dir_pub, dir_prv):
    context = zmq.Context()
    socket = setup_socket(context, host_type)

    if host_type == "server" or host_type == "publish":
        auth = setup_auth(context, server_address, dir_pub)
        auth_server(socket, server_name, dir_prv)
        open_connection(socket, server_address)
    elif host_type == "client" or host_type == "subscribe":
        auth_client(socket, server_name, client_name, dir_pub, dir_prv)
        auth = None

    if host_type == "subscribe":
        for iter in range(len(filters)):
            socket.setsockopt_string(zmq.SUBSCRIBE, filters[iter])

    return auth, socket
