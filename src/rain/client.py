from pathlib import Path

import zmq

from .authenticate import setup_client
from .config import load_config, reduced_config, DEFAULT_FOLDER
from .packaging import form_request, print_response, pub_split
from .transport import send_request, receive_response, receive_subscribe


def run_request(server, client, config, interaction, params, new_values, path_pub, path_prv):
    ''' The function used to run all functions relevant to the handling of the
        user requesting parameters provided by the server

    Parameters
    ----------
    server : string
        The name of the server
    client : string
        The name of the client
    config : ConfigParser
        The set of client configs
    interaction : string
        The type of interaction: get or set
    params : list of strings
        The parameters to interact with
    new_values : list of strings
        The new values to give to parameters (if interaction is set)
    path_pub: Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key
    '''
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
    ''' The function used to run all functions relevant to the handling of the
        user subscribing to parameters provided by the server

    Parameters
    ----------
    server : string
        The name of the server
    client : string
        The name of the client
    config : ConfigParser
        The set of client configs
    interaction : string
        The type of interaction: get or set
    params : list of strings
        The parameters to interact with
    path_pub: Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key
    '''
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


# TODO 45: Move the argument handling into functions
# TODO 46: Move the config handling into functions
def client(args):
    ''' The top-level function handling the function of the RAIN client

    Parameters
    ----------
    args : Namespace
        The command line arguments entered by the user
    '''
    server_name = args.server
    client_name = "apollo"
    interaction = args.interaction

    if interaction == "get" or interaction == "sub":
        params = args.param
        new_values = None
    elif interaction == "set":
        params = []
        new_values = []
        for item in args.p:
            params.append(item[0])
            new_values.append(item[1])

    if args.cfgpath is None:
        conf_folder = DEFAULT_FOLDER
    else:
        conf_folder = args.cfgpath

    conf_loc = conf_folder / "hosts.cfg"
    config = load_config(conf_loc)

    dir_pub = Path(config.get("Security", "public_keys"))
    dir_prv = Path(config.get("Security", "private_keys"))
    dir_info, dir_data = reduced_config()

    if interaction == "get" or interaction == "set":
        run_request(server_name, client_name, config, interaction, params, new_values, dir_pub, dir_prv)
    elif interaction == "sub":
        run_subscribe(server_name, client_name, config, params, dir_pub, dir_prv)
