from rain import register_plugin


@register_plugin(
    action="get",
    name="hello",
)
def say_hello(message):
    return {
        "data": "HELLO!"
    }
