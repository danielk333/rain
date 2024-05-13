import pathlib
import os
import configparser
import warnings
import logging

logger = logging.getLogger(__name__)

HOME = pathlib.Path(os.path.expanduser("~"))
CONF_FOLDER = (HOME / ".config" / "rain").resolve()

if not CONF_FOLDER.is_dir():
    CONF_FOLDER.mkdir()

# Default paths
HOSTS_CFG = CONF_FOLDER / "hosts.cfg"
SERVER_CFG = CONF_FOLDER / "server.cfg"
PLUGIN_FOLDER = CONF_FOLDER / "plugins"
AUTHORIZED_KEYS_FOLDER = CONF_FOLDER / "authorized_keys"
KNOWN_HOSTS_FOLDER = CONF_FOLDER / "known_hosts"
KEYPAIRS_FOLDER = CONF_FOLDER / "keypairs"


DEFAULT_SERVER_CFG = {
    "Response": {
        "port": "1234",
        "hostname": "127.0.0.1",
    },
    "Publish": {
        "port": "1235",
        "hostname": "127.0.0.1",
    },
    "Security": {
        "public_keys": "./public_keys",
        "private_keys": "./private_keys",
    },
    "Plugins": {
        "plugin_folder": "./plugins",
    },
}

_CFG_PATHS = [
    ("Security", "public_keys"),
    ("Security", "private_keys"),
    ("Plugins", "plugin_folder"),
]


# TODO 21: Setup a client/server config file
def load_config(config_file=None):

    config = configparser.ConfigParser()

    config.read_dict(DEFAULT_SERVER_CFG)

    if config_file is not None:
        if not isinstance(config_file, pathlib.Path):
            config_file = pathlib.Path(config_file)
        config.read([config_file])

    for section, key in _CFG_PATHS:
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
