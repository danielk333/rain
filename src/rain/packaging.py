import time

from .user_input import params_request, params_command
from .actions import action_request, action_command

# TODO 27: Rename the packaging functions


def form_request(params, group_name):
    message = {"type": "request",
               "group": group_name,
               "parameters": params}

    return message


def form_command(params, new_values, group_name):
    message = {"type": "command",
               "group": group_name,
               "parameters": params,
               "new_values": new_values}

    return message


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


def form_message(message_type, group, group_name):
    if message_type == "admin":
        message = form_admin()
    elif message_type == "request":
        params = params_request(group)
        if params:
            message = form_request(params, group_name)
            print(message)
    elif message_type == "command":
        params, new_values = params_command(group)
        if params:
            message = form_command(params, new_values, group_name)
            print(message)
    else:
        message = None
        print("You have not entered a valid message type")

    return message


def response_request(message, values):
    response = {"type": "command",
                "group": message["group"],
                "parameters": message["parameters"],
                "values": values}

    return response


def response_command(message):
    response = {"type": "command",
                "group": message["group"],
                "parameters": message["parameters"],
                "new_values": message["new_values"]}

    return response


def response_admin(message, server_open):
    response = "Shutting down the server"
    local_time = time.localtime()
    current_time = f"{local_time[3]:02}:{local_time[4]:02}:{local_time[5]:02} Local Time"
    response = {"type": message["type"],
                "response": response,
                "time": current_time}
    server_open = False

    return response, server_open


def form_response(message, group, num_params, response_type, server_open, server_name, dir_data):
    if response_type == "admin":
        response, server_open = response_admin(message, server_open)
    elif response_type == "request":
        values = action_request(message, group, num_params, server_name, dir_data)
        response = response_request(message, values)
    elif response_type == "command":
        action_command(message, group, num_params, server_name, dir_data)
        response = response_command(message)

    return response, server_open
