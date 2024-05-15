from .decompose import load_params


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


def subscribable_params(path, name):
    subsc_params = []
    avail_params = load_params(path, name)
    for item in avail_params["parameters"]:
        if item["subscribe"] == "true":
            subsc_params.append(item["name"])

    return subsc_params
