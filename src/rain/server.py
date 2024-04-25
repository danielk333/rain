import os
from .load import load_server
from .transport import receive_message, send_response
from .actions import form_response, message_components
from .authenticate import setup_server


def run_server():

    home = os.path.dirname(__file__)
    home = home.removesuffix("/src/rain")
    dir_pub = os.path.join(home, "public_keys")
    dir_prv = os.path.join(home, "private_keys")
    dir_info = os.path.join(home, "infra_info")
    dir_data = os.path.join(home, "data")

    server_name = "odyssey"
    server_address = load_server(dir_info, server_name)
    server_open = False

    auth, socket, server_open = setup_server(server_name, server_address, dir_pub, dir_prv)
    while server_open:
        message = receive_message(socket)
        group, num_params, response_type = message_components(dir_info, server_name, message)
        response, server_open = form_response(message, group, num_params, response_type, server_open, server_name, dir_data)
        send_response(socket, response)
    auth.stop()

    return


run_server()