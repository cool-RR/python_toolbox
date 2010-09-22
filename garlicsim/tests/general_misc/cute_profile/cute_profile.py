
from garlicsim.general_misc import cute_profile

from .shared import call_and_check_if_profiled


def func(x, y, z=3):
    sum([1, 2, 3])
    set([1, 2]) | set([2, 3])
    return x, y, z



def test_simple():
    
    f = cute_profile.profile_ready()(func)
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    f.profiling_on = True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    
    
    f = cute_profile.profile_ready(start_on=True)(func)
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    f.profiling_on = False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    
    
    f = cute_profile.profile_ready(start_on=True, off_after=True)(func)
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    f.profiling_on = True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    
    
    f = cute_profile.profile_ready(off_after=True)(func)
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    f.profiling_on = True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    f.profiling_on = True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    
    
    
def test_method():
    
    class A(object):
        def __init__(self):
            self.x = 0
                
        @cute_profile.profile_ready()
        def increment(self):
            sum([1, 2, 3])
            self.x += 1
            
    a = A()
    assert a.x == 0
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 1
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 2
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 3

    a.increment.im_func.profiling_on = True
    
    assert call_and_check_if_profiled(a.increment) is True
    assert a.x == 4
    assert call_and_check_if_profiled(a.increment) is True
    assert a.x == 5
    assert call_and_check_if_profiled(a.increment) is True
    assert a.x == 6
    
    a.increment.im_func.off_after = True
    
    assert call_and_check_if_profiled(a.increment) is True
    assert a.x == 7
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 8
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 9
    
    a.increment.im_func.profiling_on = True
    
    assert call_and_check_if_profiled(a.increment) is True
    assert a.x == 10
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 11
    assert call_and_check_if_profiled(a.increment) is False
    assert a.x == 12
    
    
    