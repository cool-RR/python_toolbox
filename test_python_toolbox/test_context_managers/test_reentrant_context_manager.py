# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `context_managers.ReentrantContextManager`.''' 

from __future__ import with_statement

from garlicsim.general_misc.context_managers import ReentrantContextManager
from garlicsim.general_misc import cute_testing


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
    assert my_set == set([0, 1, 2, 3, 4])
        
        