import zmq.auth

from pathlib import Path
from shutil import copy

from .cli import new_user_cli
from .config import DEFAULT_FOLDER, PLUGIN_FOLDER
from .config import AUTHORISED_KEYS_FOLDER, KNOWN_HOSTS_FOLDER  # , KEYPAIRS_FOLDER
from .generate import generate_server_config, generate_client_config


def run_register():
    ''' The top-level function handling the registration of new instruments to
        RAIN
    '''
    args = new_user_cli()

    if args.cfgpath is None:
        path_conf = DEFAULT_FOLDER
        path_auth = AUTHORISED_KEYS_FOLDER
        path_host = KNOWN_HOSTS_FOLDER
        path_plug = PLUGIN_FOLDER
    else:
        path_conf = args.cfgpath
        path_auth = path_conf / "authorised_keys"
        path_host = path_conf / "known_hosts"
        path_plug = path_conf / "plugins"

    if args.keypath is None:
        path_pair = path_conf / "keypairs"
    else:
        path_pair = args.keypath

    if not path_conf.is_dir():
        path_conf.mkdir()
    if not path_auth.is_dir():
        path_auth.mkdir()
    if not path_host.is_dir():
        path_host.mkdir()
    if not path_plug.is_dir():
        path_plug.mkdir()
    if not path_pair.is_dir():
        path_pair.mkdir()

    # print("Please enter the location to store your private keypair")
    # print(f"Press ENTER for the default path: {KEYPAIRS_FOLDER}")
    # path_pair = input()
    # if path_pair == '':
    #     path_pair = KEYPAIRS_FOLDER

    file_pub, file_prv = zmq.auth.create_certificates(path_conf, args.name)
    key_pub, key_prv = zmq.auth.load_certificate(file_prv)

    # TODO 48: Change the name of the private key file to include 'curve'
    Path.rename(
        path_conf / f"{args.name}.key_secret",
        path_pair / f"{args.name}.key_secret"
    )

    if "server" in args.mode and "client" in args.mode:
        copy(path_conf / f"{args.name}.key", path_auth / f"{args.name}.key")
        Path.rename(
            path_conf / f"{args.name}.key",
            path_host / f"{args.name}.key"
        )
    else:
        if "server" in args.mode:
            Path.rename(
                path_conf / f"{args.name}.key",
                path_auth / f"{args.name}.key"
            )
        elif "client" in args.mode:
            Path.rename(
                path_conf / f"{args.name}.key",
                path_host / f"{args.name}.key"
            )

    if "server" in args.mode:
        generate_server_config(args.name, path_conf, path_auth, path_pair, path_plug)
    if "client" in args.mode:
        generate_client_config(args.name, path_conf, path_host, path_pair, path_plug)
