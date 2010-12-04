import sys

from garlicsim.general_misc.temp_value_setters import TempRecursionLimitSetter


def test():
    
    old_recursion_limit = sys.getrecursionlimit()
    assert sys.getrecursionlimit() == old_recursion_limit
    with TempRecursionLimitSetter(old_recursion_limit + 3):
        assert sys.getrecursionlimit() == old_recursion_limit + 3
    assert sys.getrecursionlimit() == old_recursion_limit
    