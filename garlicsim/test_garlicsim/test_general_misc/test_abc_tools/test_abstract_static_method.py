import nose

from garlicsim.general_misc.abc_tools import abstract_static_method
from garlicsim.general_misc.third_party import abc


def test():
    
    class A(object):
        __metaclass__ = abc.ABCMeta
        
        @abstract_static_method
        def f():
            pass
        
    nose.tools.assert_raises(TypeError, lambda: A())
    
    class B(A):
        @staticmethod
        def f():
            return 7
        
    b = B()
    
    assert B.f() == b.f() == 7