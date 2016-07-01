# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import threading

from python_toolbox import cute_testing

from python_toolbox.nifty_collections import ConditionList


def test():
    c = ConditionList()
    assert list(c) == []
    assert 7 not in c
    assert len(c) == 0
    assert not c
    c.append(7)
    assert 7 in c
    assert len(c) == 1
    assert c
    c[0] = 'meow'
    assert 'meow' in c
    assert 7 not in c
    assert len(c) == 1
    assert c
    c.extend(range(3))
    assert list(c) == ['meow', 0, 1, 2]
    
    c = ConditionList([1, 2, 3])
    assert list(c) == [1, 2, 3]
    
def test_threaded():
    
    
    log_list = []
    log_list_lock = threading.RLock()
    
    c = ConditionList()
    
    
    class Thread(threading.Thread):
        def __init__(self, number):
            super().__init__()
            self.number = number
            
        def run(self):
            for i in range(10):
                c.wait_for('t%sm%s' % (self.number, i))
                with log_list_lock:
                    log_list.append('Thread %s achieved milestone %s')

    threads = tuple(map(Thread, range(10)))
    for thread in threads:
        thread.start()
    
    timings = [0, 1, 4, 7, 9, 9, 8, 8, 3, 5, 3, 9, 5, 2, 1, 1, 9, 8, 1, 7, 3,
               4, 9, 4, 5, 0, 1, 0, 9, 5, 0, 5, 4, 4, 5, 9, 3, 9, 2, 3, 8, 7,
               2, 2, 1, 3, 0, 0, 7, 6, 6, 8, 7, 6, 4, 6, 2, 6, 0, 1, 7, 8, 6,
               2, 9, 3, 4, 3, 0, 2, 5, 1, 4, 2, 4, 3, 0, 1, 7, 5, 4, 5, 8, 6,
               5, 2, 8, 6, 1, 2, 6, 6, 3, 0, 7, 7, 9, 8, 7, 8]
    # (Generated randomly, keeping static here to ensure reproducible test
    # runs.)
    
    expected_log_list = []
    expected_thread_states = [0] * 10
    for timing in timings:
        
        
        
    assert log_list == expected_log_list
    
    
    
    
                
            
            
            