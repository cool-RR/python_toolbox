import re
import cPickle as pickle_module

from garlicsim.general_misc import caching
from garlicsim.general_misc import address_tools


def is_atomically_pickleable(thing):
    # Using __class__ instead of type because of goddamned old-style classes.
    # And using `type` as a fallback because goddamned old-style classes don't
    # have `__class__`. tododoc: make tests.
    my_type = getattr(thing, '__class__', None) or type(thing) 
    return _is_type_atomically_pickleable(my_type)


def _is_type_atomically_pickleable(my_type):
    try:
        return _is_type_atomically_pickleable.cache[my_type]
    except KeyError:
        pass
    if hasattr(my_type, 'is_atomically_pickleable'):
        _is_type_atomically_pickleable.cache[my_type] = \
            my_type.is_atomically_pickleable
        return my_type.is_atomically_pickleable
    # tododoc This is done by stupid whitelisting temporarily:
    import thread, multiprocessing.synchronize
    atomically_non_pickleable_types = \
        (file, thread.LockType, multiprocessing.synchronize.Lock)
    if issubclass(my_type, atomically_non_pickleable_types):
        _is_type_atomically_pickleable.cache[my_type] = False
        return False
    else:
        _is_type_atomically_pickleable.cache[my_type] = True
        return True
_is_type_atomically_pickleable.cache = {}
 

class FilteredObject(object): 
    def __init__(self, about): 
        self.about = about 
    def __repr__(self): 
        return 'FilteredObject(%s)' % repr(self.about) 
    def __getattr__(self, key):
        return FilteredObject('%s.%s' % (self.about, key))
        

_filtered_string_pattern = re.compile(
    r'^Filtered by pickle_tools \((?P<description>.*?)\)$'
)
 
class CutePickler(object): 
    '''Not subclassing because cPickle.Pickler doesn't support subclassing.'''
    def __init__(self, file_, protocol=0): 
        pickler = self.pickler = pickle_module.Pickler(file_, protocol) 
        pickler.persistent_id = self.persistent_id 
        self.dump, self.clear_memo = \
            pickler.dump, pickler.clear_memo
 
    def persistent_id(self, obj): 
        if is_atomically_pickleable(obj): 
            return None 
        else:
            return 'Filtered by pickle_tools (%s)' % \
                   address_tools.describe(obj)
 
    
class CuteUnpickler(object): 
    '''
    Not subclassing because cPickle.Unpickler doesn't support subclassing.
    '''
    def __init__(self, file_): 
        unpickler = self.unpickler = pickle_module.Unpickler(file_) 
        unpickler.persistent_load = self.persistent_load
        self.load = unpickler.load
        self.noload = getattr(unpickler, 'noload', None)
        # (Defaulting to `None` because `pickle.Unpickler` doesn't have
        # `noload`.)

            
 
    def persistent_load(self, id_string):
        match = _filtered_string_pattern.match(id_string)
        if match:
            description = match.groupdict()['description']            
            return FilteredObject(description) 
        else: 
            raise UnpicklingError('Invalid persistent id') 
 
 
    
if __name__ == '__main__':
    import threading, multiprocessing, pickle, copy_reg
    rl = threading.RLock()
    f = open(r'c:\Users\User\delete_me', 'r')
    f.__reduce__()
    pickle.dumps(rl)
