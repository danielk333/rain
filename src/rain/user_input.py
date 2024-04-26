from pprint import pprint

from .decompose import load_groups


# TODO 20: Move the shutdown command to the server side
def determine_type(server_ip_address):
    print(f"Please enter the type of message you would like to send to {server_ip_address}:")
    message_type = input()

    return message_type


# TODO 19: Accept numerical inputs
def determine_group(folder, file_name):
    groups = load_groups(folder, file_name)
    for iter in range(len(groups)):
        print(f"{iter+1} - " + groups[iter]["group_name"])
    print("Please enter the parameter group you would like to access:")

    user_input = input()
    group_name = user_input
    for item in groups:
        if item["group_name"] == group_name:
            group = item

    return group, group_name


def params_request(group):
    print("Please enter a parameter you'd like to request:")
    pprint(group["parameters"], indent=4, sort_dicts=False)
    params = []
    input_param = input()
    params.append(input_param)
    input_continue = True
    while input_continue:
        print("Please enter another parameter you'd like to request:")
        print("Enter 'end' if there are none")
        input_param = input()
        if input_param == "end":
            input_continue = False
        else:
            for item in group["parameters"]:
                if item["name"] == input_param:
                    if item["request"] == "true":
                        params.append(input_param)
                        break
                    else:
                        print("This parameter is not requestable")

    return params


def params_command(group):
    print("Please enter a parameter you'd like to command:")
    pprint(group["parameters"], indent=4, sort_dicts=False)
    params = []
    new_values = []
    input_continue = False

    input_param = input()
    for item in group["parameters"]:
        if item["name"] == input_param:
            if item["command"] == "true":
                params.append(input_param)
                print("Please enter the value you would like to give this parameter:")
                input_value = input()
                new_values.append(input_value)
                input_continue = True
                break
            else:
                print("This parameter is not commandable")
                params = None

    while input_continue:
        print("Please enter another parameter you'd like to command:")
        print("Enter 'end' if there are none")
        input_param = input()
        if input_param == "end":
            input_continue = False
        else:
            for item in group["parameters"]:
                if item["name"] == input_param:
                    if item["command"] == "true":
                        params.append(input_param)
                        print("Please enter the value you would like to give this parameter:")
                        input_value = input()
                        new_values.append(input_value)
                        break
                    else:
                        print("This parameter is not commandable")
                        params = None

    return params, new_values
