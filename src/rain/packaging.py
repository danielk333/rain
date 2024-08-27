import json
import logging
import sys
import copy
import socket as pys

from .fetch import get_datetime
from .plugins import PLUGINS

logger = logging.getLogger(__name__)


def form_request(message_type, params, data):
    ''' Creates the request message for the client to send to a server

    Parameters
    ----------
    message_type : string
        Whether the request is in the form of a GET or a SET command
    params : list of strings
        The parameters that are the subject of the request
    data : list of strings
        The data to transmit along with the parameters

    Returns
    -------
    request : JSON
        The formatted request to be sent by the client to the server
    '''
    date_time = get_datetime()
    request = {"sender": ""}
    request.update({
        "date": date_time[0],
        "time": date_time[1],
        "hostname": pys.gethostname(),
    })
    request.update({"action": message_type})
    request.update({"name": params})
    if request["action"] == "get":
        if data is None:
            request.update({"data": ["None"]*len(params)})
        else:
            if len(params) == len(data):
                request.update({"data": data})
            else:
                logger.error("Number of data values does not match the number of parameters")
                exit()
    elif request["action"] == "set":
        if data is None:
            logger.error("Number of data values does not match the number of parameters")
            exit()
        if len(params) == len(data):
            request.update({"data": data})
        else:
            logger.error("Number of data values does not match the number of parameters")
            exit()

    return request


def form_response(request, address):
    ''' Creates the response message following from the reception of a request
        from a client. This response message will later be sent to the client

    Parameters
    ----------
    request : JSON
        The request made by the client
    address : list of strings
        The hostname and port number of the server

    Returns
    -------
    response : JSON
        The formatted response to be sent by the server to the client
    '''
    date_time = get_datetime()
    response = {"sender": address[0]}
    response.update({"date": date_time[0],
                     "time": date_time[1]})
    response.update({"action": request["action"]})
    response.update({"name": request["name"]})

    data = []
    for ind, param in enumerate(request["name"]):
        try:
            func = PLUGINS[request["action"]][param]["function"]
        except KeyError:
            data.append(f"Parameter '{param}' invalid")
        else:
            request_copy = copy.deepcopy(request)
            request_copy["name"] = param
            request_copy["data"] = request["data"][ind]
            try:
                return_data = func(request_copy)
            except BaseException as e:
                return_data = f"Plugin failed with: {e}"
                logger.exception("Plugin failed")
            data.append(return_data)
    response.update({"data": data})

    return response


def form_failed(form, address):
    ''' Creates a failure response message, either because the server received
        a request that failed validation or because its response failed
        validation. This message needs to be sent as a REQ/REP socket requires
        both a request and a response to be transmitted, otherwise blocking
        will occur

    Parameters
    ----------
    form : string
        Whether the message that failed verification was a request or a
        response
    address : list of strings
        The hostname and port number of the server

    Returns
    -------
    response : JSON
        The formatted response to be sent by the server to the client
    '''
    date_time = get_datetime()
    response = {"sender": address[0],
                "date": date_time[0],
                "time": date_time[1],
                "action": "fail",
                "name": ["fail"]}
    if form == "request":
        response.update({"data": ["Request verification failed"]})
    elif form == "response":
        response.update({"data": ["Response verification failed"]})

    return response


def publish_update(param, value, address, current_datetime):
    ''' Creates a JSON blob containing the updated value of a parameter

    Parameters
    ----------
    param : string
        The parameter whose value has been updated
    value : string
        The new values this parameter has
    address : list of strings
        The hostname and port number of the server
    current_datetime : list of strings
        The server's current local date and time

    Returns
    -------
    update : JSON
        The update to be published by the server
    '''
    update = {"sender": address[0],
              "date": current_datetime[0],
              "time": current_datetime[1],
              "action": "sub",
              "name": param,
              "data": value}

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
    publish = f'{update["name"]}${json.dumps(update)}'

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
    print(json.dumps(response, indent=4, sort_keys=False))
    sys.stdout.flush()
