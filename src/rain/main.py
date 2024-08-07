from .cli import client_cli, server_cli
from .client import run_client
from .packaging import print_response
from .server import run_server


def rain_server():
    # INSERT YOUR ARGUMENT INPUT METHOD HERE
    # server_cli is a CLI you can use if you wish
    args = server_cli()

    # Add an output to this?
    run_server(args)

    return


def rain_client():
    # INSERT YOUR ARGUMENT INPUT METHOD HERE
    # client_cli is a CLI you can use if you wish
    args = client_cli()

    messages = run_client(args)

    # INSERT YOUR OUTPUT HANDLING METHOD HERE
    # Note that the output is a generator
    for message in messages:
        print_response(message)

    return
