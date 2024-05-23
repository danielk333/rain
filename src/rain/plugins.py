import pathlib
import importlib
import sys

PLUGINS = {
    "set": {},
    "get": {},
}


def add_plugin(action, name, func):
    global PLUGINS
    PLUGINS[action][name] = func


def register_plugin(action, name):
    def register_wrapper(func):
        add_plugin(action, name, func)
        return func

    return register_wrapper


def load_plugins(plugins_folder):

    if not isinstance(plugins_folder, pathlib.Path):
        plugins_folder = pathlib.Path(plugins_folder)

    if plugins_folder.exists():
        prev_sys_path = sys.path.copy()
        sys.path = [str(plugins_folder)] + sys.path
        for item in plugins_folder.iterdir():
            if item.is_file() and item.suffix == '.py':
                importlib.import_module(item.stem)
            elif item.is_dir() and (item / '__init__.py').is_file():
                importlib.import_module(item.stem)
        sys.path = prev_sys_path
