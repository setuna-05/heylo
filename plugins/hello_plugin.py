from plugin_api import plugin

@plugin
def hello(msg):
    print("hello " + msg)
    return True