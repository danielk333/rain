import time
from load import load_info
from data import load_data, change_data


def determine_response_type(message):
    response_type = message["type"]

    return response_type


def response_admin(message, server_open):
    response = "Shutting down the server"
    local_time = time.localtime()
    current_time = f"{local_time[3]:02}:{local_time[4]:02}:{local_time[5]:02} Local Time"
    response = {"type": message["type"],
                "response": response,
                "time": current_time}
    server_open = False

    return response, server_open


def response_request(dir_info, dir_data, server_name, message):
    info = load_info(dir_info, f"{server_name}.info")
    for item in info["parameters"]:
        if item["name"] == message["parameter"]:
            value = load_data(dir_data, server_name, message["parameter"])
            response = {"type": message["type"],
                        "parameter": message["parameter"],
                        "value": value}
            break

    return response


def response_command(dir_info, dir_data, server_name, message):
    info = load_info(dir_info, f"{server_name}.info")
    for item in info["parameters"]:
        if item["name"] == message["parameter"]:
            change_data(dir_data, server_name, message["parameter"], message["new_value"])
            response = {"type": "command",
                        "parameter": message["parameter"],
                        "new value": message["new_value"]}
            break

    return response


def form_response(message, response_type, server_open, server_name, dir_info, dir_data):
    if response_type == "admin":
        response, server_open = response_admin(message, server_open)
    elif response_type == "request":
        response = response_request(dir_info, dir_data, server_name, message)
    elif response_type == "command":
        response = response_command(dir_info, dir_data, server_name, message)

    return response, server_open
