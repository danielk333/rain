import time

from .user_input import params_get, params_set
from .actions import actions_get, actions_set


def message_get(params, group_name):
    message = {"type": "get",
               "group": group_name,
               "parameters": params}

    return message


def message_set(params, new_values, group_name):
    message = {"type": "set",
               "group": group_name,
               "parameters": params,
               "new_values": new_values}

    return message


def message_admin():
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
        message = message_admin()
    elif message_type == "get":
        params = params_get(group)
        if params:
            message = message_get(params, group_name)
            print(message)
    elif message_type == "set":
        params, new_values = params_set(group)
        if params:
            message = message_set(params, new_values, group_name)
            print(message)
    else:
        message = None
        print("You have not entered a valid message type")

    return message


def response_get(message, values):
    response = {"type": "get",
                "group": message["group"],
                "parameters": message["parameters"],
                "values": values}

    return response


def response_set(message):
    response = {"type": "set",
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
    elif response_type == "get":
        values = actions_get(message, group, num_params, server_name, dir_data)
        response = response_get(message, values)
    elif response_type == "set":
        actions_set(message, group, num_params, server_name, dir_data)
        response = response_set(message)

    return response, server_open
