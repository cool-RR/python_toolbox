# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import threading
import time
import queue as queue_module

from python_toolbox import queue_tools
from python_toolbox import cute_iter_tools
from python_toolbox import sequence_tools
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
    
    thread_started_queue = queue_module.Queue()
    
    class Thread(threading.Thread):
        def __init__(self, number):
            super().__init__()
            self.number = number
            
        def run(self):
            thread_started_queue.put(self.number)
            for i in range(10):
                milestone = 't%sm%s' % (self.number, i)
                c.is_waiting = True
                c.wait_for(milestone)
                with log_list_lock:
                    log_list.append(milestone)
                    
    
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
    milestones_in_the_bank = [set() for _ in range(10)]
    def get_thread_state(number):
        for i in range(0, 10):
            milestones_in_the_bank_for_thread = milestones_in_the_bank[number]
            if i not in milestones_in_the_bank_for_thread:
                return i - 1
        return 9
            
    for milestone in milestones_release_order:
        thread_number = int(milestone[1])
        milestone_number = int(milestone[3])
        old_thread_state = get_thread_state(thread_number)
        milestones_in_the_bank[thread_number].add(milestone_number)
        new_thread_state = get_thread_state(thread_number)
        for milestone_accomplished in range(old_thread_state + 1,
                                             new_thread_state + 1):
            expected_log_list.append('t%sm%s' %
                                     (thread_number, milestone_accomplished))
    assert len(expected_log_list) == 100
    assert not sequence_tools.get_recurrences(expected_log_list)
    
    # Start your engines...
    threads = tuple(map(Thread, range(10)))
    for thread in threads:
        thread.start()
    
    # This waits for all the threads to start:
    assert sorted(
        cute_iter_tools.shorten(queue_tools.iterate(thread_started_queue), 10)
    ) == list(range(10))
    
    time.sleep(1)
    
    # And now, let the show begin!
    for i, milestone in enumerate(milestones_release_order):
        with log_list_lock:
            assert len(log_list) <= i
        c.append(milestone)
        
        # Ensure that all threads advanced if they should, by ensuring that the
        # condition lock is free:
        with c:
            pass
        
    # This is the money line right here:
    assert log_list == expected_log_list
    
    
    
    
                
            
            
            