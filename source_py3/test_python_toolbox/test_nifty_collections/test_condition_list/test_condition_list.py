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
    # This `log_list_lock` serves two purposes:
    # 1. Ensuring no two threads try to write to `log_list` at the same time.
    #    (Though the GIL might protect from that, I'm not sure, but it's
    #    implementation detail anyway.)
    # 2. Ensuring that only one thread runs at a time, so there won't be any 
    #    race conditions and the log list will be in the expected order. This 
    #    is done by acquiring this lock between releasing one milestone and the
    #    next.
    
    
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
                    
    
    milestones_release_order = [
        't6m3', 't9m4', 't1m4', 't1m8', 't6m0', 't7m7', 't4m4', 't5m1', 't8m8',
        't4m0', 't5m2', 't8m9', 't5m8', 't2m4', 't1m2', 't9m9', 't6m7', 't9m7',
        't1m9', 't8m3', 't6m8', 't7m5', 't5m4', 't3m6', 't0m5', 't4m2', 't6m9',
        't9m0', 't9m1', 't6m4', 't8m5', 't0m3', 't3m8', 't0m1', 't4m1', 't4m3',
        't3m3', 't1m7', 't5m0', 't8m0', 't2m1', 't6m1', 't1m1', 't9m6', 't3m7',
        't7m8', 't8m4', 't8m6', 't9m5', 't6m6', 't5m3', 't4m9', 't3m5', 't4m8',
        't0m6', 't3m1', 't0m8', 't5m5', 't4m6', 't3m0', 't7m0', 't2m5', 't5m7',
        't7m6', 't7m4', 't8m2', 't4m5', 't4m7', 't8m1', 't9m2', 't2m6', 't2m2',
        't1m6', 't2m3', 't1m5', 't2m8', 't0m0', 't6m2', 't1m3', 't7m1', 't2m0',
        't3m2', 't3m9', 't2m9', 't7m3', 't0m2', 't2m7', 't8m7', 't7m2', 't1m0',
        't0m4', 't0m9', 't0m7', 't6m5', 't9m8', 't5m6', 't3m4', 't5m9', 't7m9',
        't9m3'
    ]
    # (Generated randomly, keeping static here to ensure reproducible test
    # runs.)
    
    # First we're going to calculate the 
    
    expected_log_list = []
    expected_thread_states = [0] * 10
    for thread_number_to_advance in timings:
        expected_thread_state = expected_thread_state[thread_number_to_advance]
        c.append('')
        

    
    # And now, let the show begin!    
    threads = tuple(map(Thread, range(10)))
    for thread in threads:
        thread.start()
    for i, milestone in enumerate(milestones_release_order):
        with log_list_lock:
            assert len(log_list_lock) == i
        c.append(milestone)
        
    # This is the money line right here:
    assert log_list == expected_log_list
    
    
    
    
                
            
            
            