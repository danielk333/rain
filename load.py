import os
import json
from pprint import pprint

home = os.path.dirname(__file__)
dir_info = os.path.join(home, 'infra_info')
# file_name = 'odyssey.info'

def load_info(path, file_name):
    with open(os.path.join(dir_info, file_name), 'r') as f:
        data = f.read()
        for char in range(len(data)):
            if data[char] == '{':
                data = data[char:len(data)]
                break
        info = json.loads(data)
        # pprint(info, indent=4, sort_dicts=False, depth=4)
        # parameters = info["parameters"]
        # pprint(parameters, indent=4, sort_dicts=False)
        # print(parameters[0]["name"] == "thrusters")
        # for item in parameters:
        #     if item["name"] == "hyperdrive" and info["request"] == "true":
        #         print(item["value"])
    return info#, parameters

def request_parameters(info, request):
    if info["request"] == "true":
        for item in info["parameters"]:
            if item["name"] == request:
                value = item["value"]
    else:
        print("This group of parameters cannot be requested")
        value = None

    return value

#
# print("Please enter a command:")
# prompt = input()
# if prompt == "request":
#     info = load_info(dir_info, file_name)
#     pprint(info["parameters"], indent=4, sort_dicts=False)
#     print("Please enter a parameter to request:")
#     request = input()
#     value = request_parameters(info, request)
#     print(f"Value of {request}: {value}")
