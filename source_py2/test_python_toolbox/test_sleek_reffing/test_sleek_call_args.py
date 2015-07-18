# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.sleek_reffing.SleekCallArgs`.'''

import weakref

from python_toolbox import gc_tools

from python_toolbox.sleek_reffing import (SleekCallArgs,
                                          SleekRef,
                                          CuteSleekValueDict)
from .shared import _is_weakreffable, A, counter


def f(*args, **kwargs): pass


def test():
    '''Test the basic workings of `SleekCallArgs`.'''
    sca_dict = {}
    
    args = (1, 2)
    sca1 = SleekCallArgs(sca_dict, f, *args)
    sca_dict[sca1] = 'meow'
    del args
    gc_tools.collect()
    assert len(sca_dict) == 1
    
    args = (1, A())
    sca2 = SleekCallArgs(sca_dict, f, *args)
    sca_dict[sca2] = 'meow'
    del args
    gc_tools.collect()
    assert len(sca_dict) == 1
    
    
def test_unhashable():
    '''Test `SleekCallArgs` on unhashable arguments.'''
    sca_dict = {}
    
    args = ([1, 2], {1: [1, 2]}, set(('a', 1)))
    sca1 = SleekCallArgs(sca_dict, f, *args)
    hash(sca1)
    sca_dict[sca1] = 'meow'
    del args
    gc_tools.collect()
    # GCed because there's a `set` in `args`, and it's weakreffable:
    assert len(sca_dict) == 0
    
    kwargs = {
        'a': {1: 2},
        'b': [
            set(),
            set((frozenset((3, 4))))
        ]
    }
    sca2 = SleekCallArgs(sca_dict, f, **kwargs)
    hash(sca2)
    sca_dict[sca2] = 'meow'
    del kwargs
    gc_tools.collect()
    # Not GCed because all objects in `kwargs` are not weakreffable:
    assert len(sca_dict) == 1
    