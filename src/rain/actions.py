def load_data(path_data, server, req_param):
    with open(path_data / f"{server}.data", "r") as f:
        for line in f:
            if req_param in line:
                components = line.split(' : ')
                value = components[1]
                value = value[0:len(value)-1]
                break

    return value


def change_data(path_data, server, req_param, value):
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


def actions_get(request, params, server, path_data):
    values = []
    for iter in range(len(request["parameters"])):
        for item in params["parameters"]:
            if item["name"] == request["parameters"][iter]:
                value = load_data(path_data, server, item["name"])
                values.append(value)
                break

    return values


def actions_set(request, avail_params, server, path_data):
    for iter in range(len(request["parameters"])):
        for item in avail_params["parameters"]:
            if item["name"] == request["parameters"][iter]:
                change_data(path_data, server, item["name"], request["new_values"][iter])

    return
