import json
import logging
import queue
import threading
import time

import jsonschema
import zmq

from .authenticate import setup_server
from .defaults import (
    SERVER_EXIT_KEY,
    SERVER_EXIT_CODE,
    SERVER_TRIGGER_REQ_OK,
    SERVER_TRIGGER_REQ_FAIL
)
from .fetch import (
    get_datetime,
    handle_server_args,
    sub_params,
    sub_trig_params,
)
from .packaging import (
    fill_sender_details,
    form_response,
    form_failed,
    publish_format,
    publish_update
)
from .plugins import PLUGINS
from .transport import receive_request, send_response
from .validate import validate_reqrep, validate_pub

logger = logging.getLogger(__name__)


def run_response(address, allowed, path_pub, path_prv, max_size, exit_handler=None, exit_handler_check=10):
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
    max_size : int
        The maximum message size a server will accept. If a client attempts to
        send a longer message, it will be immediately disconnected
    exit_handler : function, default=None
        A function that returns a boolean to check weather the server should
        exit or not, if this is set, the socket receive will no longer be
        blocking and check the value returned according to `exit_handler_check`
    exit_handler_check : int, default=10
        Milliseconds time interval between to checks for new received messages
        and the return value of the `exit_handler` function if `exit_handler`
        is set
    '''
    auth, socket = setup_server("rep", address, allowed, path_pub, path_prv, max_size)

    server_open = True
    blocking = True if exit_handler is None else False
    while server_open:
        if exit_handler is not None:
            server_open = exit_handler()

        try:
            request = receive_request(socket, auth, blocking=blocking)
            logger.debug("Request received")
        except KeyboardInterrupt:
            server_open = False
            logger.info("Closing server")
            continue
        except zmq.error.Again:
            time.sleep(exit_handler_check*1e-3)
            continue

        request = fill_sender_details(auth.keys_dict, request)

        try:
            validate_reqrep(request)
        except jsonschema.exceptions.ValidationError:
            logger.error("Request validation failed:\n" + json.dumps(request))
            response = form_failed("request")
        else:
            logger.debug("Request validated")
            logger.info(f"Request: {json.dumps(request)}")
            response = form_response(request)
        finally:
            logger.debug("Response formed")

        try:
            validate_reqrep(response)
        except jsonschema.exceptions.ValidationError:
            logger.error("Response validation failed")
            response = form_failed("response")
        else:
            logger.debug("Response validated")
            logger.debug(f"Response: {json.dumps(response)}")
        finally:
            send_response(socket, response)
            logger.debug("Response sent to the client")

    auth.stop()


def run_publish(serv_addr, trig_addr, allowed, path_pub, path_prv, max_size, custom_message_queue=None):
    ''' The function used to run all functions relevant to the handling of a
        client requesting parameters provided by this server

    Parameters
    ----------
    serv_addr : list of strings
        The publish server's hostname and port
    trig_addr : list of strings
        The trigger server's hostname and port
    allowed : list of strings
        The hostnames of the clients that are allowed to connect to this server
    path_pub: Posix path
        The path to the folder containing the public keys of the authorised
        hosts
    path_prv : Posix path
        The path to the folder containing the server's private key
    max_size : int
        The maximum message size a server will accept. If a client attempts to
        send a longer message, it will be immediately disconnected
    custom_message_queue : queue.Queue
        Queue instance that will be used to get messages to be published by the
        server, control over this queue allows for custom injection of new
        published values and possibility to terminate the server via the magic
        `(SERVER_EXIT_KEY, SERVER_EXIT_CODE)` put into the queue
    '''
    auth, socket = setup_server("pub", serv_addr, allowed, path_pub, path_prv, max_size)
    possible_sub = sub_params()
    possible_sub_trig = sub_trig_params()
    if custom_message_queue is None:
        q = queue.Queue()
    else:
        q = custom_message_queue
    server_open = True

    def trigger_wait():
        ''' The worker function used by the thread running the trigger server
            to wait for a trigger parameter to be triggered
        '''
        context = zmq.Context()
        context.setsockopt(zmq.SocketOption.SNDTIMEO, 1000)
        context.setsockopt(zmq.SocketOption.RCVTIMEO, 1000)
        context.setsockopt(zmq.LINGER, 0)
        tsocket = context.socket(zmq.REP)
        tsocket.bind(f"tcp://{trig_addr[0]}:{trig_addr[1]}")
        logger.debug("Trigger server opened")
        while server_open:
            try:
                trigger = tsocket.recv_json(0)
            except zmq.error.Again:
                continue
            logger.debug(f"Trigger received: {json.dumps(trigger)}")
            response = {"name": trigger["name"]}
            if trigger["name"] in possible_sub_trig:
                q.put([trigger["name"], trigger["data"]])
                response["data"] = SERVER_TRIGGER_REQ_OK
            else:
                response["data"] = SERVER_TRIGGER_REQ_FAIL
            logger.debug(f"Trigger response formed: {json.dumps(response)}")
            tsocket.send_json(response, 0)
            logger.debug("Trigger response sent to the trigger server")

    def worker(name):
        ''' The worker function run by each parameter thread, calling the
            relevant plugin function, adding the parameter value to the queue
            and waiting for the set interval before repeating this process
        '''
        func = PLUGINS["sub"][name]["function"]
        interval = PLUGINS["sub"][name]["interval"]
        while server_open:
            value = func(name)
            logger.debug(f"Sending value of '{name}'")
            q.put([name, value])
            time.sleep(interval)

    trig = threading.Thread(target=trigger_wait)
    trig.start()

    sub_threads = []
    for param in possible_sub:
        t = threading.Thread(target=worker, args=[param])
        t.start()
        sub_threads.append(t)
        logger.debug(f"Thread started for parameter {param}")

    while server_open:
        try:
            name, new_value = q.get()
        except KeyboardInterrupt:
            server_open = False
            logger.info("Stopping publish server")
            break

        if name == SERVER_EXIT_KEY and new_value == SERVER_EXIT_CODE:
            server_open = False
            logger.info("Stopping publish server from magic Queue code")
            break

        date_time = get_datetime()
        update = publish_update(name, new_value, date_time)
        logger.debug("Update formed")
        try:
            validate_pub(update)
        except jsonschema.exceptions.ValidationError:
            logger.error("Update validation failed")
        else:
            logger.debug("Update validated")
            logger.debug(f"Update: {json.dumps(update)}")
            publish = publish_format(update)
            socket.send_string(publish)
            logger.debug("Update published")

    trig.join()
    for t in sub_threads:
        t.join()
    auth.stop()


def run_server(args):
    ''' The top-level function handling the function of the RAIN server

    Parameters
    ----------
    args : Namespace
        The command line arguments entered by the user
    '''
    dir_pub, dir_prv, addr_server, addr_trig, allowed, max_size = handle_server_args(args)

    if args.host == "rep":
        run_response(
            addr_server,
            allowed,
            dir_pub,
            dir_prv,
            max_size
        )
    elif args.host == "pub":
        run_publish(
            addr_server,
            addr_trig,
            allowed,
            dir_pub,
            dir_prv,
            max_size
        )
