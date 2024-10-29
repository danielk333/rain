# Messages

Messages are the packets of information exchanged between servers and clients.
These messages are in JSON format and have been given defined fields:

- `sender-name`: the name of the sender, as taken from the name its public key is stored in
- `sender-key`: the sender's public key, extracted from the established connection
- `datetime`: the date and time this message was formed, including timezone offset. This is in ISO 8601 format
- `action`: whether this message relates to a `GET`, `SET` or `SUB` request
- `name`: the name(s) of the requested parameter(s)
- `data`: any data value, such as parameter values (for responses) or additional request information

Every field is in the format of a string, with the `name` and `data` fields being lists of strings.
This means that numeric values must be converted to string.

Messages are automatically formatted by `rain` are also validated using validation schemas, provided by [JSON Schema](https://json-schema.org/).
These validation schemas check the structure of a message, ensuring that the required fields are presented and are of the correct data type.
The validation schemas do not verify the content of the messages, only the structure.
This means that if servers want to validate the content of the data field (in the case of a `SET` command for example), then users will need to implement this into their plugin functions.
Similar validation schemas could be used in a similar way to how `rain` uses them.

Below is an example message, a response to a `GET` request of a parameter called `herd_size` provided by the "reindeer" server:
```
{
    "sender-name": "reindeer",
    "sender-key": "N?</IPRcpG.aNx()nLiAMEO0LWzwWfb<0H?d{IVE",
    "datetime": "2024-10-29T22:25:09.633010+01:00",
    "action": "get",
    "name": [
        "herd_size"
    ],
    "data": [
        "10"
    ]
}

```
