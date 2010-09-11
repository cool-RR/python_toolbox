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

            
prefix = __name__ + '.'


def test_get_object_by_address():

    ###########################################################################
    # Testing for locally defined class:
    
    assert get_object_by_address(prefix + 'A') is A
    assert get_object_by_address(prefix + 'A.B') is A.B
    assert get_object_by_address(prefix + 'A.method') == A.method
    assert get_object_by_address(prefix + 'A.B.deep_method') == A.B.deep_method
    assert get_object_by_address(prefix + 'A.C.D') is A.C.D
    assert get_object_by_address(prefix + 'A.C.D.deeper_method') == \
           A.C.D.deeper_method
    
    assert get_object_by_address('D.deeper_method', root=(prefix + 'A.C.D')) == \
           A.C.D.deeper_method
    assert get_object_by_address('D.deeper_method', root=A.C.D) == \
           A.C.D.deeper_method
    assert get_object_by_address('A', root=A) == A

    
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
    
    result = get_object_by_address('email.email.encoders.base64.b32decode')
    assert result is email.encoders.base64.b32decode
    
    result = get_object_by_address('base64.b32decode',
                                   root='email.email.encoders.base64')
    assert result is email.encoders.base64.b32decode
    
    
    ###########################################################################
    # Testing for garlicsim:
    
    result = get_object_by_address('garlicsim.general_misc')
    import garlicsim
    assert garlicsim.general_misc is result
    
    result = get_object_by_address('garlicsim.misc.persistent.'
                                   'cross_process_persistent.'
                                   'CrossProcessPersistent.personality')
    assert result is garlicsim.misc.persistent.cross_process_persistent.\
                     CrossProcessPersistent.personality
    
    result = get_object_by_address('data_structures.end.End',
                                   root=garlicsim.data_structures)
    assert result is garlicsim.data_structures.end.End
    
    
def test_get_address():
    
    ###########################################################################
    # Testing for locally defined class:
    
    #result = get_address(A.B)
    #assert result == prefix + 'A.B'
    #assert get_object_by_address(result) is A.B
    
    #result = get_address(A.C.D.deeper_method)
    #assert result == prefix + 'A.C.D.deeper_method'
    #assert get_object_by_address(result) == A.C.D.deeper_method
    
    #result = get_address(A.C.D.deeper_method, root=A.C)
    #assert result == 'C.D.deeper_method'
    #assert get_object_by_address(result, root=A.C) == A.C.D.deeper_method
    
    #result = get_address(A.C.D.deeper_method, root='A.C.D')
    #assert result == 'D.deeper_method'
    #assert get_object_by_address(result, root='A.C.D') == A.C.D.deeper_method
    
    
    ###########################################################################
    # Testing for standard-library module:
    
    import email.encoders
    result = get_address(email.encoders)
    assert result == 'email.encoders'
    assert get_object_by_address(result) is email.encoders
    
    result = get_address(email.encoders, root=email.encoders)
    assert result == 'encoders'
    assert get_object_by_address(result, root=email.encoders) is \
           email.encoders
    
    
    ###########################################################################
    # Testing for garlicsim:
    
    import garlicsim
    result = get_address(garlicsim.data_structures.state.State)
    assert result == 'garlicsim.data_structures.state.State'
    assert get_object_by_address(result) is \
           garlicsim.data_structures.state.State
    
    result = get_address(garlicsim.data_structures.state.State, shorten=True)
    assert result == 'garlicsim.data_structures.State'
    assert get_object_by_address(result) is \
           garlicsim.data_structures.state.State
    
    result = get_address(garlicsim.Project, shorten=True)
    assert result == 'garlicsim.Project'
    assert get_object_by_address(result) is \
           garlicsim.Project
    
    result = get_address(garlicsim.data_structures.state.State, root=garlicsim)
    assert result == 'garlicsim.data_structures.state.State'
    assert get_object_by_address(result, root=garlicsim) is \
           garlicsim.data_structures.state.State
    
    
    import garlicsim_lib.simpacks.life
    
    result = get_address(garlicsim_lib.simpacks.life.life.State.step)
    assert result == 'garlicsim_lib.simpacks.life.life.State.step'
    
    result = get_address(garlicsim_lib.simpacks.life.life.State.step,
                         shorten=True)
    assert result == 'garlicsim_lib.simpacks.life.State.step'
    
    result = get_address(garlicsim_lib.simpacks.life.life.State.step, root=life)
    assert result == 'life.life.State.step'
    
    result = get_address(garlicsim_lib.simpacks.life.life.State.step,
                         root=life, shorten=True)
    assert result == 'life.State.step'
    
    
    
    
    
    
    