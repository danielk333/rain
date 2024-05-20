import json
from pprint import pprint

from .actions import actions_get, actions_set, load_data
from .fetch import load_params


def request_get(req_params):
    ''' Forms the request to send in the case of a GET command

    Parameters
    ----------
    req_params : list of strings
        The parameters whose values have been requested

    Returns
    -------
    request : JSON
        The formatted request to be sent by the client to the server
    '''
    request = {"type": "get",
               "parameters": req_params}

    return request


def request_set(req_params, new_values):
    ''' Forms the request to send in the case of a SET command

    Parameters
    ----------
    req_params : list of strings
        The parameters whose values are to be changed
    new_values : list of strings
        The values to assign to req_params

    Returns
    -------
    request : JSON
        The formatted request to be sent by the client to the server
    '''
    request = {"type": "set",
               "parameters": req_params,
               "new_values": new_values}

    return request


def form_request(message_type, req_params, new_values):
    ''' A higher level function that handles the forming of a request in the
        case where a client makes a request to a server

    Parameters
    ----------
    message_type : string
        Whether the request is in the form of a GET or a SET command
    req_params : list of strings
        The parameters that are the subject of the request
    new_values : list of string
        The values to assign to req_params in the event of a SET command,
        else None

    Returns
    -------
    request : JSON
        The formatted request to be sent by the client to the server
    '''
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
    ''' Forms the response to send in the case of a GET command

    Parameters
    ----------
    request : JSON
        The request made by the client
    values : list of strings
        The values of the parameters requested by the client

    Returns
    -------
    response : JSON
        The formatted response to be sent by the server to the client
    '''
    response = {"type": "get",
                "parameters": request["parameters"],
                "values": values}

    return response


def response_set(request):
    ''' Forms the response to send in the case of a SET command

    Parameters
    ----------
    request : JSON
        The request made by the client

    Returns
    -------
    response : JSON
        The formatted response to be sent by the server to the client
    '''
    response = {"type": "set",
                "parameters": request["parameters"],
                "new_values": request["new_values"]}

    return response


# TODO 47: Load parameters from somewhere other than an info file
def form_response(request, server, path_info, path_data):
    ''' A higher level function that handles the forming of a response in the
        case where a client makes a request to a server

    Parameters
    ----------
    request : JSON
        The request made by the client
    server : string
        The name of the server
    path_info : Posix path
        The path to the folder containing the server's info file
    path_data : Posix path
        The path to the folder containing the server's data file

    Returns
    -------
    response : JSON
        The formatted response to be sent by the server to the client
    '''
    avail_params = load_params(path_info, server)
    if request["type"] == "get":
        values = actions_get(request, avail_params, server, path_data)
        response = response_get(request, values)
    elif request["type"] == "set":
        actions_set(request, avail_params, server, path_data)
        response = response_set(request)

    return response


def publish_update(sub_param, value):
    ''' Creates a JSON blob containing the updated value of a parameter

    Parameters
    ----------
    sub_param : string
        The parameter whose value has been updated
    value : string
        The new values this parameter has

    Returns
    -------
    update : JSON
        The update to be published by the server
    '''
    update = {"parameter": sub_param,
              "value": value}
    return update


def publish_format(update):
    ''' Converts the JSON update into a string and adds the parameter name and
        an extra character as a prefix, in order for the update to be detected
        by the client's filter

    Parameters
    ----------
    update : JSON
        The update to be published by the server

    Returns
    -------
    publish : string
        The reformatted update to be published by the server
    '''
    publish = f'{update["parameter"]}${json.dumps(update)}'

    return publish


def publish_response(sub_param, server, path_data):
    ''' A higher level function that handles the formatting of an update for
        the server to publish

    Parameters
    ----------
    sub_param : string
        The name of the parameter whose value has just changed
    server : string
        The name of the server
    path_data : Posix path
        The path to the folder containing the server's data file
    '''
    value = load_data(path_data, server, sub_param)
    update = publish_update(sub_param, value)
    publish = publish_format(update)

    return publish


def pub_split(publish):
    ''' Removes the prefix to the update published by the server, in order to
        recover only the JSON data

    Parameters:
    -----------
    publish : string
        The formatted update published by the server

    Returns
    -------
    update : JSON
        The JSON data containing the updated parameter
    '''
    [_, update] = publish.split('$', maxsplit=1)

    return update


def print_response(response):
    ''' Prints a message sent by the server to the client in a nicer format

    Parameters
    ----------
    response : JSON
        The message sent by the server to the client
    '''
    print("Server Response:")
    pprint(response, indent=4, sort_dicts=False)
