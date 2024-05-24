import argparse
import pathlib

from .client import rain_client
from .register import rain_register
from .server import rain_server

# TODO 44: Improve the layout of the --help command


def client_cli():
    ''' The CLI for a user wanting to use the client side of RAIN

    Returns
    -------
    args : Namespace
        The command line arguments entered by the user
    '''
    parser = argparse.ArgumentParser(
        prog="RAIN",
        description="RAIN Client Interface"
    )

    parser.add_argument(
        "-c", "--cfgpath",
        help="the path to your RAIN config folder"
    )

    subparsers = parser.add_subparsers(
        title="RAIN Interactions",
        description="List of interactions",
        dest='interaction'
    )

    parser_get = subparsers.add_parser(
        'get',
        help='get the values of parameters'
    )
    parser_get.add_argument(
        "server",
        help="the instrument server to connect to"
    )
    parser_get.add_argument(
        'param',
        nargs='+',
        help='the parameters to get'
    )

    parser_set = subparsers.add_parser(
        'set',
        help='set the values of parameters'
    )
    parser_set.add_argument(
        "server",
        help="the instrument server to connect to"
    )
    parser_set.add_argument(
        '-p',
        action='append',
        nargs=2,
        help='the parameter to set and the value to set it to'
    )

    parser_sub = subparsers.add_parser(
        'sub',
        help='subscribe to the values of parameters'
    )
    parser_sub.add_argument(
        "server",
        help="the instrument server to connect to"
    )
    parser_sub.add_argument(
        'param',
        nargs='+',
        help='the parameters to subscribe to'
    )

    args = parser.parse_args()

    rain_client(args)

    return


def server_cli():
    ''' The CLI for a user wanting to use the server side of RAIN

    Returns
    -------
    args: Namespace
        The command line arguments entered by the user
    '''
    parser = argparse.ArgumentParser(
        prog="RAIN",
        description="RAIN Server Interface"
    )

    parser.add_argument(
        "interaction",
        choices=["rep", "pub"],
        help="the type of interaction with the server"
    )

    parser.add_argument(
        "instrument",
        help="the instrument server to connect to"
    )

    parser.add_argument(
        "-c", "--cfgpath",
        help="the path to your RAIN config folder"
    )

    args = parser.parse_args()

    rain_server(args)

    return


def new_user_cli():
    ''' The CLI for users who want to register an instrument to RAIN

    Returns
    -------
    args : Namespace
        The command line arguments entered by the user
    '''
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

    parser.add_argument(
        "-c", "--cfgpath",
        type=pathlib.PosixPath,
        help="the path to your RAIN config folder"
    )

    parser.add_argument(
        "-k", "--keypath",
        type=pathlib.PosixPath,
        help="the path to your keypair folder"
    )

    args = parser.parse_args()

    rain_register(args)

    return
