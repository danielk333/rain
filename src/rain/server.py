from pathlib import Path

from .authenticate import setup
from .config import load_config, reduced_config
from .plugins import load_plugins, PLUGINS
from .decompose import message_components
from .packaging import response_get, form_response
from .transport import receive_request, send_response


def run_response():
    config = load_config("./rain.cfg")
    load_plugins(config.get("Plugins", "plugin_folder"))

    dir_pub = Path(config.get("Security", "public_keys"))
    dir_prv = Path(config.get("Security", "private_keys"))
    dir_info, dir_data = reduced_config()

    server_name = "odyssey"
    server_address = [
        config.get("Response", "hostname"),
        config.get("Response", "port"),
    ]

    auth, socket = setup(
        "server", server_name, server_address, None, None, dir_pub, dir_prv
    )

    server_open = True
    while server_open:
        message = receive_request(socket)
        group, num_params, response_type = message_components(
            dir_info, server_name, message
        )
        response, server_open = form_response(
            message,
            group,
            num_params,
            response_type,
            server_open,
            server_name,
            dir_data,
        )
        # data = []
        # for name in message["parameters"]:
        #     func = PLUGINS[message["type"]][name]
        #     data.append(func(message))
        # response = response_get(message, data)
        send_response(socket, response)
    auth.stop()


def run_server():
    """Runs the response socket using the supplied configuration

    TODO: write docstring
    """

    config = load_config("./rain.cfg")
    load_plugins(config.get("Plugins", "plugin_folder"))

    dir_pub = Path(config.get("Security", "public_keys"))
    dir_prv = Path(config.get("Security", "private_keys"))

    server_name = "test-testson"
    server_address = [
        config.get("Response", "hostname"),
        config.get("Response", "port"),
    ]
    host_type = "server"

    auth, socket = setup(
        host_type, server_name, server_address, None, None, dir_pub, dir_prv
    )
    server_open = True
    while server_open:
        message = receive_request(socket)
        print(message)
        data = []
        for name in message["parameters"]:
            func = PLUGINS[message["type"]][name]
            data.append(func(message))
        response = response_get(message, data)

        # group, num_params, response_type = message_components(
        #     dir_info, server_name, message
        # )
        # response, server_open = form_response(
        #     message,
        #     group,
        #     num_params,
        #     response_type,
        #     server_open,
        #     server_name,
        #     dir_data,
        # )
        send_response(socket, response)
    auth.stop()

    return
