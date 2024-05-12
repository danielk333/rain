from pathlib import Path

from .authenticate import setup_client
from .cli import client_cli
from .config import load_config, reduced_config
from .decompose import load_groups, print_response, pub_split
from .packaging import form_request
from .transport import send_request, receive_response, receive_subscribe


def run_request(server_name, client_name, config, interaction, group_name, params, new_values, dir_pub, dir_info, dir_prv):
    server_address = [
        config.get("Response", "hostname"),
        config.get("Response", "port"),
    ]
    group = load_groups(dir_info, server_name)
    message = form_request(interaction, group, group_name, params, new_values)

    if message:
        _, socket = setup_client(
            "request", server_name, client_name, None, dir_pub, dir_prv
        )
        send_request(socket, server_address, message)
        response = receive_response(socket, server_address)
        print_response(response)


def run_subscribe(server_name, client_name, config, params, dir_pub, dir_prv):
    server_address = [
        config.get("Publish", "hostname"),
        config.get("Publish", "port"),
    ]
    _, socket = setup_client(
        "subscribe", server_name, client_name, params, dir_pub, dir_prv
    )

    print("Waiting for updates from the server")
    socket.connect(f"tcp://{server_address[0]}:{server_address[1]}")
    client_connected = True
    while client_connected:
        formatted_update = receive_subscribe(socket)
        update = pub_split(formatted_update)
        print_response(update)


def client():
    config = load_config("./rain.cfg")

    dir_pub = Path(config.get("Security", "public_keys"))
    dir_prv = Path(config.get("Security", "private_keys"))
    dir_info, dir_data = reduced_config()

    args = client_cli()
    server_name = args.instrument
    client_name = "apollo"
    interaction = args.interaction
    group_name = args.group
    params = args.param
    new_values = None

    if interaction == "get" or interaction == "set":
        run_request(server_name, client_name, config, interaction, group_name, params, new_values, dir_pub, dir_info, dir_prv)
    elif interaction == "sub":
        run_subscribe(server_name, client_name, config, params, dir_pub, dir_prv)
