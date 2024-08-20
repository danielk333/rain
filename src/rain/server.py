import logging
import queue
import threading
import time

import jsonschema
import zmq

from .authenticate import setup_server
from .fetch import convert_server_args, get_server_config, sub_params
from .fetch import get_datetime, setup_logging
from .packaging import form_response, form_failed
from .packaging import publish_update, publish_format
from .plugins import PLUGINS
from .transport import receive_request, send_response
from .validate import validate_request, validate_response, validate_update

logger = logging.getLogger(__name__)


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
        request = receive_request(socket)
        logger.debug("Request received")
        try:
            validate_request(request)
        except jsonschema.exceptions.ValidationError:
            logger.error("Request validation failed")
            response = form_failed("request")
        else:
            logger.debug("Request validated")
            logger.info(f"Request: {request}")
            response = form_response(request)
        finally:
            logger.debug("Response formed")

        try:
            validate_response(response)
        except jsonschema.exceptions.ValidationError:
            logger.error("Response validation failed")
            response = form_failed("response")
        else:
            logger.debug("Response validated")
            logger.info(f"Response: {response}")
        finally:
            send_response(socket, response)
            logger.debug("Response sent to the client")

    auth.stop()


def run_publish(serv_addr, trig_addr, allowed, path_pub, path_prv):
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
    auth, socket = setup_server("pub", serv_addr, allowed, path_pub, path_prv)
    possible_sub = sub_params()
    q = queue.Queue()
    server_open = True

    def trigger_wait():
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(f"tcp://{trig_addr[0]}:{trig_addr[1]}")
        logger.debug("Trigger server opened")
        while server_open:
            trigger = socket.recv_json(0)
            logger.info(f"Trigger received: {trigger}")
            q.put([trigger["name"], trigger["data"]])
            response = {
                "name": trigger["name"],
                "data": "Trigger received"
            }
            logger.debug(f"Trigger response formed: {response}")
            socket.send_json(response, 0)
            logger.debug("Trigger response sent to the trigger server")

    def worker(name):
        func = PLUGINS["sub"][name]["function"]
        interval = PLUGINS["sub"][name]["interval"]
        while server_open:
            value = func(name)
            q.put([name, value])
            time.sleep(interval)

    trig = threading.Thread(target=trigger_wait)
    trig.start()

    for param in possible_sub:
        t = threading.Thread(target=worker, args=[param])
        t.start()
    logger.debug("Threads started for each subscribable parameter")

    while server_open:
        name, new_value = q.get()
        date_time = get_datetime()
        update = publish_update(name, new_value, date_time)
        logger.debug("Update formed")
        try:
            validate_update(update)
        except jsonschema.exceptions.ValidationError:
            logger.error("Update validation failed")
        else:
            logger.debug("Update validated")
            logger.debug(f"Update: {update}")
            publish = publish_format(update)
            socket.send_string(publish)
            logger.debug("Update published")

    auth.stop()


def run_server(args):
    ''' The top-level function handling the function of the RAIN server

    Parameters
    ----------
    args : Namespace
        The command line arguments entered by the user
    '''
    host_type, conf_folder, arg_file, arg_print = convert_server_args(args)
    dir_pub, dir_prv, server_address, trigger_address, allowed_add, logfile, logprint, loglevel = get_server_config(conf_folder, host_type, arg_file, arg_print)
    setup_logging(logfile, logprint, loglevel)

    if host_type == "rep":
        run_response(server_address, allowed_add, dir_pub, dir_prv)
    elif host_type == "pub":
        run_publish(server_address, trigger_address, allowed_add, dir_pub, dir_prv)
