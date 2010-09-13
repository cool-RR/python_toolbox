import gc
import weakref
from garlicsim.general_misc.sleek_refs import (SleekCallArgs,
                                               SleekRef,
                                               CuteSleekValueDictionary)

from .shared import _is_weakreffable, A, counter


def test_sleek_call_args():
    
    volatile_things = [A(), 1, 4.5, 'meow', u'woof', [1, 2], (1, 2), {1: 2},
                       set([1, 2, 3])]
    unvolatile_things = [A.s, __builtins__, list, type,  list.append, str.join,
                         sum]
    def f(*args, **kwargs):
        pass
    
    sca_dict = {}
    
    args = (1, 2)
    sca1 = SleekCallArgs(sca_dict, f, *args)
    sca_dict[sca1] = 'meow'
    del args
    gc.collect()
    assert len(sca_dict) == 1
    
    args = (1, A())
    sca2 = SleekCallArgs(sca_dict, f, *args)
    sca_dict[sca2] = 'meow'
    del args
    gc.collect()
    assert len(sca_dict) == 1
    