import os
import pathlib
from pprint import pprint

from rain import register_plugin, PLUGINS


@register_plugin(
    action="get",
    name="hyperdrive",
)
def get_hyp():
    HOME = pathlib.Path(os.path.expanduser("~"))
    DEFAULT_FOLDER = (HOME / "Documents" / "Studies" / "LTU" / "Thesis" / "rain").resolve()
    DATA_FODLER = DEFAULT_FOLDER / "data"
    with open(DATA_FODLER / "odyssey.data", "r") as f:
        for line in f:
            if "hyperdrive" in line:
                components = line.split(' : ')
                value = components[1]
                value = value[0:len(value)-1]
                break

    return value


pprint(PLUGINS)
func = PLUGINS["get"]["hyperdrive"]
print("Getting parameter 'hyperdrive':")
response = func()
pprint(response)
