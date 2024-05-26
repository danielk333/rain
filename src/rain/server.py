import time

from .authenticate import setup_server
from .fetch import convert_server_args, get_server_config, sub_params
from .packaging import form_response, publish_response
from .transport import receive_request, send_response


def run_response(server, address, path_pub, path_prv):
    ''' The function used to run all functions relevant to the handling of a
        client requesting parameters provided by this server

    Parameters
    ----------
    server : string
        The name of the server
    address : list of strings
        The server's hostname and port
    path_pub: Posix path
        The path to the folder containing the public keys of the authorised
        hosts
    path_prv : Posix path
        The path to the folder containing the server's private key
    '''

    auth, socket = setup_server(
        "response", server, address, path_pub, path_prv
    )

    server_open = True
    while server_open:
        message = receive_request(socket)
        response = form_response(message)
        print(response)
        send_response(socket, response)
    auth.stop()


def run_publish(server, address, path_pub, path_prv):
    ''' The function used to run all functions relevant to the handling of a
        client requesting parameters provided by this server

    Parameters
    ----------
    server : string
        The name of the server
    address : list of strings
        The server's hostname and port
    path_pub: Posix path
        The path to the folder containing the public keys of the authorised
        hosts
    path_prv : Posix path
        The path to the folder containing the server's private key
    '''
    auth, socket = setup_server("publish", server, address, path_pub, path_prv)
    possible_sub = sub_params()
    server_open = True

    while server_open:
        # TODO 31: Send subscription updates when changes occur
        time.sleep(2)
        for param in possible_sub:
            response = publish_response(param)
            socket.send_string(response)

    auth.stop()


def rain_server(args):
    ''' The top-level function handling the function of the RAIN server

    Parameters
    ----------
    args : Namespace
        The command line arguments entered by the user
    '''
    server_name, interaction, conf_folder = convert_server_args(args)
    dir_pub, dir_prv, server_address = get_server_config(conf_folder, interaction)

    if interaction == "rep":
        run_response(server_name, server_address, dir_pub, dir_prv)
    elif interaction == "pub":
        run_publish(server_name, server_address, dir_pub, dir_prv)
