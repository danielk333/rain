import logging
from pprint import pprint

import zmq

from .authenticate import setup_client
from .fetch import convert_client_args, get_client_config
from .packaging import form_request, pub_split
from .transport import send_request, receive_response, receive_subscribe
from .validate import validate_response, validate_request, validate_update


def run_request(server, server_address, action, params, path_pub, path_prv):
    ''' The function used to run all functions relevant to the handling of the
        user requesting parameters provided by the server

    Parameters
    ----------
    server : string
        The name of the server
    action : string
        The type of action: get or set
    params : list of strings
        The parameters to interact with
    path_pub: Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key
    '''
    logger = logging.getLogger(__name__)

    request = form_request(action, params)
    logger.debug("Request formed")
    validate_request(request)
    logger.info(f"Request: {request}")
    logger.debug("Request validated")
    pprint(request, indent=4, sort_dicts=False)

    if request:
        socket = setup_client("req", server, path_pub, path_prv)
        send_request(socket, server_address, request)
        logger.debug("Request sent to the server")
        response = receive_response(socket, server_address)
        logger.debug("Response received from the server")
        validate_response(response)
        logger.info(f"Response: {response}")
        logger.debug("Response validated")
        yield response


# TODO 57: Nicely shut down a subscribed client
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
    logger = logging.getLogger(__name__)

    socket = setup_client("sub", server, path_pub, path_prv)

    change_params = params[0]
    freq_params = params[1]
    trig_params = params[2]
    prev_values = []

    for item in change_params:
        prev_values.append([item, ""])
        socket.setsockopt_string(zmq.SUBSCRIBE, item)
    for item in freq_params:
        socket.setsockopt_string(zmq.SUBSCRIBE, item)
    for item in trig_params:
        socket.setsockopt_string(zmq.SUBSCRIBE, item)

    print("Waiting for updates from the server")
    socket.connect(f"tcp://{server_address[0]}:{server_address[1]}")
    logger.info("Connection opened to the publish server")

    client_connected = True
    while client_connected:
        formatted_update = receive_subscribe(socket)
        update = pub_split(formatted_update)
        logger.debug(f"Update received from the server: {update}")
        validate_update(update)
        logger.debug("Update validated")

        if update["name"] in freq_params:
            logger.info(f"Saved update: {update}")
            yield update
        elif update["name"] in change_params:
            for item in range(len(prev_values)):
                if prev_values[item][0] == update["name"]:
                    index = item
            if update["data"] != prev_values[index][1]:
                prev_values[index][1] = update["data"]
                logger.info(f"Saved update: {update}")
                yield update
            else:
                logger.debug("Update not saved")
        elif update["name"] in trig_params:
            logger.info(f"Saved update: {update}")
            yield update


def rain_client(args):
    ''' The top-level function handling the function of the RAIN client

    Parameters
    ----------
    args : Namespace
        The command line arguments entered by the user
    '''
    server_name, action, params, conf_folder = convert_client_args(args)
    dir_pub, dir_prv, server_address = get_client_config(conf_folder, server_name, action)

    if action == "get" or action == "set":
        response = run_request(server_name, server_address, action, params, dir_pub, dir_prv)
    elif action == "sub":
        response = run_subscribe(server_name, server_address, params, dir_pub, dir_prv)

    return response
