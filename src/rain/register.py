import zmq.auth

from pathlib import Path
from shutil import copy

from .cli import new_user_cli
from .config import CONF_FOLDER, PLUGIN_FOLDER
from .config import AUTHORISED_KEYS_FOLDER, KNOWN_HOSTS_FOLDER, KEYPAIRS_FOLDER
from .generate import generate_server_config, generate_client_config


def run_register():
    args = new_user_cli()
    name = args.name
    mode = args.mode

    path_conf = CONF_FOLDER
    path_auth = AUTHORISED_KEYS_FOLDER
    path_host = KNOWN_HOSTS_FOLDER
    path_plug = PLUGIN_FOLDER

    print("Please enter the location to store your private keypair")
    print(f"Press ENTER for the default path: {KEYPAIRS_FOLDER}")
    path_pair = input()
    if path_pair == '':
        path_pair = KEYPAIRS_FOLDER

    file_pub, file_prv = zmq.auth.create_certificates(path_conf, name)
    key_pub, key_prv = zmq.auth.load_certificate(file_prv)

    Path.rename(
        path_conf / f"{name}.key_secret",
        path_pair / f"{name}.key_secret"
    )

    if "server" in mode and "client" in mode:
        copy(path_conf / f"{name}.key", path_auth / f"{name}.key")
        Path.rename(
            path_conf / f"{name}.key",
            path_host / f"{name}.key"
        )
    else:
        if "server" in mode:
            Path.rename(
                path_conf / f"{name}.key",
                AUTHORISED_KEYS_FOLDER / f"{name}.key"
            )
        elif "client" in mode:
            Path.rename(
                path_conf / f"{name}.key",
                KNOWN_HOSTS_FOLDER / f"{name}.key"
            )

    if "server" in mode:
        generate_server_config(name, path_conf, path_auth, path_pair, path_plug)
    if "client" in mode:
        generate_client_config(name, path_conf, path_host, path_pair, path_plug)
