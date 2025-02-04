"""
Example usage of subscribing to a data-stream using the rain client API rather than the client CLI

RUN THE SERVER BEFORE USING THIS EXAMPLE
either with the CLI or the `server.py` example with the `pub` argument
"""
import pathlib
import json
from rain.client import run_subscribe
from rain import Client, Paths


SERVER_CONFIG_LOC = pathlib.Path(".") / "examples" / "reindeer"

response_generator = run_subscribe(
    client = Client(
        server="reindeer",
        action="sub",
        timeout=-1,
        hostname="127.0.0.1",
        port=2468,
    ),
    params = ["activity"],
    paths = Paths(
        public = SERVER_CONFIG_LOC / "known_hosts",
        private = SERVER_CONFIG_LOC / "keypairs",
        plugins = "",
    ),
)

# This will iterate forever over all incoming messages
for message in response_generator:
    print(json.dumps(message, indent=4))
