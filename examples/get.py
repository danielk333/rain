"""
Example usage of fetching a get response using rain client API rather than the client CLI
"""
import pathlib
import json
from rain.client import run_request
from rain import Client, Paths

SERVER_CONFIG_LOC = pathlib.Path(".") / "examples" / "reindeer"

response_generator = run_request(
    client = Client(
        server="reindeer",
        action="get",
        timeout=1000,
        hostname="127.0.0.1",
        port=1234,
    ),
    params = ["activity"],
    data = None,
    paths = Paths(
        public = SERVER_CONFIG_LOC / "known_hosts",
        private = SERVER_CONFIG_LOC / "keypairs",
        plugins = "",
    ),
)

# This will iterate forever over all incoming messages
for message in response_generator:
    print(json.dumps(message, indent=4))
