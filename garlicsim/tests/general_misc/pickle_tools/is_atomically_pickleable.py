import threading
import multiprocessing

from garlicsim.general_misc import pickle_tools

# We're importing `pickle_module` from `pickle_tools`, so we get the exact same
# pickle module it's using. (Giving it the freedom to change between `cPickle`
# and `pickle`.)
from garlicsim.general_misc.pickle_tools import pickle_module


def is_pickle_successful(thing):
    try:
        string = pickle_module.dumps(thing)
        unpickled_thing = pickle_module.loads(thing)
    except Exception:
        return False
    else:
        return thing == unpickled_thing

    
def test_simple_atomically_pickleables():
    pickleables = [
        None, True, False,
        1, 1.1, -3, 3+4.5j,
        'roar', u'Meow!',
        {1: 3, 'frr': 'meow'},
        ['one', 'two', (3, 4)],
        set([1, 2, 3, 1]),
        frozenset((1, 2, 3, 1, 'meow', frozenset())),
        sum, slice, type
    ]
    
    atomically_pickleables = [
        set([threading.Lock()]),
        [multiprocessing.Lock()],
    ]
    
    for thing in pickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        assert is_pickle_successful(thing)
        
    for thing in atomically_pickleablespickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        
        
        