# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing
from python_toolbox import sequence_tools
from python_toolbox.sequence_tools import is_subsequence



def test():
    true_pairs = (
        ([1, 2, 3, 4], [2, 3]),
        ([1, 2, 3, 4], (2, 3)),
        ([1, 2, 'meow', 3, 4], (2, 'meow', 3)),
        ('abracadabra', 'cad'),
        ('abracadabra', 'dab'),
        ('abracadabra', 'a'),
        ('abracadabra', 'ab'),
        ('abracadabra', 'bra'),
        (range(10000), (range(7, 14))),
        (range(10000), [99]),
    )
    false_pairs = (
        ([1, 2, 3, 4], [2, 4]),
        ([1, 2, 3, 4], (2, 4)),
        ([1, 2, 'meow', 3, 4], (2, 3)),
        ('abracadabra', 'cab'),
        ('abracadabra', 'darb'),
        ('abracadabra', 'z'),
        ('abracadabra', 'bab'),
        ('abracadabra', 'arb'),
        (range(10000), (range(14, 7, -1))),
        (range(100), [100]),
        (range(100), [109]),
    )

    for true_pair in true_pairs:
        assert is_subsequence(*true_pair)
    for false_pair in false_pairs:
        assert not is_subsequence(*false_pair)