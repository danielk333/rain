import os
from load import load_server
from transport import receive_message, send_response
from actions import determine_response_type, form_response
from authenticate import setup_server


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
        response_type = determine_response_type(message)
        response, server_open = form_response(message, response_type, server_open, server_name, dir_info, dir_data)
        send_response(socket, response)
    auth.stop()
