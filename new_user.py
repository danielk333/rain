from keygen import new_keypair
import os

def key_detect(key_file):
    with open(key_file, 'r') as in_file:
        row_found = False
        while not row_found:
            line = in_file.readline()
            if line[0:5] == 'curve':
                row_found = True
                line = in_file.readline()
        pos = []
        for iter in range(len(line)):
            if line[iter] == '"':
                pos.append(iter)
        key = line[pos[0]+1: pos[1]]

    return key

## TODO 2: Add the time the keypair was generated
def generate_static(name, key):
    with open(f'{name}.info', 'w') as static:
        static.write(name.upper())
        static.write('\n\n')
        static.write('Contact Name:\n')
        static.write('Contact Address:\n')
        static.write('Contact Coordinates:\n\n')

        static.write('Type: ZeroMQ CURVE Public Certificate\n')
        static.write(f'Generated: \n')
        static.write('curve\n')
        static.write(f'    public-key = {key_pub}\n')

        static.write('\n' + '-------------------\n\n')

    return

## TODO 2
def generate_secret(name, key_pub, key_prv):
    with open(f'{name}.private', 'w') as secret:
        secret.write(name.upper() + '\n\n')
        secret.write('Type: ZeroMQ CURVE **Secret** Certificate\n\n')
        secret.write(f'Generated: \n')
        secret.write('curve\n')
        secret.write(f'    public-key = {key_pub}\n')
        secret.write(f'    secret-key = {key_prv}\n')

    return

home = os.path.dirname(__file__)
dir_pub = os.path.join(home, 'public_keys')
dir_prv = os.path.join(home, 'private_keys')

print('Please enter the name of your instrument:')
infra_name = input().lower()

# Generate a key pair for the new instrument
## TODO 1: Check there is no existing instrument with this name, and no existing keypair
file_pub, file_prv = new_keypair(infra_name)

# Extract public and private keys from the automatically generated files
key_pub = key_detect(file_pub)
key_prv = key_detect(file_prv)

# Create a new file for the private key
generate_secret(infra_name, key_pub, key_prv)

# TODO 3: Delete the automatically generated files


# Create an info file and write in it the static information
generate_static(infra_name, key_pub)

# TODO 4: Add the new info file to a directory with other info files

print(f'Thank you for registering {infra_name} to RAIN!')
