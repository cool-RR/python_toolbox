# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import concurrent.futures
import time

from python_toolbox import future_tools


def test():
    
    def sleep_and_return(seconds):
        time.sleep(seconds)
        return seconds
        
    
    with future_tools.CuteThreadPoolExecutor(5) as executor:
        assert isinstance(executor, future_tools.CuteThreadPoolExecutor)
        assert tuple(executor.filter(lambda x: (x % 2 == 0), range(10))) == \
                                                         tuple(range(0, 10, 2))
        assert sorted(executor.filter(lambda x: (x % 2 == 0), range(10),
                                     timeout=10**5, as_completed=True)) == \
                                                          list(range(0, 10, 2))
        assert tuple(executor.filter(
            lambda x: (sleep_and_return(x) % 2 == 0), range(9, -1, -1),
            as_completed=True)) == (range(0, 10, 2))
        
        
        
        