import gc
import weakref
from garlicsim.general_misc.sleek_refs import (SleekCallArgs,
                                               SleekRef,
                                               CuteSleekValueDictionary)

def _is_weakreffable(thing):
    try:
        weakref.ref(thing)
    except TypeError:
        return False
    else:
        return True

class A():
    @staticmethod
    def s():
        pass
    
    
def test_sleek_ref():
    
    def counter(_=None):
        if not hasattr(counter, 'count'):
            counter.count = 0
        result = counter.count
        counter.count += 1
        return result
            
    volatile_things = [A(), 1, 4.5, 'meow', u'woof', [1, 2], (1, 2), {1: 2},
                       set([1, 2, 3]), sum]
    unvolatile_things = [A.s, __builtins__, list, type,  list.append, str.join]
    
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
        
def test_cute_sleek_value_dictionary():
    pass