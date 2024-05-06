import os

import zmq.auth
from zmq.auth.thread import ThreadAuthenticator


def load_server(path, server_name):
    server_address = []
    with open(os.path.join(path, f"{server_name}.info"), "r") as f:
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


def setup_server(server_name, server_address, dir_pub, dir_prv):
    context = zmq.Context()
    auth = ThreadAuthenticator(context)
    auth.start()
    auth.allow(server_address[0])
    auth.configure_curve(domain="*", location=dir_pub)

    socket = context.socket(zmq.REP)
    server_file_prv = os.path.join(dir_prv, f"{server_name}.key_secret")
    server_pub, server_prv = zmq.auth.load_certificate(server_file_prv)
    socket.curve_secretkey = server_prv
    socket.curve_publickey = server_pub
    socket.curve_server = True
    socket.bind(f"tcp://{server_address[0]}:{server_address[1]}")
    server_open = True
    print(f"I am a WIP server open on {server_address[0]} with port {server_address[1]} ready to talk to friends")

    return auth, socket, server_open


def setup_client(dir_pub, dir_prv, server_name, client_name):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    client_file_prv = os.path.join(dir_prv, f"{client_name}.key_secret")
    client_pub, client_prv = zmq.auth.load_certificate(client_file_prv)
    socket.curve_secretkey = client_prv
    socket.curve_publickey = client_pub

    server_file_pub = os.path.join(dir_pub, f"{server_name}.key")
    server_pub, _ = zmq.auth.load_certificate(server_file_pub)
    socket.curve_serverkey = server_pub

    return socket


def setup_publish(server_name, server_address, dir_pub, dir_prv):
    context = zmq.Context()
    auth = ThreadAuthenticator(context)
    auth.start()
    auth.allow(server_address[0])
    auth.configure_curve(domain="*", location=dir_pub)

    socket = context.socket(zmq.PUB)
    server_file_prv = os.path.join(dir_prv, f"{server_name}.key_secret")
    server_pub, server_prv = zmq.auth.load_certificate(server_file_prv)
    socket.curve_secretkey = server_prv
    socket.curve_publickey = server_pub
    socket.curve_server = True
    socket.bind(f"tcp://{server_address[0]}:{server_address[1]}")
    server_open = True
    print(f"I am a WIP publishing server open on {server_address[0]} " +
          f"with port {server_address[1]} ready to talk to friends")

    return auth, socket, server_open


def setup_subscribe(dir_pub, dir_prv, server_name, client_name):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    client_file_prv = os.path.join(dir_prv, f"{client_name}.key_secret")
    client_pub, client_prv = zmq.auth.load_certificate(client_file_prv)
    socket.curve_secretkey = client_prv
    socket.curve_publickey = client_pub

    server_file_pub = os.path.join(dir_pub, f"{server_name}.key")
    server_pub, _ = zmq.auth.load_certificate(server_file_pub)
    socket.curve_serverkey = server_pub

    return socket
