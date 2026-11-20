from errors import MiniError
from plugin_api import REGISTRY
import importlib.util
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

def load_plugins():
    plugins_dir = os.path.join(base_dir,"plugins")
    if os.path.isdir(plugins_dir):
        for file_name in os.listdir(plugins_dir):
            if file_name.endswith(".py") and file_name != "__init__.py":
                path = os.path.join(plugins_dir,file_name)
                spec = importlib.util.spec_from_file_location(file_name[:-3],path)
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                except MiniError as e:
                    e.file = os.path.join("plugins",file_name)
                    raise
    return REGISTRY