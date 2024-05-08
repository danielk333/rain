from .authenticate import load_server, setup
from .config import config
from .decompose import message_components
from .packaging import form_response
from .transport import receive_request, send_response


def run_server():

    dir_pub, dir_prv, dir_info, dir_data = config()

    server_name = "odyssey"
    server_address = load_server(dir_info, server_name)
    host_type = "server"

    auth, socket = setup(host_type, server_name, server_address, None, None, dir_pub, dir_prv)
    server_open = True
    while server_open:
        message = receive_request(socket)
        group, num_params, response_type = message_components(dir_info, server_name, message)
        response, server_open = form_response(message, group, num_params, response_type, server_open, server_name, dir_data)
        send_response(socket, response)
    auth.stop()

    return
