import os
import json


def load_server(path, server_name):
    server_address = []
    with open(os.path.join(path, f"{server_name}.info"), "r") as f:
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


def load_groups(path, file_name):
    with open(os.path.join(path, f"{file_name}.info"), "r") as f:
        data = f.read()
        end_found = False
        pos_list = []
        while not end_found:  # Until the document END is found
            start_found = False
            for char in range(len(data)):
                # Until the start of a parameter group has been found
                if not start_found:
                    if data[char] == '{':
                        if data[char+1] == '\n':
                            positions = []
                            positions.append(char)
                            start_found = True

                    # If no start to a parameter group, check for the END of the document
                    elif data[char:char+3] == 'END':
                        end_found = True

                # Now find the end of a parameter group
                if data[char] == ']':
                    if data[char+1:char+3] == '\n}':
                        positions.append(char+2)
                        pos_list.append(positions)
                        # Reset the value for the start of the parameter group
                        start_found = False

        groups = []
        for item in pos_list:
            params = data[item[0]:item[1]+1]
            groups.append(json.loads(params))

        return groups
