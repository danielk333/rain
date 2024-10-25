import json
import logging

import jsonschema
import zmq

from .authenticate import setup_client
from .fetch import handle_client_args
from .packaging import fill_sender_details, form_request, pub_split
from .transport import send_request, receive_response, receive_subscribe
from .validate import validate_reqrep, validate_pub

logger = logging.getLogger(__name__)


def run_request(client, params, data, paths):
    ''' The function used to run all functions relevant to the handling of the
        user requesting parameters provided by the server

    Parameters
    ----------
    client : Client object
        Contains information regarding the connection to the server
    params : list of strings
        The parameters to interact with
    data : list of strings
        The data to transmit along with the parameters
    paths : Path object
        An object containing the paths to the folders holding the senders'
        public keys and the user's private keypair
    '''
    request = form_request(client.action, params, data)
    logger.debug("Request formed")
    try:
        validate_reqrep(request)
    except jsonschema.exceptions.ValidationError:
        request = None
        logger.error("Request validation failed")
        return
    else:
        logger.debug("Request validated")
        logger.debug(f"Request: {json.dumps(request)}")

    if request:
        socket, client.pub_key = setup_client(client, paths)
        send_request(socket, client.hostname, client.port, request)
        logger.debug("Request sent to the server")
        try:
            response = receive_response(socket, client.hostname, client.port, client.pub_key)
        except zmq.error.Again:
            logger.error("Server not reachable, response timed out")
            return

        response = fill_sender_details(client.pub_key, response)

        logger.info("Response received from the server")
        try:
            validate_reqrep(response)
        except jsonschema.exceptions.ValidationError:
            logger.error("Response validation failed")
            return
        else:
            logger.debug("Response validated")
            logger.debug(f"Response: {json.dumps(response)}")
            yield response


def run_subscribe(client, params, paths):
    ''' The function used to run all functions relevant to the handling of the
        user subscribing to parameters provided by the server

    Parameters
    ----------
    client : Client object
        Contains information regarding the connection to the server
    params : list of strings
        The parameters to interact with
    paths : Path object
        An object containing the paths to the folders holding the senders'
        public keys and the user's private keypair
    '''
    socket, client.pub_key = setup_client(client, paths)

    for item in params:
        socket.setsockopt_string(zmq.SUBSCRIBE, item)

    socket.connect(f"tcp://{client.hostname}:{client.port}")
    logger.info("Connection opened to the publish server")

    client_connected = True
    while client_connected:
        try:
            formatted_update = receive_subscribe(socket)
        except (KeyboardInterrupt, zmq.error.Again) as e:
            if isinstance(e, KeyboardInterrupt):
                logger.info("Closing subscribe client")
            elif isinstance(e, zmq.error.Again):
                logger.error("Server not reachable, response timed out")

            client_connected = False
            for item in params:
                socket.setsockopt_string(zmq.UNSUBSCRIBE, item)
            continue

        update = pub_split(formatted_update)

        if client.pub_key:
            for key in client.pub_key:
                update["sender-key"] = key
                update["sender-name"] = client.pub_key[key]

        logger.debug(f"Update received from the server: {json.dumps(update)}")
        try:
            validate_pub(update)
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
    client, params, paths = handle_client_args(args)

    if args.action == "get" or args.action == "set":
        response = run_request(client, params, args.data, paths)
    elif args.action == "sub":
        response = run_subscribe(client, params, paths)

    return response
