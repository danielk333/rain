import configparser
import json
from pathlib import Path

import zmq

from .config import DEFAULT_FOLDER


def rain_trigger(args):
    ''' Function used to send a trigger to the server's trigger server

    Parameters
    ----------
    args : Namespace
        The arguments entered into the system
    '''
    if args.cfgpath is None:
        folder = DEFAULT_FOLDER
    else:
        folder = Path(args.cfgpath)
    path_conf = folder / "server.cfg"

    config = configparser.ConfigParser()
    config.read([path_conf])

    server_host = config.get("Trigger", "hostname")
    server_port = config.get("Trigger", "port")

    name = args.name
    value = args.value
    message = {
        "name": name,
        "data": value
    }

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{server_host}:{server_port}")
    socket.send_json(message, 0)
    response = socket.recv_json(0)
    print(json.dumps(response, indent=4, sort_keys=False))
