import json
from pprint import pprint


def find_group(message, groups):
    for item in groups:
        if item["group_name"] == message["group"]:
            group = item
            break

    return group


def load_groups(path, file_name):
    with open(path.joinpath(f"{file_name}.info"), "r") as f:
        data = f.read()
        end_found = False
        pos_list = []
        while not end_found:  # Until the document END is found
            start_found = False
            for char in range(len(data)):
                # Until the start of a parameter group has been found
                if not start_found:
                    if data[char] == '{':
                        if data[char+1] == '\n':
                            positions = []
                            positions.append(char)
                            start_found = True

                    # If no start to a parameter group, check for the END of the document
                    elif data[char:char+3] == 'END':
                        end_found = True

                # Now find the end of a parameter group
                if data[char] == ']':
                    if data[char+1:char+3] == '\n}':
                        positions.append(char+2)
                        pos_list.append(positions)
                        # Reset the value for the start of the parameter group
                        start_found = False

        groups = []
        for item in pos_list:
            params = data[item[0]:item[1]+1]
            groups.append(json.loads(params))

        return groups


def message_components(dir_info, server_name, message):
    response_type = message["type"]
    num_params = len(message["parameters"])
    groups = load_groups(dir_info, server_name)
    group = find_group(message, groups)

    return group, num_params, response_type


def pub_split(message):
    for char in range(len(message)):
        if message[char] == "$":
            break_point = char
            break
    actual_message = message[break_point+1:len(message)]

    return actual_message


def print_response(response):
    print("Server Response:")
    pprint(response, indent=4, sort_dicts=False)
