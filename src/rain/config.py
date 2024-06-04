import logging
from pathlib import Path

logger = logging.getLogger(__name__)

HOME = Path(Path.home())

# Default paths
DEFAULT_FOLDER = (HOME / ".config" / "rain").resolve()
PLUGIN_FOLDER = DEFAULT_FOLDER / "plugins"
AUTHORISED_KEYS_FOLDER = DEFAULT_FOLDER / "authorised_keys"
KNOWN_HOSTS_FOLDER = DEFAULT_FOLDER / "known_hosts"
KEYPAIRS_FOLDER = DEFAULT_FOLDER / "keypairs"


DEFAULT_SERVER_CFG = {
    "Security": {
        "public-keys": AUTHORISED_KEYS_FOLDER,
        "private-keys": KEYPAIRS_FOLDER
    },
    "Plugins": {
        "plugins": PLUGIN_FOLDER
    },
    "Response": {
        "hostname": "127.0.0.1",
        "port": "1234"
    },
    "Publish": {
        "hostname": "127.0.0.1",
        "port": "2468"
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
