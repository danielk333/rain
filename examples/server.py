"""
Example usage of starting servers and loading plugins using rain API rather than the server CLI
"""
import pathlib
import argparse
from rain.server import run_response, run_publish
from rain import Server, Paths, load_plugins


SERVER_CONFIG_LOC = pathlib.Path(".") / "examples" / "reindeer"

parser = argparse.ArgumentParser()
parser.add_argument("type", choices=["rep", "pub"])
args = parser.parse_args()

paths = Paths(
    public = SERVER_CONFIG_LOC / "known_hosts",
    private = SERVER_CONFIG_LOC / "keypairs",
    plugins = SERVER_CONFIG_LOC / "plugins",
)
load_plugins(paths.plugins)

if args.type == "rep":
    run_response(
        server = Server(
            host = "rep",
            allowed = [],
            publ_host = "127.0.0.1",
            publ_port = 1234,
        ),
        paths = paths,
    )
elif args.type == "pub":
    run_publish(
        server = Server(
            host = "pub",
            allowed = [],
            publ_host = "127.0.0.1",
            publ_port = 2468,
            trig_host = "127.0.0.1",
            trig_port = 1793,
        ),
        paths = Paths(
            public = SERVER_CONFIG_LOC / "known_hosts",
            private = SERVER_CONFIG_LOC / "keypairs",
            plugins = SERVER_CONFIG_LOC / "plugins",
        ),
    )
