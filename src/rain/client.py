import zmq

from .authenticate import setup_client
from .fetch import convert_client_args, get_client_config
from .packaging import form_request, print_response, pub_split
from .transport import send_request, receive_response, receive_subscribe


def run_request(server, server_address, interaction, params, path_pub, path_prv):
    ''' The function used to run all functions relevant to the handling of the
        user requesting parameters provided by the server

    Parameters
    ----------
    server : string
        The name of the server
    interaction : string
        The type of interaction: get or set
    params : list of strings
        The parameters to interact with
    path_pub: Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key
    '''
    message = form_request(interaction, params)

    if message:
        socket = setup_client("request", server, path_pub, path_prv)
        send_request(socket, server_address, message)
        response = receive_response(socket, server_address)
        print_response(response)


def run_subscribe(server, server_address, params, path_pub, path_prv):
    ''' The function used to run all functions relevant to the handling of the
        user subscribing to parameters provided by the server

    Parameters
    ----------
    server : string
        The name of the server
    server_address : list of strings
        The server's hostname and port
    params : list of strings
        The parameters to interact with
    path_pub: Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key
    '''

    socket = setup_client("subscribe", server, path_pub, path_prv)

    for iter in range(len(params)):
        socket.setsockopt_string(zmq.SUBSCRIBE, params[iter])

    print("Waiting for updates from the server")
    socket.connect(f"tcp://{server_address[0]}:{server_address[1]}")
    client_connected = True
    while client_connected:
        formatted_update = receive_subscribe(socket)
        update = pub_split(formatted_update)
        print_response(update)


def rain_client(args):
    ''' The top-level function handling the function of the RAIN client

    Parameters
    ----------
    args : Namespace
        The command line arguments entered by the user
    '''
    server_name, interaction, params, conf_folder = convert_client_args(args)
    dir_pub, dir_prv, server_address = get_client_config(conf_folder, server_name, interaction)

    if interaction == "get" or interaction == "set":
        run_request(server_name, server_address, interaction, params, dir_pub, dir_prv)
    elif interaction == "sub":
        run_subscribe(server_name, server_address, params, dir_pub, dir_prv)
