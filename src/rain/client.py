import os
from .packaging import form_message, print_response
from .user_input import determine_type, determine_group
from .transport import send_message, receive_response
from .authenticate import setup_client, load_server


def run_client():

    # TODO 21: Make the paths global variables
    home = os.path.dirname(__file__)
    home = home.removesuffix("/src/rain")
    dir_pub = os.path.join(home, "public_keys")
    dir_prv = os.path.join(home, "private_keys")
    dir_info = os.path.join(home, "infra_info")

    print("Which server would you like to interact with?")
    server_name = input()
    server_address = load_server(dir_info, server_name)
    client_name = "apollo"

    # TODO 11: Make a list of each type of command and separate the responses to these in separate functions
    message_type = determine_type(server_address[0])
    group, group_name = determine_group(dir_info, server_name)
    message = form_message(message_type, group, group_name)

    if message:
        socket = setup_client(dir_pub, dir_prv, server_name, client_name)
        send_message(socket, server_address, message)
        response = receive_response(socket, server_address)
        print_response(response)

    return


run_client()
