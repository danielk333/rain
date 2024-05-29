import json
from pprint import pprint

from .fetch import get_datetime
from .plugins import PLUGINS
from .validate import validate_request, validate_response, validate_update


def form_request(message_type, req_params):
    ''' Creates the request message for the client to send to a server

    Parameters
    ----------
    message_type : string
        Whether the request is in the form of a GET or a SET command
    req_params : list of strings
        The parameters that are the subject of the request

    Returns
    -------
    request : JSON
        The formatted request to be sent by the client to the server
    '''
    request = {"action": message_type}
    if message_type == "get":
        request.update({"name": req_params})
    if message_type == "set":
        names = []
        values = []
        for name, value in req_params:
            names.append(name)
            values.append(value)
        request.update({"name": names})
        request.update({"data": values})
    validate_request(request)
    pprint(request, indent=4, sort_dicts=False)

    return request


def form_response(request):
    ''' Creates the response message following from the reception of a request
        from a client. This response message will later be sent to the client

    Parameters
    ----------
    request : JSON
        The request made by the client

    Returns
    -------
    response : JSON
        The formatted response to be sent by the server to the client
    '''
    date_time = get_datetime()
    response = {"date": date_time[0],
                "time": date_time[1]}

    if request["action"] == "get":
        validate_request(request)

        response.update({"action": "get"})
        response.update({"name": request["name"]})
        data = []
        for param in request["name"]:
            func = PLUGINS["get"][param]["function"]
            data.append(func())
        response.update({"data": data})

    elif request["action"] == "set":
        validate_request(request)

        response.update({"action": "set"})
        response.update({"name": request["name"]})
        data = []
        for item, value in zip(request["name"], request["data"]):
            func = PLUGINS["set"][item]["function"]
            response_value = func(value)
            data.append(response_value)
        response.update({"data": data})

    validate_response(response)

    return response


def publish_update(sub_param, value, current_datetime):
    ''' Creates a JSON blob containing the updated value of a parameter

    Parameters
    ----------
    sub_param : string
        The parameter whose value has been updated
    value : string
        The new values this parameter has
    current_datetime : list of strings
        The server's current local date and time

    Returns
    -------
    update : JSON
        The update to be published by the server
    '''
    update = {"date": current_datetime[0],
              "time": current_datetime[1],
              "parameter": sub_param,
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


def publish_response(sub_param):
    ''' A higher level function that handles the formatting of an update for
        the server to publish

    Parameters
    ----------
    sub_param : string
        The name of the parameter whose value has just changed
    '''
    func = PLUGINS["sub"][sub_param]["function"]
    value = func()
    date_time = get_datetime()
    update = publish_update(sub_param, value, date_time)
    validate_update(update)
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
    update = json.loads(update)

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
