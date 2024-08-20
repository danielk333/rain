import configparser
import logging
from pathlib import Path
import time
import sys
import warnings

from .config import DEFAULT_FOLDER, _CFG_PATHS_SERVER, _CFG_PATHS_CLIENT
from .plugins import PLUGINS, load_plugins

logger = logging.getLogger(__name__)


def find_config(arg_path):
    if arg_path is None:
        folder = DEFAULT_FOLDER
        logger.debug(f"Path to config folder: {None}")
    else:
        folder = Path(arg_path)
        logger.debug(f"Path to config folder: {folder}")

    return folder


def load_config(folder, container):
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
    lib_logger = logging.getLogger("rain")

    cfg_file = config.get("Logging", "filepath", fallback=None)
    cfg_print = config.getboolean("Logging", "print", fallback=False)
    cfg_level = config.get("Logging", "level", fallback="INFO")

    if args.logfile is not None:
        logfile = args.logfile.resolve()
    else:
        logfile = cfg_file

    logprint = cfg_print or args.logprint

    if args.loglevel is not None:
        loglevel = args.loglevel
    else:
        loglevel = cfg_level

    # TODO: Make format configurable
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s')

    if logfile is not None:
        handler = logging.FileHandler(str(logfile))
        handler.setFormatter(formatter)
        handler.setLevel(loglevel)
        lib_logger.addHandler(handler)

    if logprint:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        handler.setLevel(loglevel)
        lib_logger.addHandler(handler)

    lib_logger.setLevel(loglevel)
    lib_logger.debug("logging setup complete")


def find_paths(config, container):
    path_pub = Path(config.get("Security", "public-keys"))
    path_prv = Path(config.get("Security", "private-keys"))
    if container == "server":
        path_plug = Path(config.get("Plugins", "plugins"))
    else:
        path_plug = None

    return path_pub, path_prv, path_plug


def find_details_server(args, config):
    if args.host == "rep":
        addr_pub = [
            config.get("Response", "hostname"),
            config.get("Response", "port")
        ]
        addr_trig = None
    elif args.host == "pub":
        addr_pub = [
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

    return addr_pub, addr_trig, allowed


def find_details_client(args, config):
    if args.action == "set" or args.action == "get":
        inter_type = "response"
    elif args.action == "sub":
        inter_type = "publish"
    address = [
        config.get(f"{args.server}-{inter_type}", "hostname"),
        config.get(f"{args.server}-{inter_type}", "port")
    ]

    return address


def find_params(args):
    if args.action == "get" or args.action == "set":
        params = args.param
        logger.info(f"Parameters: {params}")

    elif args.action == "sub":
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

    return params


def handle_server_args(args):
    conf_folder = find_config(args.cfgpath)
    config = load_config(conf_folder, "server")
    setup_logging(args, config)
    path_pub, path_prv, path_plug = find_paths(config, "server")
    load_plugins(path_plug)
    addr_pub, addr_trig, allowed = find_details_server(args, config)

    return path_pub, path_prv, addr_pub, addr_trig, allowed


def handle_client_args(args):
    conf_folder = find_config(args.cfgpath)
    config = load_config(conf_folder, "client")
    setup_logging(args, config)
    path_pub, path_prv, _ = find_paths(config, "client")
    address = find_details_client(args, config)
    params = find_params(args)

    return path_pub, path_prv, address, params


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
