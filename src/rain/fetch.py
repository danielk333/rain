import configparser
from datetime import datetime
import logging
from pathlib import Path
import sys
import warnings

import zmq

from .defaults import (
    Client,
    Server,
    _CFG_PATHS_SERVER,
    _CFG_PATHS_CLIENT,
    DEFAULT_FOLDER,
    DEFAULT_TIMEOUTS
)
from .plugins import PLUGINS, load_plugins

logger = logging.getLogger(__name__)


def find_config(args):
    ''' Uses the input arguments to extract the folder containing the
        configuration file

    Parameters
    ----------
    args : Namespace
        The arguments entered into the system

    Returns
    -------
    folder : Posix path
        The path to the folder containing the configuration file
    '''
    if args.cfgpath is None:
        folder = DEFAULT_FOLDER
        logger.debug(f"Path to config folder: {None}")
    else:
        folder = Path(args.cfgpath)
        logger.debug(f"Path to config folder: {folder}")

    return folder


def load_config(folder, container):
    ''' Establishes the path to the configuration file and reads its contents

    Parameters
    ----------
    folder : Posix path
        The path to the folder containing the configuration file
    container : string
        Whether the user is running a server or a client

    Returns
    -------
    config : ConfigParser
        The set of configs found in the configuration file
    '''
    if container == "server":
        config_file = folder / "server.cfg"
        defaults = _CFG_PATHS_SERVER
    elif container == "client":
        config_file = folder / "hosts.cfg"
        defaults = _CFG_PATHS_CLIENT

    config = configparser.ConfigParser()

    if config_file is not None:
        if not isinstance(config_file, Path):
            config_file = Path(config_file)
        config.read([config_file])

    for section, key in defaults:
        _path = Path(config.get(section, key)).resolve()
        config.set(section, key, str(_path))
        if not _path.exists():
            warnings.warn(f"configured path '{_path}' does not exist")

    return config


def setup_logging(args, config):
    ''' Uses the input arguments and configs to set up logging

    Parameters
    ----------
    args : Namespace
        The arguments entered into the system
    config : ConfigParser
        The set of configs found in the client's configuration file
    '''
    lib_logger = logging.getLogger("rain")

    cfg_level = config.get("Logging", "level", fallback="INFO")
    cfg_file = config.get("Logging", "filepath", fallback=None)
    if cfg_file == "None":
        cfg_file = None
    cfg_filelevel = config.get("Logging", "file-level", fallback="INFO")
    cfg_print = config.getboolean("Logging", "print", fallback=False)
    cfg_printlevel = config.get("Logging", "print-level", fallback="INFO")

    if args.loglevel is not None:
        loglevel = args.loglevel
    else:
        loglevel = cfg_level

    if args.logfile is not None:
        logfile = args.logfile.resolve()
    else:
        logfile = cfg_file

    if args.filelevel is not None:
        filelevel = args.filelevel
    else:
        filelevel = cfg_filelevel

    logprint = cfg_print or args.logprint

    if args.printlevel is not None:
        printlevel = args.printlevel
    else:
        printlevel = cfg_printlevel

    # TODO 65: Make logging format configurable
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s')

    if logfile is not None:
        handler = logging.FileHandler(str(logfile))
        handler.setFormatter(formatter)
        handler.setLevel(filelevel)
        lib_logger.addHandler(handler)

    if logprint:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        handler.setLevel(printlevel)
        lib_logger.addHandler(handler)

    lib_logger.setLevel(loglevel)
    lib_logger.debug("Logging setup complete")


def find_paths(config, container):
    ''' Uses the configs from the configuration file to extract the paths to
        the public keys, keypair and (for a server) plugins

    Parameters
    ----------
    config : ConfigParser
        The set of configs found in the client's configuration file
    container : string
        Whether the user is running a server or a client

    Returns
    -------
    path_pub : Posix path
        The path to the folder containing the public keys of the known clients
    path_prv : Posix path
        The path to the folder containing the server's private key
    path_plug : Posix path
        The path to the folder containing the server's plugins
    '''
    path_pub = Path(config.get("Security", "public-keys"))
    path_prv = Path(config.get("Security", "private-keys"))
    if container == "server":
        path_plug = Path(config.get("Plugins", "plugins"))
    else:
        path_plug = None

    return path_pub, path_prv, path_plug


def setup_server_object(args, config):
    ''' Reads the input arguments and the loaded configs to fill in a Server
        object containing relevant connection information

    Parameters
    ----------
    args : Namespace
        The arguments entered into the system
    config : ConfigParser
        The set of configs found in the configuration file

    Returns
    -------
    server : Server object
        Contains information regarding the connection established by the server
    '''
    if "Allowed" in config:
        allowed = [config.get("Allowed", option) for option in config["Allowed"]]

    server = Server(args.host, allowed)

    if args.host == "rep":
        server.publ_host = config.get("Response", "hostname")
        server.publ_port = config.get("Response", "port")

    elif args.host == "pub":
        server.publ_host = config.get("Publish", "hostname")
        server.publ_port = config.get("Publish", "port")
        server.trig_host = config.get("Trigger", "hostname")
        server.trig_port = config.get("Trigger", "port")
        server.enable_auth = args.auth

    if "Messages" in config:
        server.max_msg_size = config.getint("Messages", "max-size")

    return server


def setup_client_object(args, config):
    ''' Reads the input arguments and the loaded configs to fill in a Client
        object containing relevant connection information

    Parameters
    ----------
    args : Namespace
        The arguments entered into the system
    config : ConfigParser
        The set of configs found in the configuration file

    Returns
    -------
    client : Client object
        Contains information regarding the connection to the server
    '''
    if args.action == "set" or args.action == "get":
        interaction = "response"
        timeout_fb = DEFAULT_TIMEOUTS["Timeouts"]["receive"]
        timeout = config.getint("Timeouts", "receive", fallback=timeout_fb)

    elif args.action == "sub":
        interaction = "publish"
        timeout_fb = DEFAULT_TIMEOUTS["Timeouts"]["subscribe"]
        timeout = config.getint("Timeouts", "subscribe", fallback=timeout_fb)

    client = Client(args.server, args.action, timeout)

    client.hostname = config.get(f"{args.server}-{interaction}", "hostname")
    client.port = config.get(f"{args.server}-{interaction}", "port")

    if args.action == "sub":
        client.enable_auth = args.auth

    return client


def find_params(args):
    ''' Uses the input arguments to determine the list of parameters requested
        by the client

    Parameters
    ----------
    args : Namespace
        The arguments entered into the system

    Returns
    -------
    params : list of strings
        The parameters requested by the client
    '''
    if args.action == "get" or args.action == "set":
        params = args.param
        logger.info(f"Parameters requested: {params}")

    elif args.action == "sub":
        params = []
        if args.changes is not None:
            for item in args.changes:
                params.append(item)
            logger.info(f"Parameter changes: {args.changes}")
        else:
            logger.info(f"Parameter changes: {None}")
        if args.freq is not None:
            for item in args.freq:
                params.append(item)
            logger.info(f"Frequency parameters: {args.freq}")
        else:
            logger.info(f"Frequency parameters: {args.freq}")
        if args.trigger is not None:
            for item in args.trigger:
                params.append(item)
            logger.info(f"Triggers: {args.trigger}")
        else:
            logger.info(f"Triggers: {None}")

        if len(params) == 0:
            logger.error("No parameters entered")
            exit()

    return params


def handle_server_args(args):
    ''' Uses the input arguments to read the server's configuration file and
        set up the necessary paths, connection details and logging

    Parameters
    ----------
    args : Namespace
        The arguments entered into the system

    Returns
    -------
    server : Server object
        Contains information regarding the connection established by the server
    path_pub : Posix path
        The path to the folder containing the public keys of the known clients
    path_prv : Posix path
        The path to the folder containing the server's private key
    '''
    conf_folder = find_config(args)
    config = load_config(conf_folder, "server")
    setup_logging(args, config)
    path_pub, path_prv, path_plug = find_paths(config, "server")
    load_plugins(path_plug)
    server = setup_server_object(args, config)

    return server, path_pub, path_prv


def handle_client_args(args):
    ''' Uses the input arguments to read the client's configuration file and
        set up the necessary paths, connection details and logging

    Parameters
    ----------
    args : Namespace
        The arguments entered into the system

    Returns
    -------
    client : Client object
        Contains information regarding the connection to the server
    params : list of strings
        The parameters requested by the client
    path_pub : Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key
    '''
    conf_folder = find_config(args)
    config = load_config(conf_folder, "client")
    setup_logging(args, config)
    path_pub, path_prv, _ = find_paths(config, "client")
    client = setup_client_object(args, config)
    params = find_params(args)

    return client, params, path_pub, path_prv


def get_datetime():
    ''' Finds the current time and date with a timezone offset and returns a
        string in the ISO 8601 format

    Returns
    -------
    current_datetime : string
        The current time and date in ISO format including a timezone offset
    '''
    current_datetime = datetime.now().astimezone().isoformat()

    return current_datetime


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


def sub_trig_params():
    ''' Returns a list of the triggered parameters that the server has made
        available for clients to subscribe to

    Returns
    -------
    list_params : list of strings
        A list of trigger parameters that can be subscribed to
    '''
    list_params = list(PLUGINS["sub-trigger"].keys())

    return list_params


def get_keys(path_pub):
    ''' Returns a dict containing the public keys of all users that can connect
        and the associated user names, taken from the name of the file the key
        is stored in

    Parameters
    ----------
    path_pub : Posix path
        The path to the folder containing the public keys of the known hosts

    Returns
    -------
    keys_dict : dict
        A dict containing all server/client public keys as keys and the file
        names they are in as values
    '''
    keys_dict = {}
    for file in path_pub.glob("*"):
        key = zmq.auth.load_certificate(file)
        keys_dict[key[0].decode()] = file.stem

    return keys_dict
