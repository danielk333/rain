import os

from keygen import new_keypair, key_detect
from generate import generate_static

home = os.path.dirname(__file__)
dir_info = os.path.join(home, 'infra_info')
dir_pub = os.path.join(home, 'public_keys')
dir_prv = os.path.join(home, 'private_keys')

print('Please enter the name of your instrument:')
infra_name = input().lower()

# Generate a key pair for the new instrument
## TODO 1: Check there is no existing instrument with this name, and no existing keypair
file_pub, file_prv, gen_time = new_keypair(home, infra_name)

# Extract public and private keys from the automatically generated files
key_pub, key_prv = key_detect(file_prv)

# Create an info file and write in it the static information, in the infra_info directory
generate_static(dir_info, infra_name, key_pub, gen_time)

# Move these files into their respective directories
os.rename(os.path.join(home, f'{infra_name}.key'), os.path.join(dir_pub, f'{infra_name}.key'))
os.rename(os.path.join(home, f'{infra_name}.key_secret'), os.path.join(dir_prv, f'{infra_name}.key_secret'))

print(f'Thank you for registering {infra_name} to RAIN!')
