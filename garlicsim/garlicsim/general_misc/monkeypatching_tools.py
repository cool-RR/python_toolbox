import types

def monkeypatch_method(class_, name=None):
    def decorator(function):
        name = name or function.__name__
        new_method = types.MethodType(function, class_)
        setattr(class_, name, new_method)
        return function
            
        