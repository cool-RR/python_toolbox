
# tododoc: Must use weakref, otherwise all garbage-collection goes kaput!


from garlicsim.general_misc.sleek_refs import SleekCallArgs


# tododoc __all__


class SelfPlaceholder(object):
    pass # todo: make uninstanciable


class CachedType(type):
    def __new__(self, *args, **kwargs):
        result = type.__new__(self, *args, **kwargs)
        result.__cache = {}
        return result
    
    def __call__(cls, *args, **kwargs):
        sleek_call_args = SleekCallArgs(
            cls.__cache,
            cls.__init__,
            *((SelfPlaceholder,) + args),
            **kwargs
        )
        try:
            return cls.__cache[sleek_call_args]
        except KeyError:
            cls.__cache[sleek_call_args] = value = \
                type.__call__(cls, *args, **kwargs)
            return value
