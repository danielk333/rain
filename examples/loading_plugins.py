import rain
from pprint import pprint

config = rain.load_config("./rain.cfg")
rain.load_plugins(config.get("Plugins", "plugin_folder"))

pprint(rain.PLUGINS)

func = rain.PLUGINS["GET"]["hello"]

print("Calling function 'hello':")
pprint(func())
