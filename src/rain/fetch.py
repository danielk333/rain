import configparser
import logging
from pathlib import Path
import time
import warnings

from .config import DEFAULT_FOLDER, _CFG_PATHS_SERVER, _CFG_PATHS_CLIENT
from .plugins import PLUGINS, load_plugins


def convert_server_args(args):
    ''' Assigns the server CLI arguments to variables

    Parameters
    ----------
    args : Namespace
        The server CLI arguments

    Returns
    -------
    host_type : string
        The type of message for the server to send: pub or rep
    folder : Posix path
        The path to the folder containing the server's config file
    '''
    # TODO 60: Make logging level configurable
    # Make file name and location configurable?
    logging.basicConfig(filename="rain-server.log", level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Start of server operations")

    host_type = args.host
    logger.info(f"Server type: {host_type}")

    if args.cfgpath is None:
        folder = DEFAULT_FOLDER
        logger.info(f"Path to config folder: {None}")
    else:
        folder = Path(args.cfgpath)
        logger.info(f"Path to config folder: {folder}")

    return host_type, folder


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
    action : string
        The type of action with the server: get, set, sub
    params : list of strings
        The parameters to interact with
    new_values : list of strings
        The new values to assign to params (in a SET action)
    folder : Posix path
        The path to the folder containing the client's config file
    '''
    # TODO 60: Make logging level configurable
    # Make file name and location configurable?
    logging.basicConfig(filename="rain-client.log", level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Start of client operations")

    server = args.server
    action = args.action

    logger.info(f"Server: {server}")
    logger.info(f"Action: {action}")

    if action == "sub":
        params = [[], [], []]
        if args.changes is not None:
            for item in args.changes:
                params[0].append(item)
            logger.info(f"Parameter changes: {params[0]}")
        else:
            logger.info(f"Parameter changes: {None}")
        if args.freq is not None:
            for item in args.freq:
                params[1].append(item)
            logger.info(f"Frequency parameters: {params[1]}")
        else:
            logger.info(f"Frequency parameters: {params[1]}")
        if args.trigger is not None:
            for item in args.trigger:
                params[2].append(item)
            logger.info(f"Triggers: {params[2]}")
        else:
            logger.info(f"Triggers: {None}")
    elif action == "get" or action == "set":
        params = args.param
        logger.info(f"Parameters: {params}")

    if args.cfgpath is None:
        folder = DEFAULT_FOLDER
        logger.info(f"Path to config folder: {None}")
    else:
        folder = Path(args.cfgpath)
        logger.info(f"Path to config folder: {folder}")

    return server, action, params, folder


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
    ''' Loads the configurations of a server

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
        config.set(section, key, str(_path))
        if not _path.exists():
            warnings.warn(f"configured path '{_path}' does not exist")

    return config


def load_client_config(config_file):
    ''' Loads the configurations of a client

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
        config.set(section, key, str(_path))
        if not _path.exists():
            warnings.warn(f"configured path '{_path}' does not exist")

    return config


def get_client_config(folder, server, action):
    ''' Load the values inside the client's config file

    Parameters
    ----------
    folder : Posix path
        The path to the folder containing the client's config file
    server : string
        The name of the server
    action : "string"
        The type of action with the server: get, set, sub

    Returns
    -------
    path_pub : Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key
    address : list of strings
        The server's hostname and port
    '''
    logger = logging.getLogger(__name__)

    config = load_client_config(folder / "hosts.cfg")

    path_pub = Path(config.get("Security", "public-keys"))
    path_prv = Path(config.get("Security", "private-keys"))

    if action == "set" or action == "get":
        act_type = "response"
    elif action == "sub":
        act_type = "publish"
    address = [
        config.get(f"{server}-{act_type}", "hostname"),
        config.get(f"{server}-{act_type}", "port")
    ]

    logger.debug("Client configs read")

    return path_pub, path_prv, address


def get_server_config(folder, host_type):
    ''' Load the values inside the server's config file and loads the server's
        plugins

    Parameters
    ----------
    folder : Posix path
        The path to the folder containing the client's config file
    host_type : string
        The type of message for the server to send: pub or rep

    Returns
    -------
    path_pub : Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key
    address : list of strings
        The server's hostname and port
    allowed : list of strings
        The hostnames of the clients that are allowed to connect to this server
    '''
    logger = logging.getLogger(__name__)

    config = load_server_config(folder / "server.cfg")

    path_pub = Path(config.get("Security", "public-keys"))
    path_prv = Path(config.get("Security", "private-keys"))
    path_plug = Path(config.get("Plugins", "plugins"))
    load_plugins(path_plug)

    if host_type == "rep":
        pub_addr = [
            config.get("Response", "hostname"),
            config.get("Response", "port")
        ]
        trig_addr = None
    elif host_type == "pub":
        pub_addr = [
            config.get("Publish", "hostname"),
            config.get("Publish", "port")
        ]
        trig_addr = [
            config.get("Trigger", "hostname"),
            config.get("Trigger", "port")
        ]

    allowed = []
    for option in config["Allowed"]:
        allowed.append(config.get("Allowed", option))

    logger.debug("Server configs read")

    return path_pub, path_prv, pub_addr, trig_addr, allowed


def sub_params():
    ''' Returns a list of the parameters that the server has made available for
        clients to subscribe to

    Returns
    -------
    list_params : list of strings
        A list of parameters that can be subscribed to
    '''
    list_params = list(PLUGINS["sub"].keys())

    return list_params
