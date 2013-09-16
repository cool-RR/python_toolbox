# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `is_atomically_pickleable`.'''



import threading
import io
import io

# We're importing `pickle_module` from `pickle_tools`, so we get the exact same
# pickle module it's using. (Giving it the freedom to change between `cPickle`
# and `pickle`.)
from python_toolbox.pickle_tools import pickle_module

import nose

from python_toolbox import import_tools
import python_toolbox

from python_toolbox import pickle_tools

from .shared import PickleableObject, NonPickleableObject


def is_pickle_successful(thing):
    '''`try` to pickle `thing` and return whether it worked.'''
    try:
        string = pickle_module.dumps(thing)
        unpickled_thing = pickle_module.loads(string)
    except Exception:
        return False
    else:
        return True

    
def test_simple_atomically_pickleables():
    '''Test `is_atomically_pickleable` on atomically pickleable objects.'''
    pickleables = [
        None, True, False,
        1, 1.1, -3, 3+4.5j,
        'roar', 'Meow!',
        {1: 3, 'frr': 'meow'},
        ['one', 'two', (3, 4)],
        set([1, 2, 3, 1]),
        frozenset((1, 2, 3, 1, 'meow', frozenset())),
        io.StringIO(),
        sum, slice, type
    ]
    
    atomically_pickleables = [
        set([threading.Lock()]),
        [threading.Lock()],
    ]
    
    for thing in pickleables:
        assert is_pickle_successful(thing)
        assert pickle_tools.is_atomically_pickleable(thing)
        
    for thing in atomically_pickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        
        
        
def test_non_atomically_pickleables_multiprocessing():
    '''
    Test `is_atomically_pickleable` on non-atomically pickleable objects.
    
    Not including `multiprocessing` objects.
    '''
    
    import multiprocessing

    non_pickleables = [
        multiprocessing.Lock(),
        multiprocessing.BoundedSemaphore(),
        multiprocessing.Condition(),
        multiprocessing.JoinableQueue(),
        multiprocessing.Pool(),
        multiprocessing.Queue(),
        multiprocessing.RLock(),
        multiprocessing.Semaphore(),
    ]
        
    for thing in non_pickleables:
        assert not pickle_tools.is_atomically_pickleable(thing)
        assert not is_pickle_successful(thing)
    
    assert not pickle_tools.is_atomically_pickleable(NonPickleableObject())
    # Not trying to actually pickle this test object, cause it will actually
    # work.

    
def test_partially_pickleables_multiprocessing():
    '''
    "Partially-pickleable" means an object which is atomically pickleable but
    not pickleable.
    '''

    import multiprocessing
    
    x = PickleableObject()
    x.lock = threading.Lock()
    
    partially_pickleables = [
        x,
        [multiprocessing.BoundedSemaphore()],
        {1: multiprocessing.Lock(), 2: 3},
        set([multiprocessing.Queue(), x])
    ]
    
    for thing in partially_pickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        assert not is_pickle_successful(thing)
        
        
def test_non_atomically_pickleables():
    '''Test `is_atomically_pickleable` on non-atomically pickleable objects.'''
    
    if python_toolbox.__version_info__ <= (0, 6, 0, 'release'):
        raise nose.SkipTest

    non_pickleables = [
        threading.Lock(),
        io.StringIO()
    ]
        
    for thing in non_pickleables:
        assert not pickle_tools.is_atomically_pickleable(thing)
        assert not is_pickle_successful(thing)
    
    assert not pickle_tools.is_atomically_pickleable(NonPickleableObject())
    # Not trying to actually pickle this test object, cause it will actually
    # work.

    
def test_partially_pickleables():
    '''
    Test `is_atomically_pickleable` on partially pickleable objects.
    
    "Partially-pickleable" means an object which is atomically pickleable but
    not pickleable.
    '''
    
    x = PickleableObject()
    x.lock = threading.Lock()
    
    partially_pickleables = [
        x,
        [threading.Lock()],
        {1: threading.Lock(), 2: 3},
        set([threading.Lock(), x])
    ]
    
    for thing in partially_pickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        assert not is_pickle_successful(thing)
