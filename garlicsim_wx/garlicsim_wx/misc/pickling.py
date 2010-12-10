from garlicsim.general_misc import pickle_tools


class Pickler(pickle_tools.CutePickler):
    def __init__(self, file_, protocol=2): 
        pickle_tools.CutePickler.__init__(self, file_, protocol)

    def pre_filter(self, thing):
        return (getattr(thing, '__module__', None) != '__garlicsim_shell__')

class Unpickler(pickle_tools.CuteUnpickler):
    pass

