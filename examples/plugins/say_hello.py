from pprint import pprint

from rain import register_plugin, PLUGINS

pprint(PLUGINS)


@register_plugin(
    action="get",
    name="hello",
)
def say_hello(message):
    response = {
        "data": "HELLO!",
        "message": message
    }
    return response


pprint(PLUGINS)
func = PLUGINS["get"]["hello"]
print("Calling function 'hello':")
response = func("test")
pprint(response)
