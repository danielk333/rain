import configparser
from pathlib import Path

import zmq

from .config import AUTHORISED_KEYS_FOLDER, DEFAULT_FOLDER, KNOWN_HOSTS_FOLDER, PLUGINS_FOLDER
from .config import DEFAULT_SERVER_CFG, DEFAULT_LOGGING, DEFAULT_TIMEOUTS


def gen_paths(cfg_path, key_path):
    ''' Generates the configuration paths based on the user's input. If no
        input, then default locations are used, otherwise the config paths are
        set relative to the inputted path

    Parameters
    ----------
    cfg_path : Posix path
        The path to the folder containing the instrument's config file
    key_path : Posix path
        The path to the folder containing the instrument's keypair

    Returns
    -------
    path_conf : Posix path
        The path to the folder containing the instrument's config file
    path_auth : Posix path
        The path to the folder containing the authorised public keys
    path_host : Posix path
        The path to the folder containing the available servers' public keys
    path_pair : Posix path
        The path to the folder containing the instrument's keypair
    path_plug : Posix path
        The path to the folder containing the plugins
    '''
    if cfg_path is None:
        path_conf = DEFAULT_FOLDER
        path_auth = AUTHORISED_KEYS_FOLDER
        path_host = KNOWN_HOSTS_FOLDER
        path_plug = PLUGINS_FOLDER
    else:
        path_conf = cfg_path
        path_auth = path_conf / "authorised_keys"
        path_host = path_conf / "known_hosts"
        path_plug = path_conf / "plugins"

    if key_path is None:
        path_pair = path_conf / "keypairs"
    else:
        path_pair = key_path

    if not path_conf.is_dir():
        path_conf.mkdir()
    if not path_auth.is_dir():
        path_auth.mkdir()
    if not path_host.is_dir():
        path_host.mkdir()
    if not path_pair.is_dir():
        path_pair.mkdir()
    if not path_plug.is_dir():
        path_plug.mkdir()

    return path_conf, path_auth, path_host, path_pair, path_plug


def gen_keys(name, cfg_path, key_path):
    ''' Generates the instrument's public-private keypair and places them in
        the keypairs folder

    Parameters
    ----------
    name : string
        The name of the server
    cfg_path : Posix path
        The path to the folder containing the instrument's config file
    key_path : Posix path
        The path to the folder containing the instrument's keypair
    '''
    file_pub, file_prv = zmq.auth.create_certificates(cfg_path, name)
    key_pub, key_prv = zmq.auth.load_certificate(file_prv)

    Path.rename(
        cfg_path / f"{name}.key",
        key_path / f"{name}.key"
    )
    Path.rename(
        cfg_path / f"{name}.key_secret",
        key_path / f"{name}-curve.key_secret"
    )


def gen_server_cfg(path_conf, path_pub, path_prv, path_plug):
    ''' Generates a configuration file for the server, containing the server's
        TCP/IP details (for both REP and PUB) socket types, as well as the
        locations of the folders holding the authorised public keys, private
        keys and plugins

    Parameters
    ----------
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

    config['Security'] = {
        'public-keys': path_pub,
        'private-keys': path_prv
    }
    config['Plugins'] = {
        'plugins': path_plug
    }

    for section in DEFAULT_LOGGING:
        config.add_section(section)
        for key in DEFAULT_LOGGING[section]:
            config[section][key] = DEFAULT_LOGGING[section][key]

    for section in DEFAULT_SERVER_CFG:
        config.add_section(section)
        for key in DEFAULT_SERVER_CFG[section]:
            config[section][key] = DEFAULT_SERVER_CFG[section][key]

    filename = path_conf / "server.cfg"
    with open(filename, 'w') as configfile:
        config.write(configfile)


def gen_client_cfg(path_conf, path_pub, path_prv):
    ''' Generates a configuration file for the client, containing the
        locations of the folders holding the public keys of the known hosts,
        private keys and plugins

    Parameters
    ----------
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

    for section in DEFAULT_LOGGING:
        config.add_section(section)
        for key in DEFAULT_LOGGING[section]:
            config[section][key] = DEFAULT_LOGGING[section][key]

    for section in DEFAULT_TIMEOUTS:
        config.add_section(section)
        for key in DEFAULT_TIMEOUTS[section]:
            config[section][key] = DEFAULT_TIMEOUTS[section][key]

    filename = path_conf / "hosts.cfg"
    with open(filename, 'w') as configfile:
        config.write(configfile)
