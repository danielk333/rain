import argparse


def client_cli():
    parser = argparse.ArgumentParser(
        prog="RAIN",
        description="RAIN Client Interface"
    )

    parser.add_argument(
        "instrument",
        choices=["odyssey"],
        help="the instrument server to connect to"
    )

    parser.add_argument(
        "interaction",
        choices=["get", "sub", "set"],
        help="the type of interaction with the server"
    )

    parser.add_argument(
        "param",
        nargs="+",
        help="the parameters to investigate"
    )

    parser.add_argument(
        "-c", "--cfgpath",
        help="the path to your RAIN config folder"
    )

    args = parser.parse_args()

    return args


def server_cli():
    parser = argparse.ArgumentParser(
        prog="RAIN",
        description="RAIN Server Interface"
    )

    parser.add_argument(
        "instrument",
        choices=["odyssey"],
        help="the instrument server to connect to"
    )

    parser.add_argument(
        "interaction",
        choices=["rep", "pub"],
        help="the type of interaction with the server"
    )

    parser.add_argument(
        "-c", "--cfgpath",
        help="the path to your RAIN config folder"
    )

    args = parser.parse_args()

    return args


def new_user_cli():
    parser = argparse.ArgumentParser(
        prog="RAIN",
        description="RAIN User Registration"
    )

    parser.add_argument(
        "name",
        help="the name of the instrument"
    )

    parser.add_argument(
        "mode",
        nargs='+',
        choices=["server", "client"],
        help="whether the instrument can act as a server, a client or both"
    )

    args = parser.parse_args()

    return args
