
from garlicsim.general_misc import cute_profile

from .shared import call_and_check_if_profiled


def func(x, y, z=3):
    sum([1, 2, 3])
    set([1, 2]) | set([2, 3])
    return x, y, z



def test_profile_ready():
    
    f = cute_profile.profile_ready(start_on=True, off_after=False)(func)
    assert call_and_check_if_profiled(lambda: f(1, 2)) is True
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    assert call_and_check_if_profiled(lambda: f(1, 2)) is False
    
    