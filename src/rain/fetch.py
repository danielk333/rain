import json
import time

from .plugins import PLUGINS


def get_datetime():
    ''' Finds the current date and local time and return an array with these
        values

    Returns
    -------
    current_datetime : list of strings
        The current local date and time
    '''
    local_time = time.localtime()
    current_datetime = []
    current_datetime.append(f"{local_time[0]:04}-{local_time[1]:02}-{local_time[2]:02}")
    current_datetime.append(f"{local_time[3]:02}:{local_time[4]:02}:{local_time[5]:02} Local Time")

    return current_datetime


def sub_params():
    list_params = PLUGINS["sub"].keys()

    return list_params


def load_params(path_info, server):
    ''' Returns all parameters made available by the server, including whether
        each parameter can be requested, commanded or subscribed to

    Parameters
    ----------
    path_info : Posix path
        The path to the folder containing the server's info file
    server : string
        The name of the server

    Returns
    -------
    avail_params : JSON
        The parameters (and their details) provided by the server
    '''
    with open(path_info.joinpath(f"{server}.info"), "r") as f:
        data = f.read()
        start_found = False
        for char in range(len(data)):
            # Until the start of a parameter group has been found
            if not start_found:
                if data[char] == '{':
                    if data[char+1] == '\n':
                        positions = []
                        positions.append(char)
                        start_found = True

            # Now find the end of a parameter group
            if start_found:
                if data[char] == ']':
                    if data[char+1:char+3] == '\n}':
                        positions.append(char+2)

        avail_params = json.loads(data[positions[0]:positions[1]+1])

    return avail_params


def subscribable_params(path_info, server):
    ''' Returns the parameters provided by the server that a client can
        subscribe to

    Parameters
    ----------
    path_info : Posix path
        The path to the folder containing the server's info file
    server : string
        The name of the server
    '''
    subsc_params = []
    avail_params = load_params(path_info, server)
    for item in avail_params["parameters"]:
        if item["subscribe"] == "true":
            subsc_params.append(item["name"])

    return subsc_params
