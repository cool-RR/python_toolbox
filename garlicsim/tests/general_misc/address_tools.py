from garlicsim.general_misc.address_tools import *

class A(object):
    def method(self):
        pass
    class B(object):
        def deep_method(self):
            pass
    class C(object):
        def deep_method(self):
            pass
        class D(object):
            def deeper_method(self):
                pass
            
def test_get_object_by_address():

    prefix = __name__ + '.'

    ###########################################################################
    # Testing for locally defined class:
    
    assert get_object_by_address(prefix + 'A') is A
    assert get_object_by_address(prefix + 'A.B') is A.B
    assert get_object_by_address(prefix + 'A.deep_method') == A.deep_method
    assert get_object_by_address(prefix + 'A.B.deep_method') == A.B.deep_method
    assert get_object_by_address(prefix + 'A.C.D') is A.C.D
    assert get_object_by_address(prefix + 'A.C.D.deep_method') == \
           A.C.D.deep_method

    
    ###########################################################################
    # Testing for standard-library modules:
    
    result = get_object_by_address('email')
    import email
    assert result is email
    
    assert get_object_by_address('email') is \
           get_object_by_address('email.email') is \
           get_object_by_address('email.email.email') is \
           get_object_by_address('email.email.email.email') is email
    
    result = get_object_by_address('email.base64mime.a2b_base64')
    assert result is email.base64mime.a2b_base64
    
    result = get_object_by_address('email.base64mime.a2b_base64')
    assert result is email.base64mime.a2b_base64
    