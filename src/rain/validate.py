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

pub_schema = {}
