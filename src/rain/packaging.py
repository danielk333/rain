import json
from pprint import pprint

from .actions import actions_get, actions_set, load_data
from .fetch import load_params


def request_get(req_params):
    request = {"type": "get",
               "parameters": req_params}

    return request


def request_set(req_params, new_values):
    request = {"type": "set",
               "parameters": req_params,
               "new_values": new_values}

    return request


def form_request(message_type, req_params, new_values):
    if message_type == "get":
        request = request_get(req_params)
        pprint(request, indent=4, sort_dicts=False)
    elif message_type == "set":
        request = request_set(req_params, new_values)
        pprint(request, indent=4, sort_dicts=False)
    else:
        request = None
        print("You have not entered a valid message type")

    return request


def response_get(request, values):
    response = {"type": "get",
                "parameters": request["parameters"],
                "values": values}

    return response


def response_set(request):
    response = {"type": "set",
                "parameters": request["parameters"],
                "new_values": request["new_values"]}

    return response


# TODO 47: Load parameters from somewhere other than an info file
def form_response(request, server, path_info, path_data):
    avail_params = load_params(path_info, server)
    if request["type"] == "get":
        values = actions_get(request, avail_params, server, path_data)
        response = response_get(request, values)
    elif request["type"] == "set":
        actions_set(request, avail_params, server, path_data)
        response = response_set(request)

    return response


def publish_update(sub_param, value):
    update = {"parameter": sub_param,
              "value": value}
    return update


def publish_format(update):
    publish = f'{update["parameter"]}${json.dumps(update)}'

    return publish


def publish_response(sub_param, server_name, dir_data):
    value = load_data(dir_data, server_name, sub_param)
    update = publish_update(sub_param, value)
    publish = publish_format(update)

    return publish


def pub_split(publish):
    [_, update] = publish.split('$', maxsplit=1)

    return update


def print_response(response):
    print("Server Response:")
    pprint(response, indent=4, sort_dicts=False)
