import argparse


def client_cli():
    parser = argparse.ArgumentParser(
        prog="RAIN",
        description="RAIN User Interface"
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
        "group",
        choices=["propulsion", "shields"],
        help="the group of parameters to interact with"
    )

    parser.add_argument(
        "--param",
        metavar="-p",
        nargs="+",
        help="the parameters to investigate"
    )

    args = parser.parse_args()

    return args
