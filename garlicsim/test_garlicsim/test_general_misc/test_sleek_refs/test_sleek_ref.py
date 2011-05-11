# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim.general_misc.sleek_refs.SleekRef`.'''

import weakref

import nose.tools

from garlicsim.general_misc import gc_tools

from garlicsim.general_misc.sleek_refs import (SleekCallArgs,
                                               SleekRef,
                                               SleekRefDied,
                                               CuteSleekValueDict)

from .shared import _is_weakreffable, A, counter

    
def test_sleek_ref():
    '''Test the basic workings of `SleekRef`.'''

    volatile_things = [A(), 1, 4.5, 'meow', u'woof', [1, 2], (1, 2), {1: 2},
                       set([1, 2, 3]), (None, 3, {None: 4})]
    unvolatile_things = [__builtins__, list, type, sum, None]
    
    while volatile_things:
        volatile_thing = volatile_things.pop()
        sleek_ref = SleekRef(volatile_thing, counter)
        assert sleek_ref() is volatile_thing
        if _is_weakreffable(volatile_thing):
            count = counter()
            del volatile_thing
            gc_tools.collect()
            assert counter() == count + 2
            nose.tools.assert_raises(SleekRefDied, sleek_ref)
        else:
            count = counter()
            del volatile_thing
            gc_tools.collect()
            assert counter() == count + 1
            assert sleek_ref() is not None
    
    while unvolatile_things:
        unvolatile_thing = unvolatile_things.pop()
        sleek_ref = SleekRef(unvolatile_thing, counter)
        assert sleek_ref() is unvolatile_thing
        
        count = counter()
        del unvolatile_thing
        gc_tools.collect()
        assert counter() == count + 1
        # Testing if it will raise `SleekRefDied`:
        sleek_ref()
