import time

from .authenticate import load_server, setup_publish
from .config import config
from .packaging import publish_response


def run_publish():
    dir_pub, dir_prv, dir_info, dir_data = config()

    server_name = "odyssey"
    server_address = load_server(dir_info, server_name)
    server_open = False

    auth, socket, server_open, possible_sub = setup_publish(server_name, server_address, dir_pub, dir_prv, dir_info)

    while server_open:
        # TODO 31: Send subscription updates when changes occur
        time.sleep(2)
        for param in possible_sub:
            response = publish_response(param, server_name, dir_data)
            socket.send_string(response)
