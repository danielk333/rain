from .authenticate import load_server, setup
from .config import config
from .decompose import pub_split, print_response
from .transport import receive_subscribe
from .user_input import params_sub


def run_subscribe():
    dir_pub, dir_prv, dir_info, dir_data = config()

    server_name = "odyssey"
    server_address = load_server(dir_info, server_name)
    client_name = "apollo"
    host_type = "subscribe"

    filters = params_sub(server_name, dir_info)
    _, socket = setup(host_type, server_name, server_address, client_name, filters, dir_pub, dir_prv)

    print("Waiting for updates from the server")
    socket.connect(f"tcp://{server_address[0]}:{server_address[1]}")
    client_connected = True
    while client_connected:
        formatted_update = receive_subscribe(socket)
        update = pub_split(formatted_update)
        print_response(update)
