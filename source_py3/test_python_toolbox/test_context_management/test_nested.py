# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Test the `python_toolbox.context_management.nested` function.'''

from python_toolbox import cute_testing

from python_toolbox.context_management import ReentrantContextManager, nested



def test_nested():
    '''Test the basic workings of `nested`.'''
    
    a = ReentrantContextManager()
    b = ReentrantContextManager()
    c = ReentrantContextManager()
    
    with nested(a):
        assert (a.depth, b.depth, c.depth) == (1, 0, 0)
        with nested(a, b):
            assert (a.depth, b.depth, c.depth) == (2, 1, 0)
            with nested(a, b, c):
                assert (a.depth, b.depth, c.depth) == (3, 2, 1)
                
        with nested(c):
            assert (a.depth, b.depth, c.depth) == (1, 0, 1)
            
    assert (a.depth, b.depth, c.depth) == (0, 0, 0)
            
            
