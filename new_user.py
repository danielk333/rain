from keygen import new_keypair
import os

home = os.path.dirname(__file__)
dir_pub = os.path.join(home, 'public_keys')
dir_prv = os.path.join(home, 'private_keys')

print('Please enter the name of your instrument:')
infra_name = input()

# Generate a key pair for the new instrument
## TODO: Check there is no existing instrument with this name, and no existing keypair
file_pub, file_prv = new_keypair(infra_name)
print(file_pub)

# Record public key
with open(file_pub, 'r') as public:
    row_found = False
    while not row_found:
        line = public.readline()
        if line[0:5] == 'curve':
            row_found = True
            line = public.readline()
    pos = []
    for iter in range(len(line)):
        if line[iter] == '"':
            pos.append(iter)
    key_pub = line[pos[0]+1: pos[1]]


# Create an info file and write in it the static information
with open(f'{infra_name}.info', 'w') as static:
    static.write(infra_name.upper())
    static.write('\n\n')
    static.write('Contact Name:\n')
    static.write('Contact Address:\n')
    static.write('Contact Coordinates:\n\n')

    static.write(f'Public Key: {key_pub}\n')
    static.write(f'Generated: \n')
    static.write('Type: ZeroMQ CURVE Public Certificate\n')

    static.write('\n' + '-------------------\n\n')

print(f'Thank you for registering {infra_name} to RAIN!')
