from __future__ import with_statement

import threading
import StringIO
import cStringIO

# We're importing `pickle_module` from `pickle_tools`, so we get the exact same
# pickle module it's using. (Giving it the freedom to change between `cPickle`
# and `pickle`.)
from garlicsim.general_misc.pickle_tools import pickle_module

import wx
import nose

from garlicsim.general_misc import import_tools

from garlicsim.general_misc import pickle_tools

from .shared import PickleableObject, NonPickleableObject


def is_pickle_successful(thing):
    try:
        string = pickle_module.dumps(thing)
        unpickled_thing = pickle_module.loads(string)
    except Exception:
        return False
    else:
        return True

    
def test_simple_atomically_pickleables():
    pickleables = [
        None, True, False,
        1, 1.1, -3, 3+4.5j,
        'roar', u'Meow!',
        {1: 3, 'frr': 'meow'},
        ['one', 'two', (3, 4)],
        set([1, 2, 3, 1]),
        frozenset((1, 2, 3, 1, 'meow', frozenset())),
        StringIO.StringIO(),
        sum, slice, type
    ]
    
    atomically_pickleables = [
        set([threading.Lock()]),
        [threading.Lock()],
    ]
    
    for thing in pickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        assert is_pickle_successful(thing)
        
    for thing in atomically_pickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        
        
def test_non_atomically_pickleables_multiprocessing():
    
    if not import_tools.exists('multiprocessing'):
        raise nose.SkipTest('`multiprocessing` is not installed.')
    
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

    if not import_tools.exists('multiprocessing'):
        raise nose.SkipTest('`multiprocessing` is not installed.')
    
    import multiprocessing
    
    x = PickleableObject()
    x.lock = threading.Lock()
    
    partially_pickleables = [
        x,
        [multiprocessing.BoundedSephamore()],
        {1: multiprocessing.Lock(), 2: 3},
        set([multiprocessing.Queue(), x])
    ]
    
    for thing in partially_pickleables:
        assert pickle_tools.is_atomically_pickleable(thing)
        assert not is_pickle_successful(thing)
        
        
def test_non_atomically_pickleables():

    non_pickleables = [
        threading.Lock(),
        cStringIO.StringIO()
    ]
    #tododoc: test on both StringIOs too
        
    for thing in non_pickleables:
        assert not pickle_tools.is_atomically_pickleable(thing)
        assert not is_pickle_successful(thing)
    
    assert not pickle_tools.is_atomically_pickleable(NonPickleableObject())
    # Not trying to actually pickle this test object, cause it will actually
    # work.

    
def test_partially_pickleables():
    '''
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