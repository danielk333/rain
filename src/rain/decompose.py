import json
from pprint import pprint


def load_params(path_info, server):
    with open(path_info.joinpath(f"{server}.info"), "r") as f:
        data = f.read()
        start_found = False
        for char in range(len(data)):
            # Until the start of a parameter group has been found
            if not start_found:
                if data[char] == '{':
                    if data[char+1] == '\n':
                        positions = []
                        positions.append(char)
                        start_found = True

            # Now find the end of a parameter group
            if start_found:
                if data[char] == ']':
                    if data[char+1:char+3] == '\n}':
                        positions.append(char+2)

        avail_params = json.loads(data[positions[0]:positions[1]+1])

    return avail_params


def pub_split(publish):
    [_, update] = publish.split('$', maxsplit=1)

    return update


def print_response(response):
    print("Server Response:")
    pprint(response, indent=4, sort_dicts=False)
