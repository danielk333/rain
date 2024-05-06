import zmq
import zmq.auth
import os

from .authenticate import load_server, setup_subscribe
from .decompose import pub_split, print_response, load_groups
from .transport import receive_subscribe


def run_subscribe():
    home = os.path.dirname(__file__)
    home = home.removesuffix("/src/rain")
    dir_pub = os.path.join(home, "public_keys")
    dir_prv = os.path.join(home, "private_keys")
    dir_info = os.path.join(home, "infra_info")

    server_name = "odyssey"
    server_address = load_server(dir_info, server_name)
    client_name = "apollo"

    possible_sub = []
    groups = load_groups(dir_info, server_name)
    for group in groups:
        for iter in range(len(group["parameters"])):
            if group["parameters"][iter]["subscribe"] == "true":
                possible_sub.append(group["parameters"][iter]["name"])

    print("Please enter the parameter you would like to subscribe to:")
    print(possible_sub)
    filters = []
    filters.append(input())
    input_continue = True
    while input_continue:
        print("Please enter another parameter you'd like to set:")
        print("Enter 'end' if there are none")
        print(possible_sub)
        user_input = input()
        if user_input == "end":
            input_continue = False
        else:
            filters.append(user_input)

    socket = setup_subscribe(dir_pub, dir_prv, server_name, client_name)
    for iter in range(len(filters)):
        socket.setsockopt_string(zmq.SUBSCRIBE, filters[iter])

    print("Waiting for updates from the server")
    socket.connect(f"tcp://{server_address[0]}:{server_address[1]}")
    client_connected = True
    while client_connected:
        formatted_update = receive_subscribe(socket)
        update = pub_split(formatted_update)
        print_response(update)
