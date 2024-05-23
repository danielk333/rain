import pathlib
import os
import configparser
import warnings
import logging

logger = logging.getLogger(__name__)

HOME = pathlib.Path(os.path.expanduser("~"))
# CONF_FOLDER = (HOME / ".config" / "rain").resolve()

# if not CONF_FOLDER.is_dir():
#     CONF_FOLDER.mkdir()

# Default paths
DEFAULT_FOLDER = (HOME / ".config" / "rain").resolve()
# HOSTS_CFG = CONF_FOLDER / "hosts.cfg"
# SERVER_CFG = CONF_FOLDER / "server.cfg"
PLUGIN_FOLDER = DEFAULT_FOLDER / "plugins"
AUTHORISED_KEYS_FOLDER = DEFAULT_FOLDER / "authorised_keys"
KNOWN_HOSTS_FOLDER = DEFAULT_FOLDER / "known_hosts"
KEYPAIRS_FOLDER = DEFAULT_FOLDER / "keypairs"


DEFAULT_SERVER_CFG = {
    "Response": {
        "hostname": "127.0.0.1",
        "port": "1234"
    },
    "Publish": {
        "hostname": "127.0.0.1",
        "port": "2468"
    },
    "Security": {
        "public-keys": AUTHORISED_KEYS_FOLDER,
        "private-keys": KEYPAIRS_FOLDER
    },
    "Plugins": {
        "plugins": PLUGIN_FOLDER
    }
}

DEFAULT_CLIENT_CFG = {
    "Security": {
        "public-keys": KNOWN_HOSTS_FOLDER,
        "private-keys": KEYPAIRS_FOLDER
    },
    "Plugins": {
        "plugins": PLUGIN_FOLDER
    }
}

_CFG_PATHS_SERVER = [
    ("Security", "public-keys"),
    ("Security", "private-keys"),
    ("Plugins", "plugins")
]

_CFG_PATHS_CLIENT = [
    ("Security", "public-keys"),
    ("Security", "private-keys")
]


# TODO 21: Setup a client/server config file
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
        if not isinstance(config_file, pathlib.Path):
            config_file = pathlib.Path(config_file)
        config.read([config_file])

    if host_type == "server":
        for section, key in _CFG_PATHS_SERVER:
            _path = pathlib.Path(config.get(section, key)).resolve()
            config.set(
                section,
                key,
                str(_path),
            )
            if not _path.exists():
                warnings.warn(f"configured path '{_path}' does not exist")

    elif host_type == "client":
        for section, key in _CFG_PATHS_CLIENT:
            _path = pathlib.Path(config.get(section, key)).resolve()
            config.set(
                section,
                key,
                str(_path),
            )
            if not _path.exists():
                warnings.warn(f"configured path '{_path}' does not exist")

    return config


def reduced_config():
    home = pathlib.Path.cwd()
    dir_info = home / "infra_info"
    dir_data = home / "data"

    return dir_info, dir_data
