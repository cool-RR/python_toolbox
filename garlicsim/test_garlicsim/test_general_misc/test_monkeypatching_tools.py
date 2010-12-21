# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim.general_misc.monkeypatching_tools`.'''

from garlicsim.general_misc import monkeypatching_tools


def test():
    '''Test basic workings of `monkeypatch_method`.'''
    
    class A(object):
        pass

    @monkeypatching_tools.monkeypatch_method(A)
    def meow(a):
        return 1
    
    a = A()
    
    assert a.meow() == meow(a) == 1
    
    @monkeypatching_tools.monkeypatch_method(A, 'roar')
    def woof(a):
        return 2
    
    assert a.roar() == woof(a) == 2
    
    assert not hasattr(a, 'woof')
    
    del meow, woof