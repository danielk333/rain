import time

from .authenticate import setup
from .config import temp_config
from .fetch import load_server, subscribable_params
from .packaging import publish_response


def run_publish():
    dir_pub, dir_prv, dir_info, dir_data = temp_config()

    server_name = "odyssey"
    server_address = load_server(dir_info, server_name)
    server_address[1] = "1235"
    host_type = "publish"

    auth, socket = setup(
        host_type, server_name, server_address, None, None, dir_pub, dir_prv
    )
    possible_sub = subscribable_params(server_name, dir_info)
    server_open = True

    while server_open:
        # TODO 31: Send subscription updates when changes occur
        time.sleep(2)
        for param in possible_sub:
            response = publish_response(param, server_name, dir_data)
            socket.send_string(response)

    auth.stop()
