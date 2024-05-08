import json

from .actions import actions_get, actions_set, load_data
from .user_input import params_get, params_set


def request_get(params, group_name):
    message = {"type": "get",
               "group": group_name,
               "parameters": params}

    return message


def request_set(params, new_values, group_name):
    message = {"type": "set",
               "group": group_name,
               "parameters": params,
               "new_values": new_values}

    return message


def form_request(message_type, group, group_name):
    if message_type == "get":
        params = params_get(group)
        if params:
            message = request_get(params, group_name)
            print(message)
    elif message_type == "set":
        params, new_values = params_set(group)
        if params:
            message = request_set(params, new_values, group_name)
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


def form_response(message, group, num_params, response_type, server_open, server_name, dir_data):
    if response_type == "get":
        values = actions_get(message, group, num_params, server_name, dir_data)
        response = response_get(message, values)
    elif response_type == "set":
        actions_set(message, group, num_params, server_name, dir_data)
        response = response_set(message)

    return response, server_open


def publish_update(param, value):
    update = {"parameter": param,
              "value": value}
    return update


def publish_format(update):
    response = f'{update["parameter"]}${json.dumps(update)}'

    return response


def publish_response(param, server_name, dir_data):
    value = load_data(dir_data, server_name, param)
    update = publish_update(param, value)
    response = publish_format(update)

    return response
