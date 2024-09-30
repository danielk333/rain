"""
Example usage of subscribing to a data-stream using the rain client API rather than the client CLI
"""
import pathlib
import json
import rain.client

SERVER_CONFIG_LOC = pathlib.Path(".") / "examples" / "reindeer"

response_generator = rain.client.run_subscribe(
    params = ["activity"],
    server = "reindeer",
    server_address = ("127.0.0.1", 2468),
    timeouts = [-1, -1],
    path_pub = SERVER_CONFIG_LOC / "known_hosts",
    path_prv = SERVER_CONFIG_LOC / "keypairs",
)

# This will iterate forever over all incoming messages
for message in response_generator:
    print(json.dumps(message, indent=4))
