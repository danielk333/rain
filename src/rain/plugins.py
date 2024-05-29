import importlib
import pathlib
import sys

PLUGINS = {
    "set": {},
    "get": {},
    "sub": {}
}


def add_plugin(action, name, func, data_description):
    global PLUGINS
    if name not in PLUGINS[action]:
        PLUGINS[action][name] = {}
    PLUGINS[action][name]["function"] = func
    PLUGINS[action][name]["data_description"] = data_description


def register_plugin(action, name, data_description):
    def register_wrapper(func):
        add_plugin(action, name, func, data_description)
        return func

    return register_wrapper


def load_plugins(plugins_folder):
    ''' Loads the files in the plugins folder, making available the functions
        they contain

    Parameters
    ----------
    plugins_folder : Posix path
        The path to the folder containg the plugin files
    '''
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
