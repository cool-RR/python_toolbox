import cPickle as pickle_module

from garlicsim.general_misc import caching


def is_atomically_pickleable(thing):
    return _is_type_atomically_pickleable(type(thing))


@caching.cache()
def _is_type_atomically_pickleable(my_type):
    if hasattr(my_type, 'is_pickleable'):
        return my_type.is_pickleable
    # tododoc This is done by stupid whitelisting temporarily:
    import thread, multiprocessing
    atomically_unpickleable_types = \
        (file, thread.LockType, multiprocessing.synchronize.Lock)
    if issubclass(my_type, atomically_unpickleable_types):
        return False
    else:
        return True
    
if __name__ == '__main__':
    import threading, multiprocessing, pickle, copy_reg
    rl = threading.RLock()
    f = open(r'c:\Users\User\delete_me', 'r')
    f.__reduce__()
    pickle.dumps(rl)

"""
from cPickle import Pickler, Unpickler, UnpicklingError 
 
 
class FilteredObject: 
    def __init__(self, about): 
        self.about = about 
    def __repr__(self): 
        return 'FilteredObject(%s)' % repr(self.about) 

    
import cPickle 
 
def persistent_id(obj): 
    if isinstance(obj, wxObject): 
        return "filtered:wxObject" 
    else: 
        return None 
 
class FilteredObject: 
    def __init__(self, about): 
        self.about = about 
    def __repr__(self): 
        return 'FilteredObject(%s)' % repr(self.about) 
 
def persistent_load(obj_id): 
    if obj_id.startswith('filtered:'): 
        return FilteredObject(obj_id[9:]) 
    else: 
        raise cPickle.UnpicklingError('Invalid persistent id') 
 
def dump_filtered(obj, file): 
    p = cPickle.Pickler(file) 
    p.persistent_id = persistent_id 
    p.dump(obj) 
 
def load_filtered(file):
    u = cPickle.Unpickler(file) 
    u.persistent_load = persistent_load 
    return u.load() 

 
class MyPickler(object): 
 
    def __init__(self, file, protocol=0): 
        pickler = Pickler(file, protocol) 
        pickler.persistent_id = self.persistent_id 
        self.dump = pickler.dump 
        self.clear_memo = pickler.clear_memo 
 
    def persistent_id(self, obj): 
        if not hasattr(obj, '__getstate__') and not isinstance(obj, 
            (basestring, int, long, float, tuple, list, set, dict)): 
            return "filtered:%s" % type(obj) 
        else: 
            return None 
 
 
class MyUnpickler(object): 
 
    def __init__(self, file): 
        unpickler = Unpickler(file) 
        unpickler.persistent_load = self.persistent_load 
        self.load = unpickler.load 
        self.noload = unpickler.noload 
 
    def persistent_load(self, obj_id): 
        if obj_id.startswith('filtered:'): 
            return FilteredObject(obj_id[9:]) 
        else: 
            raise UnpicklingError('Invalid persistent id') 
 
 
if __name__ == '__main__': 
    from cStringIO import StringIO 
 
    class UnpickleableThing(object): 
        pass 
 
    f = StringIO() 
    p = MyPickler(f) 
    p.dump({'a': 1, 'b': UnpickleableThing()}) 
 
    f.seek(0) 
    u = MyUnpickler(f) 
    obj = u.load() 
    print obj 
 
    assert obj['a'] == 1 
    assert isinstance(obj['b'], FilteredObject) 
    assert obj['b'].about 
"""