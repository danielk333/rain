from .decompose import load_groups


def load_server(path, server_name):
    server_address = []
    with open(path.joinpath(f"{server_name}.info"), "r") as f:
        for line in f:
            if "Server" in line:
                ip_address = line.split(': ')[1]
                ip_address = ip_address[0:len(ip_address)-1]
                server_address.append(ip_address)
            elif "Port" in line:
                port = line.split(': ')[1]
                port = port[0:len(port)-1]
                server_address.append(port)

    return server_address


def subscribable_params(server_name, dir_info):
    possible_sub = []
    groups = load_groups(dir_info, server_name)
    for group in groups:
        for iter in range(len(group["parameters"])):
            if group["parameters"][iter]["subscribe"] == "true":
                possible_sub.append(group["parameters"][iter]["name"])

    return possible_sub
