from jsonschema import validate


def validate_request(request):
    if request["action"] == "get":
        validate(instance=request, schema=get_req_schema)
    elif request["action"] == "set":
        validate(instance=request, schema=set_req_schema)


def validate_response(response):
    if response["action"] == "get":
        validate(instance=response, schema=get_rep_schema)
    elif response["action"] == "set":
        validate(instance=response, schema=set_rep_schema)


def validate_update(update):
    validate(instance=update, schema=pub_schema)


set_req_schema = {
    "type": "object",
    "description": "",
    "required": ["action", "name", "data"],
    "properties": {
        "action": {
            "type": "string"
        },
        "name": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "data": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "data_description": {
            "type": "string"
        }
    }
}

set_rep_schema = {
    "type": "object",
    "description": "",
    "required": ["action", "name", "data"],
    "properties": {
        "date": {
            "type": "string",
            "description": "https://www.iso.org/iso-8601-date-and-time-format.html"
        },
        "time": {
            "type": "string",
            "description": "https://www.iso.org/iso-8601-date-and-time-format.html"
        },
        "action": {
            "type": "string"
        },
        "name": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "data": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "data_description": {
            "type": "string"
        }
    }
}

get_req_schema = {
    "type": "object",
    "description": "",
    "required": ["action", "name"],
    "properties": {
        "action": {
            "type": "string"
        },
        "name": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    }
}

get_rep_schema = {
    "type": "object",
    "description": "",
    "required": ["action", "name", "data"],
    "properties": {
        "action": {
            "type": "string"
        },
        "name": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "data": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "data_description": {
            "type": "string"
        }
    }
}

pub_schema = {
    "type": "object",
    "description": "",
    "required": ["action", "name", "data"],
    "properties": {
        "date": {
            "type": "string",
            "description": "https://www.iso.org/iso-8601-date-and-time-format.html"
        },
        "time": {
            "type": "string",
            "description": "https://www.iso.org/iso-8601-date-and-time-format.html"
        },
        "action": {
            "type": "string"
        },
        "name": {
            "type": "string"
        },
        "data": {
            "type": "string"
        },
        "data_description": {
            "type": "string"
        }
    }
}
