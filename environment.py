class Environment:
    def __init__(self,plugins,execute):
        self.variables = [{}]
        self.ship = None
        self.execute = execute
        self.stack = []
        self.plugins = plugins
        self.function = {}
        self.pos = 0

class Block:
    def __init__(self,kind,where):
        self.kind = kind
        self.where = where

class Function:
    def __init__(self,point,arg_name):
        self.point = point
        self.arg_name = arg_name