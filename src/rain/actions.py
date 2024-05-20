def load_data(path_data, server, req_param):
    ''' Finds the value of a parameter in the server's data file

    Parameters
    ----------
    path_data : Posix path
        The path to the folder containing the server's data file
    server : string
        The name of the server
    req_param : string
        The name of the parameter whose value is requested

    Returns
    -------
    value : string
        The value of the requested parameter
    '''
    with open(path_data / f"{server}.data", "r") as f:
        for line in f:
            if req_param in line:
                components = line.split(' : ')
                value = components[1]
                value = value[0:len(value)-1]
                break

    return value


def change_data(path_data, server, req_param, value):
    ''' Changes the value of a parameter in the server's data file

    Parameters
    ----------
    path_data : Posix path
        The path to the folder containing the server's data file
    server : string
        The name of the server
    req_param : string
        The name of the parameter whose value is to changed
    value : string
        The new value to give this parameter
    '''
    with open(path_data / f"{server}.data", "r") as f:
        lines = []
        for line in f:
            if req_param in line:
                line_to_change = line
                components = line_to_change.split(" : ")
                new_line = components[0] + " : " + value + "\n"
                lines.append(new_line)
            else:
                lines.append(line)

    with open(path_data / f"{server}.data", "w") as f:
        for item in lines:
            f.write(item)

    return


def actions_get(request, avail_params, server, path_data):
    ''' Finds the current values of the requested parameters, as a response to
        a GET command

    Parameters
    ----------
    request : JSON
        The JSON GET message received by the server
    avail_params : JSON
        The list of parameters made available by the server
    server : string
        The name of the server
    path_data : Posix path
        The path to the folder containing the server's data file

    Returns
    -------
    values : list of strings
        The current values of the requested parameters
    '''
    values = []
    for iter in range(len(request["parameters"])):
        for item in avail_params["parameters"]:
            if item["name"] == request["parameters"][iter]:
                value = load_data(path_data, server, item["name"])
                values.append(value)
                break

    return values


def actions_set(request, avail_params, server, path_data):
    ''' Changes the values of the requested parameters, as a response to a SET
        command

    Parameters
    ----------
    request : JSON
        The JSON GET message received by the server
    avail_params : JSON
        The list of parameters made available by the server
    server : string
        The name of the server
    path_data : Posix path
        The path to the folder containing the server's data file
    '''
    for iter in range(len(request["parameters"])):
        for item in avail_params["parameters"]:
            if item["name"] == request["parameters"][iter]:
                change_data(path_data, server, item["name"], request["new_values"][iter])

    return
