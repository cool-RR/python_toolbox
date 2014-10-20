# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.caching.CachedType`.'''

from python_toolbox.caching import CachedType

        
def test():
    '''Test basic workings of `CachedType`.'''
    class A(object):
        __metaclass__ = CachedType
        def __init__(self, a=1, b=2, *args, **kwargs):
            pass
        
    assert A() is A(1) is A(b=2) is A(1, 2) is A(1, b=2)
    assert A() is not A(3) is not A(b=7) is not A(1, 2, 'meow') is not A(x=9)
    