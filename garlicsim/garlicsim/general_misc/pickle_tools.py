import re
import pickle as pickle_module
import copy_reg

from garlicsim.general_misc import caching
from garlicsim.general_misc import address_tools


def is_atomically_pickleable(thing):
    # Using __class__ instead of type because of goddamned old-style classes.
    # And using `type` as a fallback because goddamned old-style classes don't
    # have `__class__`. tododoc: make tests.
    my_type = getattr(thing, '__class__', None) or type(thing) 
    return _is_type_atomically_pickleable(my_type, thing)


def _is_type_atomically_pickleable(type_, thing=None):
    try:
        return _is_type_atomically_pickleable.cache[type_]
    except KeyError:
        pass
    
    if thing is not None:
        assert isinstance(thing, type_)
        
    # Sub-function in order to do caching without crowding the main algorithm:
    def get_result():
        
        if hasattr(type_, '_is_atomically_pickleable'):
            return type_._is_atomically_pickleable
        
        # Weird special case: `threading.Lock` objects don't have `__class__`.
        # We assume that objects that don't have `__class__` can't be pickled.
        if not hasattr(thing, '__class__'):
            return False
        
        
        def confirm_legit_pickling_exception(exception):
            message = exception.args[0]
            segments = [
                "can't pickle",
                'should only be shared between processes through inheritance',
                'cannot be passed between processes or pickled'
            ]
            assert any((segment in message) for segment in segments)
            # todo: turn to warning
        
        reduce_function = copy_reg.dispatch_table.get(type_)
        if reduce_function:
            try:
                reduce_result = reduce_function(thing)
            except Exception, exception:
                confirm_legit_pickling_exception(exception)
                return False
            else:
                return True
        
        reduce_function = getattr(type_, '__reduce_ex__', None)
        if reduce_function:
            try:
                reduce_result = reduce_function(thing, 2) # argument is protocol
            except Exception, exception:
                confirm_legit_pickling_exception(exception)
                return False
            else:
                return True
            
        reduce_function = getattr(type_, '__reduce__', None)
        if reduce_function:
            try:
                reduce_result = reduce_function(thing)
            except Exception, exception:
                confirm_legit_pickling_exception(exception)
                return False
            else:
                return True
        
        return False

    result = get_result()
    _is_type_atomically_pickleable.cache[type_] = result
    return result
    
    
    ## tododoc This is done by stupid whitelisting temporarily:
    #import thread, multiprocessing.synchronize
    #atomically_non_pickleable_types = \
        #(file, thread.LockType, multiprocessing.synchronize.Lock)
    #if issubclass(type_, atomically_non_pickleable_types):
        #cache[type_] = False
        #return False
    #else:
        #cache[type_] = True
        #return True
        
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
