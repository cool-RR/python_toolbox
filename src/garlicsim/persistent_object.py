import gc

import weakref

class WeakRefSet(object):
    def __init__(self):
        self.weak_dict = weakref.WeakValueDictionary()
    def add(self, thing):
        id_ = id(thing)
        if self.weak_dict.has_key[id_]:
            possible_match = self.weak_dict(id_)
            assert possible_match is thing
            return
        else self.weak_dict[id_] = thing
    def __contains__(self, thing):
        return (thing in self.weak_dict.values())

library = WeakRefSet()

class PersistentObject(object):
    """
    def __init__(self):
    """
    
    def __getstate__(self):
        return (id(self), self.__dict__)
    
    def __new__(cls, *args):
        if args:
            return FFF
        else:
            thing = super(PersistentObject, cls).__new__(cls)
            library.append(id(thing))
            thing
    
    def __getnewargs__(self):
        return id(self)
    
    def __setstate__(self, state):
        
        pass
    
    
    def __deepcopy__(self, memo):
        return self
    
    def __copy__(self):
        return self
    """
    def __del__(self):
        library.remove(id(self))
    """