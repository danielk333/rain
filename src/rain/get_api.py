import json
from .plugins import PLUGINS, register_plugin


@register_plugin(
    action="get",
    name="api",
    data_description="api description description",
)
def generate_api():
    api = {
        action: [
            {"name": key, "data_description": plug["data_description"]}
            for key, plug in PLUGINS[action].items()
        ]
        for action in PLUGINS
    }
    return json.dumps(api, indent=4)