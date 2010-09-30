import gc
import weakref
from garlicsim.general_misc.sleek_refs import (SleekCallArgs,
                                               SleekRef,
                                               CuteSleekValueDict)

from .shared import _is_weakreffable, A, counter

    
def test_sleek_ref():

    volatile_things = [A(), 1, 4.5, 'meow', u'woof', [1, 2], (1, 2), {1: 2},
                       set([1, 2, 3])]
    unvolatile_things = [A.s, __builtins__, list, type,  list.append, str.join,
                         sum]
    
    while volatile_things:
        volatile_thing = volatile_things.pop()
        sleek_ref = SleekRef(volatile_thing, counter)
        assert sleek_ref() is volatile_thing
        if _is_weakreffable(volatile_thing):
            count = counter()
            del volatile_thing
            gc.collect()
            assert counter() == count + 2
            assert sleek_ref() is None 
        else:
            count = counter()
            del volatile_thing
            gc.collect()
            assert counter() == count + 1
            assert sleek_ref() is not None
    
    while unvolatile_things:
        unvolatile_thing = unvolatile_things.pop()
        sleek_ref = SleekRef(unvolatile_thing, counter)
        assert sleek_ref() is unvolatile_thing
        
        count = counter()
        del unvolatile_thing
        gc.collect()
        assert counter() == count + 1
        assert sleek_ref() is not None
