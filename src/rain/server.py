from pathlib import Path
import time

from .authenticate import setup_server
from .config import load_config, reduced_config, DEFAULT_FOLDER
from .fetch import subscribable_params
from .packaging import form_response, publish_response
from .plugins import load_plugins  # , PLUGINS
from .transport import receive_request, send_response


def run_response(server, config, path_pub, path_prv, path_info, path_data, path_plug):
    ''' The function used to run all functions relevant to the handling of a
        client requesting parameters provided by this server

    Parameters
    ----------
    server : string
        The name of the server
    config : ConfigParser
        The set of server configs
    path_pub: Posix path
        The path to the folder containing the public keys of the authorised hosts
    path_prv : Posix path
        The path to the folder containing the server's private key
    path_info : Posix path
        The path to the folder containing the server's info file
    path_data : Posix path
        The path to the folder containing the server's data file
    path_plug : Posix path
        The path to the folder containing the server's plugins
    '''
    server_address = [
        config.get("Response", "hostname"),
        config.get("Response", "port"),
    ]

    auth, socket = setup_server(
        "response", server, server_address, path_pub, path_prv
    )

    server_open = True
    while server_open:
        message = receive_request(socket)
        response = form_response(message, server, path_info, path_data, path_plug)
        print(response)
        # data = []
        # for name in message["parameters"]:
        #     func = PLUGINS[message["type"]][name]
        #     data.append(func(message))
        # response = response_get(message, data)
        send_response(socket, response)
    auth.stop()


def run_publish(server, config, path_pub, path_prv, path_info, path_data):
    ''' The function used to run all functions relevant to the handling of a
        client requesting parameters provided by this server

    Parameters
    ----------
    server : string
        The name of the server
    config : ConfigParser
        The set of server configs
    path_pub: Posix path
        The path to the folder containing the public keys of the authorised hosts
    path_prv : Posix path
        The path to the folder containing the server's private key
    path_info : Posix path
        The path to the folder containing the server's info file
    path_data : Posix path
        The path to the folder containing the server's data file
    '''
    server_address = [
        config.get("Publish", "hostname"),
        config.get("Publish", "port"),
    ]

    auth, socket = setup_server(
        "publish", server, server_address, path_pub, path_prv
    )
    possible_sub = subscribable_params(path_info, server)
    server_open = True

    while server_open:
        # TODO 31: Send subscription updates when changes occur
        time.sleep(2)
        for param in possible_sub:
            response = publish_response(param, server, path_data)
            socket.send_string(response)

    auth.stop()


# TODO 46: Move the config handling into functions
def server(args):
    ''' The top-level function handling the function of the RAIN server

    Parameters
    ----------
    args : Namespace
        The command line arguments entered by the user
    '''
    server_name = args.instrument
    interaction = args.interaction

    if args.cfgpath is None:
        conf_folder = DEFAULT_FOLDER
    else:
        conf_folder = Path(args.cfgpath)
    conf_loc = conf_folder / "server.cfg"
    config = load_config(conf_loc, "server")

    dir_pub = Path(config.get("Security", "public-keys"))
    dir_prv = Path(config.get("Security", "private-keys"))
    dir_plug = Path(config.get("Plugins", "plugins"))
    load_plugins(dir_plug)

    dir_info, dir_data = reduced_config()

    if interaction == "rep":
        run_response(server_name, config, dir_pub, dir_prv, dir_info, dir_data, dir_plug)
    elif interaction == "pub":
        run_publish(server_name, config, dir_pub, dir_prv, dir_info, dir_data)
