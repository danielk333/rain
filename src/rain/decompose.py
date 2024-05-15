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


# TODO 42: Rework the request_components function
def request_components(path_info, server, request):
    response_type = request["type"]
    avail_params = load_params(path_info, server)

    return avail_params, response_type


# TODO 43: Rework the pub_split function
def pub_split(publish):
    for char in range(len(publish)):
        if publish[char] == "$":
            break_point = char
            break
    update = publish[break_point+1:len(publish)]

    return update


def print_response(response):
    print("Server Response:")
    pprint(response, indent=4, sort_dicts=False)
