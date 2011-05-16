# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `ReentrantContextManager`.'''

from garlicsim.general_misc.context_managers import ReentrantContextManager


def test_reentrant_context_manager():
    
    class MyReentrantContextManager(ReentrantContextManager):
        def __init__(self):
            self.times_entered = 0
            self.times_exited = 0        
        def reentrant_enter(self):
            self.times_entered += 1
            return self.times_entered
        def reentrant_exit(self):
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
            