import inspect

class E(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        print(inspect.trace())
        print(inspect.stack())
        raise self
    

assert False, E("asdf")