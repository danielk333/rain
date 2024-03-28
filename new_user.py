import os

from keygen import new_keypair, key_detect
from generate import generate_static, generate_secret

home = os.path.dirname(__file__)
dir_info = os.path.join(home, 'infra_info')
dir_secret = os.path.join(home, 'infra_secret')

print('Please enter the name of your instrument:')
infra_name = input().lower()

# Generate a key pair for the new instrument
## TODO 1: Check there is no existing instrument with this name, and no existing keypair
file_pub, file_prv, gen_time = new_keypair(home, infra_name)

# Extract public and private keys from the automatically generated files
key_pub, key_prv = key_detect(file_prv)

# Delete the automatically generated files
os.remove(file_pub)
os.remove(file_prv)

# Create a new file for the private key, in the infra_secret directory
generate_secret(dir_secret, infra_name, key_pub, key_prv, gen_time)

# Create an info file and write in it the static information, in the infra_info directory
generate_static(dir_info, infra_name, key_pub, gen_time)

print(f'Thank you for registering {infra_name} to RAIN!')
