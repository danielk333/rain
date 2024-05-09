import pathlib
import configparser
import warnings

DEFAULT = {
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

    config.read_dict(DEFAULT)

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
