from errors import MiniError

REGISTRY = {}

def plugin(func):
    if func.__name__ in REGISTRY:
        raise MiniError("two contractors, one name? you're tired. rename one")
    else:
        REGISTRY[func.__name__] = func
        return func