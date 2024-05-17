import configparser


def generate_server_config(name, path_conf, path_pub, path_prv, path_plug):
    config = configparser.ConfigParser()
    config['Response'] = {
        'hostname': '127.0.0.1',
        'port': '1234',
    }
    config['Publish'] = {
        'hostname': '127.0.0.1',
        'port': '2468'
    }
    config['Security'] = {
        'public-keys': path_pub,
        'private-keys': path_prv
    }
    config['Plugins'] = {
        'plugins': path_plug
    }

    filename = path_conf / f"{name}-server.cfg"
    with open(filename, 'w') as configfile:
        config.write(configfile)


def generate_client_config(name, path_conf, path_pub, path_prv, path_plug):
    config = configparser.ConfigParser()
    config['Security'] = {
        'public-keys': path_pub,
        'private-keys': path_prv
    }
    config['Plugins'] = {
        'plugins': path_plug
    }

    filename = path_conf / f"{name}-hosts.cfg"
    with open(filename, 'w') as configfile:
        config.write(configfile)
