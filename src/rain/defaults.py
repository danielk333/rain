from dataclasses import dataclass
from pathlib import Path

HOME = Path(Path.home())

# Default paths
DEFAULT_FOLDER = HOME / ".config" / "rain"
PLUGINS_FOLDER = DEFAULT_FOLDER / "plugins"
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
    "Logging": {
        "level": "DEBUG",
        "filepath": "None",
        "file-level": "INFO",
        "print": "True",
        "print-level": "INFO",
    }
}

DEFAULT_TIMEOUTS = {
    "Timeouts": {
        "receive": "10000",
        "subscribe": "-1"
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

SERVER_EXIT_KEY = "__SERVER_EXIT__"
SERVER_EXIT_CODE = "Ezk1wDZ4MTQNG22ASim4"
SERVER_TRIGGER_REQ_OK = "Trigger received"
SERVER_TRIGGER_REQ_FAIL = "No such triggered parameter exists"

REQ_VALIDATION_ERROR = "Request verification failed"
REP_VALIDATION_ERROR = "Response verification failed"
NO_SUCH_PARAM_ERROR = "Parameter '{0}' invalid"

MAX_MESSAGE_SIZE = int(1e6)


@dataclass
class Server():
    host: str
    allowed: list
    publ_host: str = ""
    publ_port: str = ""
    trig_host: str = ""
    trig_port: str = ""
    max_msg_size: int = MAX_MESSAGE_SIZE
    enable_auth = True


@dataclass
class Client():
    server: str
    action: str
    timeout: int
    hostname: str = ""
    port: str = ""
    enable_auth = True
    pub_key: dict = None


@dataclass
class Paths():
    public: str
    private: str
    plugins: str
