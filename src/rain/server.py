import queue
import threading
import time

import zmq

from .authenticate import setup_server
from .fetch import convert_server_args, get_server_config, sub_params
from .fetch import get_datetime
from .packaging import form_response
from .packaging import publish_update, publish_format
from .plugins import PLUGINS
from .transport import receive_request, send_response
from .validate import validate_request, validate_response, validate_update


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
        print(message)
        validate_request(message)
        response = form_response(message)
        validate_response(response)
        send_response(socket, response)
        print(response)

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
    q = queue.Queue()
    server_open = True

    def trigger_wait():
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://127.0.0.1:1793")
        while server_open:
            trigger = socket.recv_json(0)
            q.put([trigger["name"], trigger["data"]])
            response = {
                "name": trigger["name"],
                "data": "Trigger received"
            }
            socket.send_json(response, 0)

    def worker(name, func, interval):
        while server_open:
            value = func()
            q.put([name, value])
            time.sleep(interval)

    trig = threading.Thread(target=trigger_wait)
    trig.start()

    for param in possible_sub:
        func = PLUGINS["sub"][param]["function"]
        get_func, interval = func()
        t = threading.Thread(target=worker, args=[param, get_func, interval])
        t.start()

    while server_open:
        name, new_value = q.get()
        date_time = get_datetime()
        update = publish_update(name, new_value, date_time)
        validate_update(update)
        publish = publish_format(update)
        socket.send_string(publish)

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
