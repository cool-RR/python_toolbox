import types

def monkeypatch_method(class_, name=None):
    def decorator(function):
        name_ = name or function.__name__
        new_method = types.MethodType(function, None, class_)
		# Was: new_method = types.MethodType(function, class_), is subtly wrong, make tests to prove
        setattr(class_, name_, new_method)
        return function
    return decorator