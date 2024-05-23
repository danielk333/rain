import configparser


def generate_server_config(name, path_conf, path_pub, path_prv, path_plug):
    ''' Generates a configuration file for the server, containing the server's
        TCP/IP details (for both REP and PUB) socket types, as well as the
        locations of the folders holding the authorised public keys, private
        keys and plugins

    Parameters
    ----------
    name : string
        The name of the server
    path_conf : Posix path
        The path to the folder containing the server's config file
    path_pub : Posix path
        The path to the folder containing the authorised public keys
    path_prv : Posix path
        The path to the folder containing the server's private key
    path_plug : Posix path
        The path to the folder containing the plugins
    '''
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

    filename = path_conf / "server.cfg"
    with open(filename, 'w') as configfile:
        config.write(configfile)


def generate_client_config(name, path_conf, path_pub, path_prv):
    ''' Generates a configuration file for the client, containing the
        locations of the folders holding the public keys of the known hosts,
        private keys and plugins

    Parameters
    ----------
    name : string
        The name of the client
    path_conf : Posix path
        The path to the folder containing the client's config file
    path_pub : Posix path
        The path to the folder containing the known hosts' public keys
    path_prv : Posix path
        The path to the folder containing the client's private key
    '''
    config = configparser.ConfigParser()
    config['Security'] = {
        'public-keys': path_pub,
        'private-keys': path_prv
    }

    filename = path_conf / "hosts.cfg"
    with open(filename, 'w') as configfile:
        config.write(configfile)
