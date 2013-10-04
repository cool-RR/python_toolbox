# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `context_management.ReentrantContextManager`.''' 

import Queue as queue_module

from python_toolbox.context_management import ReentrantContextManager
from python_toolbox import cute_testing


class MyException(Exception):
    pass


def test_reentrant_context_manager():
    '''Test the basic workings of `ReentrantContextManager`.'''
    
    class MyReentrantContextManager(ReentrantContextManager):
        def __init__(self):
            self.times_entered = 0
            self.times_exited = 0        
        def reentrant_enter(self):
            self.times_entered += 1
            return self.times_entered
        def reentrant_exit(self, exc_type, exc_value, exc_traceback):
            self.times_exited += 1
           
    my_rcm = MyReentrantContextManager()
    assert my_rcm.times_entered == 0
    assert my_rcm.times_exited == 0
    
    with my_rcm as enter_return_value:
        assert enter_return_value == 1
        assert my_rcm.times_entered == 1
        assert my_rcm.times_exited == 0
        with my_rcm as enter_return_value:
            with my_rcm as enter_return_value:
                assert enter_return_value == 1
                assert my_rcm.times_entered == 1
                assert my_rcm.times_exited == 0
            assert enter_return_value == 1
            assert my_rcm.times_entered == 1
            assert my_rcm.times_exited == 0
            
    assert my_rcm.times_entered == 1
    assert my_rcm.times_exited == 1
    
    with my_rcm as enter_return_value:
        assert enter_return_value == 2
        assert my_rcm.times_entered == 2
        assert my_rcm.times_exited == 1
        with my_rcm as enter_return_value:
            with my_rcm as enter_return_value:
                assert enter_return_value == 2
                assert my_rcm.times_entered == 2
                assert my_rcm.times_exited == 1
            assert enter_return_value == 2
            assert my_rcm.times_entered == 2
            assert my_rcm.times_exited == 1
            
    
    
    with cute_testing.RaiseAssertor(MyException):
        with my_rcm as enter_return_value:
            assert enter_return_value == 3
            assert my_rcm.times_entered == 3
            assert my_rcm.times_exited == 2
            with my_rcm as enter_return_value:
                with my_rcm as enter_return_value:
                    assert enter_return_value == 3
                    assert my_rcm.times_entered == 3
                    assert my_rcm.times_exited == 2
                assert enter_return_value == 3
                assert my_rcm.times_entered == 3
                assert my_rcm.times_exited == 2
                raise MyException
            
            
def test_exception_swallowing():
    class SwallowingReentrantContextManager(ReentrantContextManager):
        def __init__(self):
            self.times_entered = 0
            self.times_exited = 0
        def reentrant_enter(self):
            self.times_entered += 1
            return self
        def reentrant_exit(self, exc_type, exc_value, exc_traceback):
            self.times_exited += 1
            if isinstance(exc_value, MyException):
                return True
            
    swallowing_rcm = SwallowingReentrantContextManager()
    
    my_set = set()
    
    with swallowing_rcm:
        my_set.add(0)
        with swallowing_rcm:
            my_set.add(1)
            with swallowing_rcm:
                my_set.add(2)
                with swallowing_rcm:
                    my_set.add(3)
                    with swallowing_rcm:
                        my_set.add(4)
                        raise MyException
                    my_set.add(5)
                my_set.add(6)
            my_set.add(7)
        my_set.add(8)
    assert my_set == {0, 1, 2, 3, 4}
        

        
def test_order_of_depth_modification():
    ''' '''
     
    depth_log = queue_module.Queue()
    
    class JohnnyReentrantContextManager(ReentrantContextManager):
        def reentrant_enter(self):
            depth_log.put(self.depth)
            return self
        def reentrant_exit(self, exc_type, exc_value, exc_traceback):
            depth_log.put(self.depth)
        
    johnny_reentrant_context_manager = JohnnyReentrantContextManager()
    assert johnny_reentrant_context_manager.depth == 0
    with johnny_reentrant_context_manager:
        assert johnny_reentrant_context_manager.depth == 1
        
        # `reentrant_enter` saw a depth of 0, because the depth increment
        # happens *after* `reentrant_enter` is called:
        assert depth_log.get(block=False) == 0
        
        with johnny_reentrant_context_manager:
            
            assert johnny_reentrant_context_manager.depth == 2
            assert depth_log.qsize() == 0 # We're in a depth greater than 1,
                                          # so `reentrant_enter` wasn't even
                                          # called.
                                          
        assert johnny_reentrant_context_manager.depth == 1
        
        assert depth_log.qsize() == 0 # We came out of a depth greater than 1,
                                      # so `reentrant_exit` wasn't even called.
                                      
    # `reentrant_exit` saw a depth of 1, because the depth decrement happens
    # *after* `reentrant_exit` is called:
    assert depth_log.get(block=False) == 1