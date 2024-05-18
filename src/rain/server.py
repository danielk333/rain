from pathlib import Path
import time

from .authenticate import setup_server
from .cli import server_cli
from .config import load_config, reduced_config, CONF_FOLDER
from .fetch import subscribable_params
from .packaging import form_response, publish_response
# from .plugins import load_plugins, PLUGINS
from .transport import receive_request, send_response


def run_response(server, config, path_pub, path_prv, path_info, path_data):
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
        response = form_response(message, server, path_info, path_data)
        # data = []
        # for name in message["parameters"]:
        #     func = PLUGINS[message["type"]][name]
        #     data.append(func(message))
        # response = response_get(message, data)
        send_response(socket, response)
    auth.stop()


def run_publish(server, config, path_pub, path_prv, path_info, path_data):
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


def server():
    args = server_cli()
    server_name = args.instrument
    interaction = args.interaction

    if args.cfgpath is None:
        conf_folder = CONF_FOLDER
    else:
        conf_folder = args.cfgpath
    conf_loc = conf_folder / f"{server_name}-server.cfg"
    config = load_config(conf_loc)
    # load_plugins(config.get("Plugins", "plugin_folder"))

    dir_pub = Path(config.get("Security", "public_keys"))
    dir_prv = Path(config.get("Security", "private_keys"))
    dir_info, dir_data = reduced_config()

    if interaction == "rep":
        run_response(server_name, config, dir_pub, dir_prv, dir_info, dir_data)
    elif interaction == "pub":
        run_publish(server_name, config, dir_pub, dir_prv, dir_info, dir_data)
