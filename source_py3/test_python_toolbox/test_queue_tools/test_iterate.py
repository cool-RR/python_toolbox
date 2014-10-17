# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing package for `queue_tools.iterate`.'''

import queue as queue_module

from python_toolbox import cute_testing

from python_toolbox import queue_tools


def test():
    '''Test `iterate`.'''    
    queue = queue_module.Queue()
    queue.put(1)
    queue.put(2)
    queue.put(3)
    assert list(queue_tools.iterate(queue)) == [1, 2, 3]