import gc


library = []


def get_object_by_id(id_):
    for thing in gc.get_objects():
        if id(thing) == id_:
            return thing
    raise Exception("No found")

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
            thing = object.__new__(cls)
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
    
    def __del__(self):
        library.remove(id(self))