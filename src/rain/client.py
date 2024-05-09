from pathlib import Path

from .authenticate import load_server, setup
from .config import load_config
from .decompose import print_response
from .packaging import form_request
from .transport import send_request, receive_response
from .user_input import determine_group, determine_type


def run_client():

    config = load_config("./rain.cfg")

    dir_pub = Path(config.get("Security", "public_keys"))
    dir_prv = Path(config.get("Security", "private_keys"))

    server_name = "test-testson"
    server_address = [
        config.get("Response", "hostname"),
        config.get("Response", "port"),
    ]

    # print("Which server would you like to interact with?")
    # server_name = input()
    # server_name = "test-testson"
    # server_address = load_server(dir_info, server_name)
    client_name = "apollo"
    host_type = "client"

    # TODO 11: Make a list of each type of command and separate the responses to these in separate functions
    # message_type = determine_type(server_address[0])
    # group, group_name = determine_group(dir_info, server_name)
    # message = form_request(message_type, group, group_name)
    message = {"type": "get", "group": "", "parameters": ["hello"]}

    if message:
        _, socket = setup(
            host_type, server_name, server_address, client_name, None, dir_pub, dir_prv
        )
        send_request(socket, server_address, message)
        response = receive_response(socket, server_address)
        print_response(response)

    return
