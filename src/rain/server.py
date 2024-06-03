import time

from .authenticate import setup_server
from .fetch import convert_server_args, get_server_config, sub_params
from .packaging import form_response, publish_response
from .transport import receive_request, send_response


def run_response(address, allowed, path_pub, path_prv):
    ''' The function used to run all functions relevant to the handling of a
        client requesting parameters provided by this server

    Parameters
    ----------
    address : list of strings
        The server's hostname and port
    allowed : list of strings
        The hostnames of the clients that are allowed to connect to this server
    path_pub: Posix path
        The path to the folder containing the public keys of the authorised
        hosts
    path_prv : Posix path
        The path to the folder containing the server's private key
    '''

    auth, socket = setup_server("rep", address, allowed, path_pub, path_prv)

    server_open = True
    while server_open:
        message = receive_request(socket)
        response = form_response(message)
        print(response)
        send_response(socket, response)
    auth.stop()


def run_publish(address, allowed, path_pub, path_prv):
    ''' The function used to run all functions relevant to the handling of a
        client requesting parameters provided by this server

    Parameters
    ----------
    address : list of strings
        The server's hostname and port
    allowed : list of strings
        The hostnames of the clients that are allowed to connect to this server
    path_pub: Posix path
        The path to the folder containing the public keys of the authorised
        hosts
    path_prv : Posix path
        The path to the folder containing the server's private key
    '''
    auth, socket = setup_server("pub", address, allowed, path_pub, path_prv)
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
    host_type, conf_folder = convert_server_args(args)
    dir_pub, dir_prv, server_address, allowed_add = get_server_config(conf_folder, host_type)

    if host_type == "rep":
        run_response(server_address, allowed_add, dir_pub, dir_prv)
    elif host_type == "pub":
        run_publish(server_address, allowed_add, dir_pub, dir_prv)
