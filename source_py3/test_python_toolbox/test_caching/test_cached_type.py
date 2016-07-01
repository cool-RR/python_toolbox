# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import uuid as uuid_module

from python_toolbox.caching import CachedType

        
def test():
    '''Test basic workings of `CachedType`.'''
    class A(metaclass=CachedType):
        def __init__(self, a=1, b=2, *args, **kwargs):
            pass
        
    assert A() is A(1) is A(b=2) is A(1, 2) is A(1, b=2)
    assert A() is not A(3) is not A(b=7) is not A(1, 2, 'meow') is not A(x=9)
    
    
class Feline(metaclass=CachedType):
    def __init__(self, name):
        self.name = name
        self.uuid = uuid_module.uuid4().hex
        self.creation_hook()
        
    creation_hook = lambda self: None
    
def test_thread_safe():
    f1 =