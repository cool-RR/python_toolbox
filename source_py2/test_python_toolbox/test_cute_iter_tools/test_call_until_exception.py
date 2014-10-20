# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import collections

from python_toolbox.cute_iter_tools import call_until_exception


def test():
    
    assert list(call_until_exception(collections.deque(range(7)).popleft,
                                     IndexError)) == list(range(7))
    