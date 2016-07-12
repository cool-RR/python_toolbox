# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing
from python_toolbox import sequence_tools

from python_toolbox.sequence_tools import is_contained_in

class PureContainer:
    def __init__(self, inner):
        self.inner = list(inner)
    __contains__ = lambda self, item: item in self.inner
        

def test():
    true_examples = [
        ([1, 3, 6], range(10)),
        (iter([1, 3, 6]), range(10)),
        (range(4, 7), range(2, 11)), 
        (range(4, 7), PureContainer(range(2, 11))), 
    ]
    false_examples = [
        ([11, 3, 6], range(10)),
        ([1, 3, 6, 11], range(10)),
        (iter([1, 3, 6, 11]), range(10)),
        (range(4, 17), range(2, 11)), 
        (range(4, 17), PureContainer(range(2, 11))), 
    ]
    for true_example in true_examples:
        assert is_contained_in(*true_example)
    for false_example in false_examples:
        assert not is_contained_in(*false_example)