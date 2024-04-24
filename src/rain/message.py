from load import load_info
from pprint import pprint


def determine_type(server_ip_address):
    print(f"Please enter the type of message you would like to send to {server_ip_address}:")
    message_type = input()

    return message_type


def form_admin():
    print("Please enter the admin command you'd like to enter:")
    command = input()
    if command == "shutdown":
        message = {"type": "admin",
                   "command": "shutdown"}
    else:
        print("You have entered an invalid admin command")
        message = None

    return message


def form_request(dir_info, server_name):
    info = load_info(dir_info, f"{server_name}.info")
    pprint(info["parameters"], indent=4, sort_dicts=False)
    print("\nPlease enter the parameter you would like to request:")
    param = input()
    for item in info["parameters"]:
        if item["name"] == param:
            if item["request"] == "true":
                message = {"type": "request",
                           "parameter": param}
                break
            else:
                message = None
                print("This parameter is not requestable")
                break

    return message


def form_command(dir_info, server_name):
    info = load_info(dir_info, f"{server_name}.info")
    pprint(info["parameters"], indent=4, sort_dicts=False)
    print("\nPlease enter the parameter you would like to command:")
    param = input()
    for item in info["parameters"]:
        if item["name"] == param:
            if item["command"] == "true":
                print("Please enter the value you would like to give this parameter:")
                new_value = input()
                message = {"type": "command",
                           "parameter": param,
                           "new_value": new_value}
                break

    return message


def form_message(message_type, dir_info, server_name):
    if message_type == "admin":
        message = form_admin()
    elif message_type == "request":
        message = form_request(dir_info, server_name)
    elif message_type == "command":
        message = form_command(dir_info, server_name)
    else:
        message = None
        print("You have not entered a valid message type")

    return message


def print_response(response):
    print("Server Response:")
    pprint(response, indent=4, sort_dicts=False)
