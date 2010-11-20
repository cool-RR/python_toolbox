import threading
import multiprocessing

import wx

from garlicsim.general_misc import pickle_tools

# We're importing `pickle_module` from `pickle_tools`, so we get the exact same
# pickle module it's using. (Giving it the freedom to change between `cPickle`
# and `pickle`.)
from garlicsim.general_misc.pickle_tools import pickle_module


def is_pickle_successful(thing):
    try:
        string = pickle_module.dumps(thing)
        unpickled_thing = pickle_module.loads(string)
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
        
    for thing in atomically_pickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        
        
def test_simple_non_atomically_pickleables():
    non_pickleables = [
        threading.Lock(),
        threading.RLock(),
        threading.Condition(),
        threading.BoundedSemaphore(),
        threading.currentThread(),
        threading.Semaphore(),
        multiprocessing.Lock(),
        multiprocessing.BoundedSemaphore(),
        multiprocessing.Condition(),
        multiprocessing.JoinableQueue(),
        multiprocessing.Manager(),
        multiprocessing.Pool(),
        multiprocessing.Queue(),
        multiprocessing.RLock(),
        multiprocessing.Semaphore(),
    ]
    
    for thing in pickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        assert is_pickle_successful(thing)
        
    for thing in atomically_pickleablespickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        
        
        