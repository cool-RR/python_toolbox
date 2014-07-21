
from python_toolbox import cute_testing

from python_toolbox.sequence_tools import Range


def test():
    assert Range(10) == range(10)
    assert Range(3) == range(3)
    assert Range(20, 30) == range(20, 30)
    assert Range(20, 30, 2) == range(20, 30, 2)
    assert Range(20, 30, -2) == range(20, 30, -2)
    
    assert Range(10)
    
        
    