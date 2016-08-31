# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import os
import threading
import concurrent.futures
import time

from python_toolbox import future_tools


def test():
    
    def sleep_and_return(seconds):
        time.sleep(seconds)
        return seconds
        
    
    with future_tools.CuteThreadPoolExecutor(10) as executor:
        assert isinstance(executor, future_tools.CuteThreadPoolExecutor)
        assert tuple(executor.filter(lambda x: (x % 2 == 0), range(10))) == \
                                                         tuple(range(0, 10, 2))
        assert sorted(executor.filter(lambda x: (x % 2 == 0), range(10),
                                     timeout=10**5, as_completed=True)) == \
                                                          list(range(0, 10, 2))
        assert tuple(executor.filter(
            lambda x: (sleep_and_return(x) % 2 == 0), range(9, -1, -1),
            as_completed=True)) == tuple(range(0, 10, 2))
        
        
        assert tuple(executor.map(lambda x: x % 3, range(10))) == \
                                                 (0, 1, 2, 0, 1, 2, 0, 1, 2, 0)
        assert sorted(executor.map(lambda x: x % 3, range(10),
                                     timeout=10**5, as_completed=True)) == \
                                                 [0, 0, 0, 0, 1, 1, 1, 2, 2, 2]

        assert tuple(executor.map(sleep_and_return, range(9, -1, -1),
                                  as_completed=True)) == tuple(range(10))
        
        
def test_cute_dummy_executor():
    
    def foo(i):
        n = foo.n
        foo.n += 1
        return (i, n, os.getpid(), threading.get_ident())
    foo.n = 0
    
    with future_tools.CuteDummyExecutor() as executor:
        results = tuple(executor.map(foo, range(5)))
        zipped_results = tuple(zip(*results))
        assert zipped_results[0] == zipped_results[1] == tuple(range(5))
        assert len(set(zipped_results[2])) == 1
        assert len(set(zipped_results[3])) == 1
    
