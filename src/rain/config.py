from pathlib import Path

HOME = Path(Path.home())

# Default paths
DEFAULT_FOLDER = HOME / ".config" / "rain"
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
    "Trigger": {
        "hostname": "127.0.0.1",
        "port": "1793"
    },
    "Allowed": {}
}

DEFAULT_LOGGING = {
    "Logging-file": {
        "filepath": "None",
        "level": "INFO"
    },
    "Logging-print": {
        "print": "True",
        "level": "INFO"}
}

DEFAULT_TIMEOUTS = {
    "Timeouts": {
        "send": "10000",
        "receive": "10000"
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
