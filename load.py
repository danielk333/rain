import os
import json

home = os.path.dirname(__file__)
dir_info = os.path.join(home, 'infra_info')
# file_name = 'odyssey.info'

def load_info(path, file_name):
    with open(os.path.join(dir_info, file_name), 'r') as f:
        data = f.read()
        ## TODO 9: Also find the end of the parameters
        for char in range(len(data)):
            if data[char] == '{':
                if data[char+1] == '\n':
                    data = data[char:len(data)]
                    break
        info = json.loads(data)
    return info

def request_parameters(info, request):
    if info["request"] == "true":
        for item in info["parameters"]:
            if item["name"] == request:
                value = item["value"]
    else:
        print("This group of parameters cannot be requested")
        value = None

    return value
