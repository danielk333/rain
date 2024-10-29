# Server plugins

When a client sends a request, the server needs to be able to access the relevant data so that it can form a response.
As `rain` is meant to be a general software, packaged identically for all users, server-specific implementations are impossible.
However, a plugin system has been implemented, allowing `rain` to call a server-defined function that provides the correct data.

Let's illustrate this with an example, where a server provides a parameter called `herd_size` that clients that request the value of in the form of a GET request.
The user who runs the server needs to write a Python function that will be able to find the value of `herd_size` when a client request is received.
This function needs to be wrapped with a decorator, in this case `register_response`, which saves this function as being the relevant one for this parameter for this type of request.
This plugin function is stored in a Python file in the `plugins` folder in the server's configuration folder.
This means that plugin functions are kept outside of `rain`'s source code.

Please note that if the plugin function raises an error, this error will be added to the data field in the response sent to the client.
Please be aware of this when writing your plugin functions, as the error transmitted to a client could give an indication of how the server's systems operate.
This may be a concern for you, depending on your systems.

## Response server

Response servers need to create plugin functions in order to form responses to `SET` and `GET` requests.
There are restrictions on the inputs and outputs of these functions:

- `GET` requests: must accept only the request as an input and return only the value of the parameter
- `SET` requests: must accept only the request as an input and return nothing

The decorators used to wrap the functions is the same for both request types, taking the following arguments:

- `action`: the request type (`get` or `set`)
- `name`: the name of the parameter this function relates to
- `data_description`: a description what the parameter represents, the data type (int, boolean, string, etc), the units of this data, and potentially the range of expected values

An example of how this all fits together can be seen in the example below:
```
@register_response(
    action="get",
    name="herd_size",
    data_description="the description of this parameter, include the type, unit and range of values"
)
def function_name(request):
    # Code that finds the value of the requested parameter

    return value
```

## Publish server

Publish servers need to create plugin functions in order to form updates to publish to subscribed clients.
There are two types of parameters clients can subscribe to: timed parameters (whose values are published frequently) and trigger parameters (whose values are updated sporadically, only when the associated events occur).
The plugin functions differ between the two types of parameters.

For timed parameters, the plugin functions must accept only the name of the parameter as an input and return only the value of the parameter.
These functions are decorated using a function taking the following arguments:

- `action`: the request type (`sub`)
- `name`: the name of the parameter this function relates to
- `interval`: the time between updates (in seconds)
- `data_description`: a description what the parameter represents, the data type (int, boolean, string, etc), the units of this data, and potentially the range of expected values

For trigger parameters, the decorator is called as a normal function, without an associated function to decorate.
This function takes the following arguments:

- `name`: the name of the parameter this function relates to
- `data_description`: a description what the parameter represents, the data type (int, boolean, string, etc), the units of this data, and potentially the range of expected values

Below is an example of how plugin functions for timed parameters are laid out, using the same example as above:
```
@register_publish(
    action="sub",
    name="herd_size",
    interval=5,
    data_description="the description of this parameter, include the type, unit and range of values"
)
def function_name(param_name):
    # Code that finds the value of param_name

    return value
```

And for trigger parameters:
```
register_trigger(
    name="trigger_name",
    data_description="the description of this parameter, include the type, unit and range of values"
)
```

## Examples

Example files containing example plugin functions can be found in `examples/plugins`.
