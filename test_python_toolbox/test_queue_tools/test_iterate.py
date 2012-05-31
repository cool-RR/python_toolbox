# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing package for `queue_tools.iterate`.'''

from __future__ import with_statement

import Queue as queue_module

from python_toolbox import cute_testing

from python_toolbox import queue_tools


def test():
    '''Test `iterate`.'''    
    queue = queue_module.Queue()
    queue.put(1)
    queue.put(2)
    queue.put(3)
    assert list(queue_tools.iterate(queue)) == [1, 2, 3]