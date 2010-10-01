from garlicsim.general_misc.address_tools import (get_address,
                                                  get_object)


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
            

prefix = __name__ + '.'


def test_get_object():

    ###########################################################################
    # Testing for locally defined class:
    
    assert get_object(prefix + 'A') is A
    assert get_object(prefix + 'A.B') is A.B
    assert get_object(prefix + 'A.method') == A.method
    assert get_object('method', namespace=A) == A.method
    assert get_object(prefix + 'A.B.deep_method') == A.B.deep_method
    assert get_object('B.deep_method', namespace=A) == A.B.deep_method
    assert get_object(prefix + 'A.C.D') is A.C.D
    assert get_object(prefix + 'A.C.D.deeper_method') == \
           A.C.D.deeper_method
    
    assert get_object('D.deeper_method', root=(prefix + 'A.C.D')) == \
           A.C.D.deeper_method
    assert get_object('D.deeper_method', root=A.C.D, namespace='email') == \
           A.C.D.deeper_method
    assert get_object('A', root=A) == A

    
    ###########################################################################
    # Testing for standard-library modules:
    
    result = get_object('email')
    import email
    import marshal
    assert result is email
    
    assert get_object('email') is \
           get_object('email.email') is \
           get_object('email.email.email') is \
           get_object('email.email.email.email') is email
    
    result = get_object('email.base64mime.a2b_base64')
    assert result is email.base64mime.a2b_base64
    
    result = get_object('email.email.encoders.base64.b32decode')
    assert result is email.encoders.base64.b32decode
    
    result = get_object('base64.b32decode',
                        root='email.email.encoders.base64')
    assert result is email.encoders.base64.b32decode
    
    result = get_object('base64.b32decode',
                        namespace='email.email.encoders')
    assert result is email.encoders.base64.b32decode
    
    result = get_object('base64.b32decode', root=marshal,
                        namespace='email.email.encoders')
    assert result is email.encoders.base64.b32decode
    
    
    ###########################################################################
    # Testing for garlicsim:
    
    result = get_object('garlicsim.general_misc')
    import garlicsim
    assert garlicsim.general_misc is result
    
    result = get_object('garlicsim.misc.persistent.cross_process_persistent.'
                        'CrossProcessPersistent.personality')
    result2 = get_object('misc.CrossProcessPersistent.personality',
                         namespace=garlicsim)
    result3 = get_object('persistent.CrossProcessPersistent.personality',
                         root=garlicsim.misc.persistent,
                         namespace='email')
    assert result is result2 is result3 is garlicsim.misc.persistent.\
           cross_process_persistent.CrossProcessPersistent.personality
    
    result = get_object('data_structures.end.End',
                        root=garlicsim.data_structures)
    result2 = get_object('data_structures.End',
                        root=garlicsim.data_structures)
    result3 = get_object('data_structures.End', namespace='garlicsim')
    assert result is result2 is garlicsim.data_structures.end.End
    