from jsonschema import validate


def validate_request(request):
    if request["action"] == "get":
        validate(instance=request, schema=req_get_schema)
    elif request["action"] == "set":
        validate(instance=request, schema=req_set_schema)


def validate_response(response):
    validate(instance=response, schema=rep_schema)


def validate_update(update):
    validate(instance=update, schema=pub_schema)


req_get_schema = {
    "type": "object",
    "description": "",
    "required": ["action", "name"],
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
        }
    }
}

req_set_schema = {
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

rep_schema = {
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
