import types

discardables = ['__builtins__']

wrapped_modules = {}

def module_wrapper_factory(module):
    if wrapped_modules.has_key(module):
        return wrapped_modules[module]
    else:
        module_wrapper = ModuleWrapper(module)
        return module_wrapper

class ModuleWrapper(object):
    def __init__(self, module):
        wrapped_modules[module] = self
        self.__dict__ = dict(module.__dict__)
        for name, thing in self.__dict__.items():
            """
            Note this is a weak form of recursive scanning
            """
            if name in discardables:
                self.__dict__[name] = "Missing item, string representation:" +\
                                      str(thing)
                continue
            if isinstance(thing, types.ModuleType):
                self.__dict__[name] = "Missing module " + thing.__name__
                continue
                
                
if __name__ == "__main__":
    import cPickle
    def test(module):
        try:
            cPickle.dumps(ModuleWrapper(module))
            return True
        except:
            return False
        
    import garlicsim_wx.simulation_packages.life as life
    print(test(life))
    cPickle.dumps(ModuleWrapper(life))