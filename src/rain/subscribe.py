from .authenticate import setup
from .cli import client_cli
from .config import temp_config
from .decompose import pub_split, print_response
from .fetch import load_server
from .transport import receive_subscribe


def run_subscribe():
    dir_pub, dir_prv, dir_info, dir_data = temp_config()

    args = client_cli()
    server_name = args.instrument
    filters = args.param

    server_address = load_server(dir_info, server_name)
    client_name = "apollo"
    host_type = "subscribe"

    _, socket = setup(
        host_type, server_name, server_address, client_name, filters, dir_pub, dir_prv
    )

    print("Waiting for updates from the server")
    socket.connect(f"tcp://{server_address[0]}:{server_address[1]}")
    client_connected = True
    while client_connected:
        formatted_update = receive_subscribe(socket)
        update = pub_split(formatted_update)
        print_response(update)
