import gc
import uuid
import weakref

class WeakRefShit(object):
    def __init__(self):
        self.weak_dict = weakref.WeakValueDictionary()
    def add(self, thing):
        uuid_ = uuid4()
        self.weak_dict[uuid_] = thing
    def __contains__(self, thing):
        return (thing in self.weak_dict.values())

library = weakref.WeakValueDictionary() #WeakRefShit()

class Fuck(object):
    
    def __init__(self, *args, **kwargs):
        print "__init__ called with ", self, args, kwargs
    def __new__(cls, *args, **kwargs):
        print "__new__ called with ", cls, args, kwargs
        return super(Fuck, cls).__new__(cls)
    def __getnewargs__(self, *args, **kwargs):
        print "__getnewargs__ called with ", self, args, kwargs
        return ("Shit that __getnewargs__ returned", "more shit")
        
    
    


class PersistentReadOnlyObject(object):
    """
    def __init__(self):
    """
    
    def __getstate__(self):
        return (id(self), self.__dict__)
    
    def __new__(cls, *args, **kwargs):
        uuid_ = kwargs.pop("_PersistentReadOnlyObject__uuid", None)
        if uuid_: # This section is for when we are called at unpickling time
            thing = library.pop(uuid_, None)
            if thing:
                return thing
        else: # This section is for when we are called at normal creation time
            thing = super(PersistentReadOnlyObject, cls).__new__(cls)
            new_uuid = uuid.uuid4()
            thing._PersistentReadOnlyObject__uuid = new_uuid
            library[new_uuid] = thing
            return thing
    
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