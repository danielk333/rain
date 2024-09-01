import json
import logging

import jsonschema
import zmq

from .authenticate import setup_client
from .fetch import handle_client_args
from .packaging import form_request, pub_split
from .transport import send_request, receive_response, receive_subscribe
from .validate import validate_response, validate_request, validate_update

logger = logging.getLogger(__name__)


def run_request(server, server_address, timeouts, action, params, data, path_pub, path_prv):
    ''' The function used to run all functions relevant to the handling of the
        user requesting parameters provided by the server

    Parameters
    ----------
    server : string
        The name of the server
    server_address : list of strings
        The server's hostname and port
    timeouts : list of strings
        The connection timeouts when interacting with a server
    action : string
        The type of action: get or set
    params : list of strings
        The parameters to interact with
    data : list of strings
        The data to transmit along with the parameters
    path_pub: Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key
    '''
    request = form_request(action, params, data)
    logger.debug("Request formed")
    try:
        validate_request(request)
    except jsonschema.exceptions.ValidationError:
        request = None
        logger.error("Request validation failed")
        exit()
    else:
        logger.debug("Request validated")
        logger.debug(f"Request: {json.dumps(request)}")

    if request:
        socket = setup_client("req", server, timeouts, path_pub, path_prv)
        send_request(socket, server_address, request)
        logger.debug("Request sent to the server")
        response = receive_response(socket, server_address)
        logger.info("Response received from the server")
        try:
            validate_response(response)
        except jsonschema.exceptions.ValidationError:
            logger.error("Response validation failed")
            exit()
        else:
            logger.debug("Response validated")
            logger.debug(f"Response: {json.dumps(response)}")
            yield response


def run_subscribe(server, server_address, timeouts, params, path_pub, path_prv):
    ''' The function used to run all functions relevant to the handling of the
        user subscribing to parameters provided by the server

    Parameters
    ----------
    server : string
        The name of the server
    server_address : list of strings
        The server's hostname and port
    timeouts : list of strings
        The connection timeouts when interacting with a server
    params : list of strings
        The parameters to interact with
    path_pub: Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key
    '''
    socket = setup_client("sub", server, timeouts, path_pub, path_prv)

    for item in params:
        socket.setsockopt_string(zmq.SUBSCRIBE, item)

    socket.connect(f"tcp://{server_address[0]}:{server_address[1]}")
    logger.info("Connection opened to the publish server")

    client_connected = True
    while client_connected:
        try:
            formatted_update = receive_subscribe(socket)
        except KeyboardInterrupt:
            client_connected = False
            for item in params:
                socket.setsockopt_string(zmq.UNSUBSCRIBE, item)
            logger.info("Closing subscribe client")
            continue

        update = pub_split(formatted_update)
        logger.debug(f"Update received from the server: {json.dumps(update)}")
        try:
            validate_update(update)
            logger.debug("Update validated")
        except jsonschema.exceptions.ValidationError:
            logger.error("Update validation failed")
        else:
            yield update


def run_client(args):
    ''' The top-level function handling the function of the RAIN client

    Parameters
    ----------
    args : Namespace
        The command line arguments entered by the user
    '''
    dir_pub, dir_prv, address_server, timeouts, params = handle_client_args(args)

    if args.action == "get" or args.action == "set":
        response = run_request(args.server, address_server, timeouts, args.action, params, args.data, dir_pub, dir_prv)
    elif args.action == "sub":
        response = run_subscribe(args.server, address_server, timeouts, params, dir_pub, dir_prv)

    return response
