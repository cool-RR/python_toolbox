"""
todo: need to lock library to avoid thread trouble?
"""

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


class Fuck(object):
    
    def __init__(self, *args, **kwargs):
        print "__init__ called with ", self, args, kwargs
    def __new__(cls, *args, **kwargs):
        print "__new__ called with ", cls, args, kwargs
        return super(Fuck, cls).__new__(cls)
    def __getnewargs__(self, *args, **kwargs):
        print "__getnewargs__ called with ", self, args, kwargs
        return ("Shit that __getnewargs__ returned", "more shit")
    #def __setstate__(self, 
        
    
library = weakref.WeakValueDictionary() #WeakRefShit()
 


class PersistentReadOnlyObject(object):
    
    def __new__(cls, *args):
        
        assert len(args) in [0, 1]
        
        received_uuid = args.pop() if args else None
        
        if received_uuid: # This section is for when we are called at unpickling time
            thing = library.pop(received_uuid, None)
            if thing:
                return thing
            else: # This object does not exist in our library yet; Let's add it
                thing = super(PersistentReadOnlyObject, cls).__new__(cls)
                thing._PersistentReadOnlyObject__uuid = received_uuid
                library[received_uuid] = thing
                return thing
                
        else: # This section is for when we are called at normal creation time
            thing = super(PersistentReadOnlyObject, cls).__new__(cls)
            new_uuid = uuid.uuid4()
            thing._PersistentReadOnlyObject__uuid = new_uuid
            library[new_uuid] = thing
            return thing
        
    def __getstate__(self):
        my_dict = dict(self.__dict__)
        del my_dict["_PersistentReadOnlyObject__uuid"]
        return my_dict
    
    def __getnewargs__(self):
        return (self._PersistentReadOnlyObject__uuid,)
    
    def __setstate__(self, state):
        
        if self.__dict__.pop("_PersistentReadOnlyObject__skip_setstate"):
            return
        else:
            self.__dict__.update(state)
    
    
    def __deepcopy__(self, memo):
        return self
    
    def __copy__(self):
        return self
