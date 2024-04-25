import os

# TODO 25: Combine the data and actions functions into one file


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
