from jsonschema import validate


def validate_request(request):
    validate(instance=request, schema=req_schema)


def validate_response(response):
    validate(instance=response, schema=rep_schema)


def validate_update(update):
    validate(instance=update, schema=pub_schema)


req_schema = {
    "type": "object",
    "description": "",
    "required": ["action", "name", "data"],
    "properties": {
        "sender": {
            "type": "string"
        },
        "datetime": {
            "type": "string",
            "description": "the date and time at message formation, including"
            + "timezone offset, according to the ISO 8601 standard"
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
        }
    }
}

rep_schema = {
    "type": "object",
    "description": "",
    "required": ["action", "name", "data"],
    "properties": {
        "sender": {
            "type": "string"
        },
        "datetime": {
            "type": "string",
            "description": "the date and time at message formation, including"
            + "timezone offset, according to the ISO 8601 standard"
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
        }
    }
}

pub_schema = {
    "type": "object",
    "description": "",
    "required": ["action", "name", "data"],
    "properties": {
        "sender": {
            "type": "string"
        },
        "datetime": {
            "type": "string",
            "description": "the date and time at message formation, including"
            + "timezone offset, according to the ISO 8601 standard"
        },
        "action": {
            "type": "string"
        },
        "name": {
            "type": "string"
        },
        "data": {
            "type": "string"
        }
    }
}
