import zmq
import zmq.auth
import os

from authenticate import load_server, setup_subscribe
from transport import receive_subscribe

home = os.path.dirname(__file__)
home = home.removesuffix("/src/rain")
dir_pub = os.path.join(home, "public_keys")
dir_prv = os.path.join(home, "private_keys")
dir_info = os.path.join(home, "infra_info")

server_name = "odyssey"
server_address = load_server(dir_info, server_name)
client_name = "apollo"

filter_hyp = "hyperdrive"
filter_sub = "sub-light"
filter_test = ""

socket = setup_subscribe(dir_pub, dir_prv, server_name, client_name)
socket.setsockopt_string(zmq.SUBSCRIBE, filter_hyp)
socket.setsockopt_string(zmq.SUBSCRIBE, filter_sub)
# socket.setsockopt_string(zmq.SUBSCRIBE, filter_test)

print("Waiting for updates from the server")
socket.connect(f"tcp://{server_address[0]}:{server_address[1]}")
client_connected = True
while client_connected:
    output = receive_subscribe(socket)
    print(output)
