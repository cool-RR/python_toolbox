
from python_toolbox import cute_testing

from python_toolbox.sequence_tools import Range


def test():
    natural_range_arguments_tuples = (
        (10,), (3,), (20, 30), (20, 30, 2), (20, 30, -2)
    )
    
    for natural_range_arguments_tuple in natural_range_arguments_tuples:
        r0 = Range(*natural_range_arguments_tuple)
        assert type(r0) == range
        assert isinstance(r0, range)
        assert isinstance(r0, Range)
        r1 = Range(*natural_range_arguments_tuple, _avoid_builtin_range=True)
        assert type(r1) == Range
        assert isinstance(r1, range)
        assert isinstance(r1, Range)
        assert tuple(r0) == tuple(r1)
        if r0:
            assert r0[-1] == r1[-1]
        
    pass
        
    