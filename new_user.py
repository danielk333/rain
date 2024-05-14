import os
import zmq.auth

from keygen import new_keypair
from generate import generate_header, generate_key, generate_server, generate_params

home = os.path.dirname(__file__)
dir_info = os.path.join(home, "infra_info")
dir_pub = os.path.join(home, "public_keys")
dir_prv = os.path.join(home, "private_keys")

print("Please enter the name of your instrument:")
infra_name = input().lower()

# Generate a key pair for the new instrument
file_pub, file_prv, gen_time = new_keypair(home, infra_name)

# Extract public and private keys from the automatically generated private file
key_pub, key_prv = zmq.auth.load_certificate(file_prv)

# Move these files into their respective directories
os.rename(os.path.join(home, f"{infra_name}.key"), os.path.join(dir_pub, f"{infra_name}.key"))
os.rename(os.path.join(home, f"{infra_name}.key_secret"), os.path.join(dir_prv, f"{infra_name}.key_secret"))

# Create an info file in the infra_info directory and set it up
generate_header(dir_info, infra_name)
generate_key(dir_info, infra_name, key_pub, gen_time)
generate_server(dir_info, infra_name)
generate_params(dir_info, infra_name, 3)
# TODO 17: Generate the data file

print(f'Thank you for registering {infra_name} to RAIN!')
