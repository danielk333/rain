import time
from .load import load_groups
from .data import load_data, change_data


def find_group(message, groups):
    for item in groups:
        if item["group_name"] == message["group"]:
            group = item
            break

    return group


def message_components(dir_info, server_name, message):
    response_type = message["type"]
    num_params = len(message["parameters"])
    groups = load_groups(dir_info, server_name)
    group = find_group(message, groups)

    return group, num_params, response_type


def action_request(message, group, num_params, server_name, dir_data):
    values = []
    for iter in range(num_params):
        for item in group["parameters"]:
            if item["name"] == message["parameters"][iter]:
                value = load_data(dir_data, server_name, message["parameters"][iter])
                values.append(value)
                break

    return values


def action_command(message, group, num_params, server_name, dir_data):
    for iter in range(num_params):
        for item in group["parameters"]:
            if item["name"] == message["parameters"][iter]:
                change_data(dir_data, server_name, message["parameters"][iter], message["new_values"][iter])

    return


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
