from keygen import new_keypair
import os

def key_detect(key_file):
    with open(key_file, 'r') as in_file:
        row_found = False
        while not row_found:
            line = in_file.readline()
            if line[0:5] == 'curve':
                row_found = True
                key = []
                for item in range(2):
                    line = in_file.readline()
                    pos = []
                    for iter in range(len(line)):
                        if line[iter] == '"':
                            pos.append(iter)
                    key.append(line[pos[0]+1: pos[1]])
                    item =+ 1

    return key[0], key[1]

def generate_static(name, key, gen_time):
    with open(f'{name}.info', 'w') as static:
        static.write(f'#   {name.upper()}\n\n')
        static.write('#   Contact Name:\n')
        static.write('#   Contact Address:\n')
        static.write('#   Coordinates:\n')

        static.write('\n' + '-------------------\n\n')

        static.write('#   Type: ZeroMQ CURVE Public Certificate\n')
        static.write(f'#   Generated: {gen_time[0]}/{gen_time[1]:02}/{gen_time[2]:02} ' +
                     f'at {gen_time[3]:02}:{gen_time[4]:02}:{gen_time[5]:02} UTC\n\n')
        static.write('curve\n')
        static.write(f'    public-key = "{key_pub}"\n')

        static.write('\n' + '-------------------\n\n')

    return

def generate_secret(name, key_pub, key_prv, gen_time):
    with open(f'{name}.private', 'w') as secret:
        secret.write(f'#   {name.upper()}\n\n')
        secret.write('#   Type: ZeroMQ CURVE **Secret** Certificate\n')
        secret.write(f'#   Generated: {gen_time[0]}/{gen_time[1]:02}/{gen_time[2]:02} ' +
                     f'at {gen_time[3]:02}:{gen_time[4]:02}:{gen_time[5]:02} UTC\n\n')
        secret.write('curve\n')
        secret.write(f'    public-key = "{key_pub}"\n')
        secret.write(f'    secret-key = "{key_prv}"\n')

    return

home = os.path.dirname(__file__)
dir_pub = os.path.join(home, 'public_keys')
dir_prv = os.path.join(home, 'private_keys')

print('Please enter the name of your instrument:')
infra_name = input().lower()

# Generate a key pair for the new instrument
## TODO 1: Check there is no existing instrument with this name, and no existing keypair
file_pub, file_prv, gen_time = new_keypair(infra_name)

# Extract public and private keys from the automatically generated files
key_pub, key_prv = key_detect(file_prv)

# Delete the automatically generated files
os.remove(file_pub)
os.remove(file_prv)

# Create a new file for the private key
generate_secret(infra_name, key_pub, key_prv, gen_time)

# Create an info file and write in it the static information
generate_static(infra_name, key_pub, gen_time)

# TODO 4: Add the new info file to a directory with other info files

print(f'Thank you for registering {infra_name} to RAIN!')
