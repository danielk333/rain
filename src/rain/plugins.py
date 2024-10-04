import importlib
import pathlib
import sys

PLUGINS = {
    "get": {},
    "set": {},
    "sub": {},
    "sub-trigger": {}
}


def register_response(action, name, data_description):
    ''' The function used to decorate the plugin functions relating to
        parameters that can be requested, allowing these to be registered

    Parameters
    ----------
    action : string
        The type of message the plugin function relates to, in this case "sub"
    name : string
        The name of the trigger parameter
    data_description : string
        The description of the parameter: what it is, what it does, units,
        data type, possible values, etc

    Returns
    -------
    register_wrapper : Python function
        The wrapper for registering the plugin function
    '''
    def register_wrapper(func):
        add_response(action, name, func, data_description)
        return func

    return register_wrapper


def add_response(action, name, func, data_description):
    ''' Adds a requestable parameter to the list of parameters made available
        by a server

    Parameters
    ----------
    action : string
        The type of message the plugin function relates to, in this case "sub"
    name : string
        The name of the trigger parameter
    func : Python function
        The Python plugin function
    data_description : string
        The description of the parameter: what it is, what it does, units,
        data type, possible values, etc
    '''
    global PLUGINS
    if name not in PLUGINS[action]:
        PLUGINS[action][name] = {}
    PLUGINS[action][name]["function"] = func
    PLUGINS[action][name]["data_description"] = data_description


def register_publish(action, name, interval, data_description):
    ''' The function used to decorate the plugin functions relating to timed
        parameters, allowing for these to be registered

    Parameters
    ----------
    action : string
        The type of message the plugin function relates to, in this case "sub"
    name : string
        The name of the trigger parameter
    interval : int or float
        The time interval between updates of a parameter
    data_description : string
        The description of the parameter: what it is, what it does, units,
        data type, possible values, etc

    Returns
    -------
    register_wrapper : Python function
        The wrapper for registering the plugin function
    '''
    def register_wrapper(func):
        add_publish(action, name, func, interval, data_description)
        return func

    return register_wrapper


def add_publish(action, name, func, interval, data_description):
    ''' Adds a timed parameter to the list of parameters made available by a
        server

    Parameters
    ----------
    action : string
        The type of message the plugin function relates to, in this case "sub"
    name : string
        The name of the trigger parameter
    func : Python function
        The Python plugin function
    interval : int or float
        The time interval between updates of a parameter
    data_description : string
        The description of the parameter: what it is, what it does, units,
        data type, possible values, etc
    '''
    global PLUGINS
    if name not in PLUGINS[action]:
        PLUGINS[action][name] = {}
    PLUGINS[action][name]["function"] = func
    PLUGINS[action][name]["data_description"] = data_description
    PLUGINS[action][name]["interval"] = interval


def register_trigger(name, data_description):
    ''' The function used to decorate the plugin functions relating to trigger
        parameters, allowing for these to be registered

    Parameters
    ----------
    name : string
        The name of the trigger parameter
    data_description : string
        The description of the parameter: what it is, what it does, units,
        data type, possible values, etc
    '''
    add_trigger(name, data_description)


def add_trigger(name, data_description):
    ''' Adds a trigger parameter to the list of parameters made available by a
        server

    Parameters
    ----------
    name : string
        The name of the trigger parameter
    data_description : string
        The description of the parameter: what it is, what it does, units,
        data type, possible values, etc
    '''
    global PLUGINS
    if name not in PLUGINS["sub-trigger"]:
        PLUGINS["sub-trigger"][name] = {}
    PLUGINS["sub-trigger"][name]["data_description"] = data_description


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
