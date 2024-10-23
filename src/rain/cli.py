import argparse
import pathlib

from .register import rain_register
from .trigger import rain_trigger
from .client import run_client
from .packaging import print_response
from .server import run_server

# TODO 44: Improve the layout of the --help command


def register_cli():
    ''' The CLI used for registering an instrument to RAIN

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


def trigger_cli():
    ''' The CLI used server-side to trigger a trigger parameter

    Returns
    -------
    args: Namespace
        The command line arguments entered by the user
    '''
    parser = argparse.ArgumentParser(
        prog="RAIN",
        description="RAIN Trigger Interface"
    )

    parser.add_argument(
        "name",
        help="the name of the trigger to send"
    )

    parser.add_argument(
        "value",
        help="the value assigned to this trigger"
    )

    parser.add_argument(
        "-c", "--cfgpath",
        type=pathlib.PosixPath,
        help="the path to your RAIN config folder"
    )

    args = parser.parse_args()

    rain_trigger(args)


def server_cli():
    ''' The CLI to start a RAIN server

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
        "host",
        choices=["rep", "pub"],
        help="the type of message the server will send"
    )

    parser.add_argument(
        "-a", "--auth",
        action="store_false",
        help="disables authentication for publish servers"
    )

    parser.add_argument(
        "-c", "--cfgpath",
        type=pathlib.PosixPath,
        help="the path to your RAIN config folder"
    )

    parser.add_argument(
        "-l", "--logfile",
        default=None,
        help="the path to the logfile, including its name"
    )

    parser.add_argument(
        "-o", "--logprint",
        action="store_true",
        help="whether to print logs to the console"
    )

    parser.add_argument(
        "-v", "--loglevel",
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="the main logging level (first filter)"
    )

    parser.add_argument(
        "-vl", "--filelevel",
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=None,
        help="the logging level of the logfile"
    )

    parser.add_argument(
        "-vo", "--printlevel",
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=None,
        help="the logging level of the print logging"
    )

    args = parser.parse_args()

    run_server(args)


def client_cli():
    ''' The CLI to start a RAIN client

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
        "-s", "--suppress",
        action="store_true",
        help="whether to suppress return message printing to stdout"
    )

    parser.add_argument(
        "-c", "--cfgpath",
        type=pathlib.PosixPath,
        help="the path to your RAIN config folder"
    )

    parser.add_argument(
        "-l", "--logfile",
        default=None,
        help="the path to the logfile, including its name"
    )

    parser.add_argument(
        "-o", "--logprint",
        action="store_true",
        help="whether to print logs to the console"
    )

    parser.add_argument(
        "-v", "--loglevel",
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="the main logging level (first filter)"
    )

    parser.add_argument(
        "-vl", "--filelevel",
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="the logging level of the logfile"
    )

    parser.add_argument(
        "-vo", "--printlevel",
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="the logging level of the print logging"
    )

    parser.add_argument(
        "server",
        help="the name of the server to connect to"
    )

    subparsers = parser.add_subparsers(
        title="RAIN Actions",
        dest="action"
    )

    parser_get = subparsers.add_parser(
        "get",
        help="get the values of parameters"
    )
    parser_get.add_argument(
        "param",
        nargs="+",
        help="the parameter(s) to get"
    )
    parser_get.add_argument(
        "-d", "--data",
        nargs="*",
        default=None,
        help="data to request alongside a parameter"
    )

    parser_set = subparsers.add_parser(
        "set",
        help="set the values of parameters"
    )
    parser_set.add_argument(
        "param",
        nargs="+",
        help="the parameter(s) to set"
    )
    parser_set.add_argument(
        "-d", "--data",
        nargs="*",
        help="data to request alongside a parameter"
    )

    parser_sub = subparsers.add_parser(
        "sub",
        help="subscribe to the values of parameters"
    )
    parser_sub.add_argument(
        "-a", "--auth",
        action="store_false",
        help="disables authentication for publish servers"
    )
    parser_sub.add_argument(
        "-c", "--changes",
        action="append",
        help="subscribe to a change in a parameter"
    )
    parser_sub.add_argument(
        "-f", "--freq",
        action="append",
        help="subscribe to all values of a parameter"
    )
    parser_sub.add_argument(
        "-t", "--trigger",
        action="append",
        help="subscribe to a triggered parameter"
    )

    args = parser.parse_args()

    messages = run_client(args)

    prev_values = []
    if args.action == "sub":
        if args.changes is not None:
            for item in args.changes:
                prev_values.append([item, ""])

    for message in messages:
        if args.action == "sub":
            if args.changes is not None:
                if message["name"] in args.changes:
                    for item in range(len(prev_values)):
                        if prev_values[item][0] == message["name"]:
                            index = item
                    if message["data"] != prev_values[index][1]:
                        prev_values[index][1] = message["data"]
                        if not args.suppress:
                            print_response(message)
                else:
                    if not args.suppress:
                        print_response(message)
            else:
                if not args.suppress:
                    print_response(message)
        else:
            if not args.suppress:
                print_response(message)
