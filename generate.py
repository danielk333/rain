def generate_header(path, name):
    with open(f'{path}/{name}.info', 'w') as f:
        f.write(f'#   {name.upper()}\n\n')
        f.write('#   Contact Name: \n')
        f.write('#   Email: \n')
        f.write('#   Phone Number: \n')
        f.write('#   Address: \n')
        f.write('#   Coordinates: \n')
        f.write('\n' + '-------------------\n\n')

    return

def generate_key(path, name, key, gen_time):
    with open(f'{path}/{name}.info', 'a') as f:
        f.write('#   PUBLIC KEY\n\n')
        f.write('#   Type: ZeroMQ CURVE Public Certificate\n')
        f.write(f'#   Generated: {gen_time[0]}/{gen_time[1]:02}/{gen_time[2]:02} ' +
                     f'at {gen_time[3]:02}:{gen_time[4]:02}:{gen_time[5]:02} UTC\n\n')
        ## TODO 14: Convert the key from bytes to string
        f.write(f'    public-key = "{key}"\n')
        f.write('\n' + '-------------------\n\n')

    return

def generate_server(path, name):
    with open(f'{path}/{name}.info', 'a') as f:
        f.write('#   SERVER DETAILS\n\n')
        f.write('#   Server Address: \n')
        f.write('#   Port: \n')
        f.write('\n' + '-------------------\n\n')

    return

def generate_params(path, name):
    with open(f'{path}/{name}.info', 'a') as f:
        f.write('#   PARAMETER GROUPS\n\n')
        f.write('{\n')
        f.write('    "group_name": "",\n')
        f.write('    "parameters": [\n')

        number_params = 3
        for item in range(number_params):
            f.write('        {\n')
            f.write('            "name": "",\n')
            f.write('            "request": "",\n')
            f.write('            "command": "",\n')
            f.write('            "subscribe": ""\n')
            if item != number_params-1:
                f.write('        },\n')
            else:
                f.write('        }\n')

        f.write('    ]\n')
        f.write('}\n')

    return