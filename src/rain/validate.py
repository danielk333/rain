from jsonschema import validate


def validate_reqrep(message):
    ''' Used to validate the structure of a client request or a server response
        using a validation schema

    Parameters
    ----------
    message : JSON
        The formatted message to be validated
    '''
    validate(instance=message, schema=reqrep_schema)


def validate_pub(message):
    ''' Used to validate the structure of a message from a Publish server using
        a validation schema

    Parameters
    ----------
    message : JSON
        The formatted message to be validated
    '''
    validate(instance=message, schema=pub_schema)


reqrep_schema = {
    "type": "object",
    "description": "",
    "required": ["action", "name", "data"],
    "properties": {
        "sender-name": {
            "type": "string"
        },
        "sender-key": {
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
        "sender-name": {
            "type": "string"
        },
        "sender-key": {
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
