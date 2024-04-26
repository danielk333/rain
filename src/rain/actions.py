import os

# TODO 27: Rename the packaging functions


def load_data(path, file_name, parameter):
    with open(os.path.join(path, f"{file_name}.data"), "r") as f:
        for line in f:
            if parameter in line:
                components = line.split(' : ')
                value = components[1]
                value = value[0:len(value)-1]
                break

    return value


def change_data(path, file_name, param, value):
    with open(os.path.join(path, f"{file_name}.data"), "r") as f:
        lines = []
        for line in f:
            if param in line:
                line_to_change = line
                components = line_to_change.split(" : ")
                new_line = components[0] + " : " + value + "\n"
                lines.append(new_line)
            else:
                lines.append(line)

    with open(os.path.join(path, f"{file_name}.data"), "w") as f:
        for item in lines:
            f.write(item)

    return


def action_request(message, group, num_params, server_name, dir_data):
    values = []
    for iter in range(num_params):
        for item in group["parameters"]:
            if item["name"] == message["parameters"][iter]:
                value = load_data(dir_data, server_name, message["parameters"][iter])
                values.append(value)
                break

    return values


def action_command(message, group, num_params, server_name, dir_data):
    for iter in range(num_params):
        for item in group["parameters"]:
            if item["name"] == message["parameters"][iter]:
                change_data(dir_data, server_name, message["parameters"][iter], message["new_values"][iter])

    return
