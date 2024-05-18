from pathlib import Path

import zmq

from .authenticate import setup_client
from .cli import client_cli
from .config import load_config, reduced_config, DEFAULT_FOLDER
from .packaging import form_request, print_response, pub_split
from .transport import send_request, receive_response, receive_subscribe


def run_request(server, client, config, interaction, params, new_values, path_pub, path_prv):
    server_address = [
        config.get("Response", "hostname"),
        config.get("Response", "port"),
    ]

    message = form_request(interaction, params, new_values)

    if message:
        socket = setup_client(
            "request", server, client, path_pub, path_prv
        )
        send_request(socket, server_address, message)
        response = receive_response(socket, server_address)
        print_response(response)


def run_subscribe(server, client, config, params, path_pub, path_prv):
    server_address = [
        config.get("Publish", "hostname"),
        config.get("Publish", "port"),
    ]
    socket = setup_client(
        "subscribe", server, client, path_pub, path_prv
    )

    for iter in range(len(params)):
        socket.setsockopt_string(zmq.SUBSCRIBE, params[iter])

    print("Waiting for updates from the server")
    socket.connect(f"tcp://{server_address[0]}:{server_address[1]}")
    client_connected = True
    while client_connected:
        formatted_update = receive_subscribe(socket)
        update = pub_split(formatted_update)
        print_response(update)


def client():
    args = client_cli()
    server_name = args.instrument
    client_name = "apollo"
    interaction = args.interaction
    params = args.param
    new_values = None

    if args.cfgpath is None:
        conf_folder = DEFAULT_FOLDER
    else:
        conf_folder = args.cfgpath

    conf_loc = conf_folder / f"{client_name}-hosts.cfg"
    config = load_config(conf_loc)

    dir_pub = Path(config.get("Security", "public_keys"))
    dir_prv = Path(config.get("Security", "private_keys"))
    dir_info, dir_data = reduced_config()

    if interaction == "get" or interaction == "set":
        run_request(server_name, client_name, config, interaction, params, new_values, dir_pub, dir_prv)
    elif interaction == "sub":
        run_subscribe(server_name, client_name, config, params, dir_pub, dir_prv)
