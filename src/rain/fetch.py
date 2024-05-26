import configparser
from pathlib import Path
import time
import warnings

from .config import DEFAULT_FOLDER, _CFG_PATHS_SERVER, _CFG_PATHS_CLIENT
from .plugins import PLUGINS, load_plugins


def convert_client_args(args):
    server = args.server
    interaction = args.interaction

    if interaction == "get" or interaction == "sub":
        params = args.param
        new_values = None
    elif interaction == "set":
        params = []
        new_values = []
        for item in args.p:
            params.append(item[0])
            new_values.append(item[1])

    if args.cfgpath is None:
        folder = DEFAULT_FOLDER
    else:
        folder = args.cfgpath

    return server, interaction, params, new_values, folder


def convert_server_args(args):
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


# def load_config(config_file=None):
def load_config(config_file, host_type):
    ''' Loads the configurations of a server or client

    Parameters
    ----------
    config_file : Posix path
        The path to the config file
    host_type : string
        Whether a server or client config is being loaded

    Returns
    -------
    config : ConfigParser
        The set of configs
    '''

    config = configparser.ConfigParser()

    # config.read_dict(DEFAULT_SERVER_CFG)

    if config_file is not None:
        if not isinstance(config_file, Path):
            config_file = Path(config_file)
        config.read([config_file])

    if host_type == "server":
        for section, key in _CFG_PATHS_SERVER:
            _path = Path(config.get(section, key)).resolve()
            config.set(
                section,
                key,
                str(_path),
            )
            if not _path.exists():
                warnings.warn(f"configured path '{_path}' does not exist")

    elif host_type == "client":
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


def get_client_config(folder, interaction):
    conf_loc = folder / "hosts.cfg"
    config = load_config(conf_loc, "client")

    path_pub = Path(config.get("Security", "public-keys"))
    path_prv = Path(config.get("Security", "private-keys"))

    if interaction == "get" or interaction == "set":
        address = [
            config.get("Response", "hostname"),
            config.get("Response", "port"),
        ]
    elif interaction == "sub":
        address = [
            config.get("Publish", "hostname"),
            config.get("Publish", "port"),
        ]

    return path_pub, path_prv, address


def get_server_config(folder, interaction):
    conf_loc = folder / "server.cfg"
    config = load_config(conf_loc, "server")

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
    list_params = PLUGINS["sub"].keys()

    return list_params
