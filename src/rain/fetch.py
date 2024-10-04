import configparser
from datetime import datetime
import logging
from pathlib import Path
import sys
import warnings

from .defaults import DEFAULT_FOLDER, _CFG_PATHS_SERVER, _CFG_PATHS_CLIENT
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


def find_details_server(args, config):
    ''' Uses the input arguments and server configs to extract the connection
        details of the server

    Parameters
    ----------
    args : Namespace
        The arguments entered into the system
    config : ConfigParser
        The set of configs found in the client's configuration file

    Returns
    -------
    addr_publ : list of strings
        The hostname and port of the server
    addr_trig : list of strings
        The hostname and port of the server's trigger network
    allowed : list of strings
        The hostnames of the clients that are authorised to connect
    '''
    if args.host == "rep":
        addr_publ = [
            config.get("Response", "hostname"),
            config.get("Response", "port")
        ]
        addr_trig = None
    elif args.host == "pub":
        addr_publ = [
            config.get("Publish", "hostname"),
            config.get("Publish", "port")
        ]
        addr_trig = [
            config.get("Trigger", "hostname"),
            config.get("Trigger", "port")
        ]

    if "Allowed" in config:
        allowed = [config.get("Allowed", option) for option in config["Allowed"]]
    else:
        allowed = []

    return addr_publ, addr_trig, allowed


def find_details_client(args, config):
    ''' Uses the input arguments and client configs to extract the connection
        details of the server

    Parameters
    ----------
    args : Namespace
        The arguments entered into the system
    config : ConfigParser
        The set of configs found in the client's configuration file

    Returns
    -------
    addr_server : list of strings
        The hostname and port of the server
    timeouts : list of strings
        The connection timeouts when interacting with a server
    '''
    if args.action == "set" or args.action == "get":
        inter_type = "response"
        timeout_fallback = 10000
    elif args.action == "sub":
        inter_type = "publish"
        timeout_fallback = -1

    addr_server = [
        config.get(f"{args.server}-{inter_type}", "hostname"),
        config.get(f"{args.server}-{inter_type}", "port")
    ]

    timeouts = []
    timeouts.append(config.getint("Timeouts", "send", fallback=timeout_fallback))
    timeouts.append(config.getint("Timeouts", "receive", fallback=timeout_fallback))

    return addr_server, timeouts


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
    path_pub : Posix path
        The path to the folder containing the public keys of the known clients
    path_prv : Posix path
        The path to the folder containing the server's private key
    addr_publ : list of strings
        The hostname and port of the server
    addr_trig : list of strings
        The hostname and port of the server's trigger network
    allowed : list of strings
        The hostnames of the clients that are authorised to connect
    '''
    conf_folder = find_config(args)
    config = load_config(conf_folder, "server")
    setup_logging(args, config)
    path_pub, path_prv, path_plug = find_paths(config, "server")
    load_plugins(path_plug)
    addr_publ, addr_trig, allowed = find_details_server(args, config)

    return path_pub, path_prv, addr_publ, addr_trig, allowed


def handle_client_args(args):
    ''' Uses the input arguments to read the client's configuration file and
        set up the necessary paths, connection details and logging

    Parameters
    ----------
    args : Namespace
        The arguments entered into the system

    Returns
    -------
    path_pub : Posix path
        The path to the folder containing the public keys of the known hosts
    path_prv : Posix path
        The path to the folder containing the client's private key
    address : list of strings
        The hostname and port of the server
    timeouts : list of strings
        The connection timeouts when interacting with a server
    params : list of strings
        The parameters requested by the client
    '''
    conf_folder = find_config(args)
    config = load_config(conf_folder, "client")
    setup_logging(args, config)
    path_pub, path_prv, _ = find_paths(config, "client")
    address, timeouts = find_details_client(args, config)
    params = find_params(args)

    return path_pub, path_prv, address, timeouts, params


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
    ''' Returns a list of the triggered parameters that the server has made available for
        clients to subscribe to

    Returns
    -------
    list_params : list of strings
        A list of trigger parameters that can be subscribed to
    '''
    list_params = list(PLUGINS["sub-trigger"].keys())

    return list_params
