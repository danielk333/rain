import configparser
from pathlib import Path
import time
import warnings

from .config import DEFAULT_FOLDER, _CFG_PATHS_SERVER, _CFG_PATHS_CLIENT
from .plugins import PLUGINS, load_plugins


def convert_client_args(args):
    ''' Assigns the client CLI arguments to variables

    Parameters
    ----------
    args : Namespace
        The client CLI arguments

    Returns
    -------
    server : string
        The server name
    interaction : string
        The type of interaction with the server: get, set, sub
    params : list of strings
        The parameters to interact with
    new_values : list of strings
        The new values to assign to params (in a SET interaction)
    folder : Posix path
        The path to the folder containing the client's config file
    '''
    server = args.server
    interaction = args.interaction

    if interaction == "get" or interaction == "sub":
        params = args.param
        # new_values = None
    elif interaction == "set":
        params = args.p
        # new_values = []
        # for item in args.p:
        #     params.append(item[0])
        #     new_values.append(item[1])

    if args.cfgpath is None:
        folder = DEFAULT_FOLDER
    else:
        folder = args.cfgpath

    return server, interaction, params, folder


def convert_server_args(args):
    ''' Assigns the server CLI arguments to variables

    Parameters
    ----------
    args : Namespace
        The server CLI arguments

    Returns
    -------
    interaction : string
        The type of interaction to allow with clients: pub, rep
    folder : Posix path
        The path to the folder containing the server's config file
    '''
    interaction = args.interaction

    if args.cfgpath is None:
        folder = DEFAULT_FOLDER
    else:
        folder = args.cfgpath

    return interaction, folder


def get_datetime():
    ''' Finds the current date and local time and return an array with these
        values

    Returns
    -------
    current_datetime : list of strings
        The current local date and time
    '''
    local_time = time.localtime()
    current_datetime = []
    current_datetime.append(f"{local_time[0]:04}-{local_time[1]:02}-{local_time[2]:02}")
    current_datetime.append(f"{local_time[3]:02}:{local_time[4]:02}:{local_time[5]:02} Local Time")

    return current_datetime


def load_server_config(config_file):
    ''' Loads the configurations of a server or client

    Parameters
    ----------
    config_file : Posix path
        The path to the config file

    Returns
    -------
    config : ConfigParser
        The set of configs
    '''

    config = configparser.ConfigParser()

    if config_file is not None:
        if not isinstance(config_file, Path):
            config_file = Path(config_file)
        config.read([config_file])

    for section, key in _CFG_PATHS_SERVER:
        _path = Path(config.get(section, key)).resolve()
        config.set(
            section,
            key,
            str(_path),
        )
        if not _path.exists():
            warnings.warn(f"configured path '{_path}' does not exist")

    return config


def load_client_config(config_file):
    ''' Loads the configurations of a server or client

    Parameters
    ----------
    config_file : Posix path
        The path to the config file

    Returns
    -------
    config : ConfigParser
        The set of configs
    '''
    config = configparser.ConfigParser()
    if config_file is not None:
        if not isinstance(config_file, Path):
            config_file = Path(config_file)
        config.read([config_file])

    for section, key in _CFG_PATHS_CLIENT:
        _path = Path(config.get(section, key)).resolve()
        config.set(
            section,
            key,
            str(_path),
        )
        if not _path.exists():
            warnings.warn(f"configured path '{_path}' does not exist")

    return config


def get_client_config(folder, server, interaction):
    ''' Load the values inside the client's config file

    Parameters
    ----------
    folder : Posix path
        The path to the folder containing the client's config file
    server : string
        The name of the server
    interaction : "string"

    Returns
    -------
    path_pub : Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key
    address : list of strings
        The server's hostname and port
    '''
    config = load_client_config(folder / "hosts.cfg")

    path_pub = Path(config.get("Security", "public-keys"))
    path_prv = Path(config.get("Security", "private-keys"))

    if interaction == "set" or interaction == "get":
        act_type = "response"
    elif interaction == "sub":
        act_type = "publish"
    address = [
        config.get(f"{server}-{act_type}", "hostname"),
        config.get(f"{server}-{act_type}", "port")
    ]

    return path_pub, path_prv, address


def get_server_config(folder, interaction):
    ''' Load the values inside the server's config file and loads the server's
        plugins

    Parameters
    ----------
    folder : Posix path
        The path to the folder containing the client's config file
    interaction : string
        The type of interaction to allow with clients: pub, rep

    Returns
    -------
    path_pub : Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key
    address : list of strings
        The server's hostname and port
    '''
    config = load_server_config(folder / "server.cfg")

    path_pub = Path(config.get("Security", "public-keys"))
    path_prv = Path(config.get("Security", "private-keys"))
    path_plug = Path(config.get("Plugins", "plugins"))
    load_plugins(path_plug)

    if interaction == "rep":
        address = [
            config.get("Response", "hostname"),
            config.get("Response", "port"),
        ]
    elif interaction == "pub":
        address = [
            config.get("Publish", "hostname"),
            config.get("Publish", "port"),
        ]

    return path_pub, path_prv, address


def sub_params():
    ''' Returns a list of the parameters that the server has made available for
        clients to subscribe to

    Returns
    -------
    list_params : list of strings
        A list of parameters that can be subscribed to
    '''
    list_params = PLUGINS["sub"].keys()

    return list_params
