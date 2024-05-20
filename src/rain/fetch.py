import json


def load_server(path, name):
    address = []
    with open(path.joinpath(f"{name}.info"), "r") as f:
        for line in f:
            if "Server" in line:
                hostname = line.split(': ')[1]
                hostname = hostname[0:len(hostname)-1]
                address.append(hostname)
            elif "Port" in line:
                port = line.split(': ')[1]
                port = port[0:len(port)-1]
                address.append(port)

    return address


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
