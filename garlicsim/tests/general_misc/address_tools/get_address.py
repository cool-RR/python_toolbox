from garlicsim.general_misc.address_tools import (get_address,
                                                  get_object)


prefix = __name__ + '.'    
    
def test_get_address():
    
    ###########################################################################
    # Testing for locally defined class:
    
    # Currently these tests are commented out, because `get_address` doesn't
    # support nested classes yet.
    
    #result = get_address(A.B)
    #assert result == prefix + 'A.B'
    #assert get_object(result) is A.B
    
    #result = get_address(A.C.D.deeper_method)
    #assert result == prefix + 'A.C.D.deeper_method'
    #assert get_object(result) == A.C.D.deeper_method
    
    #result = get_address(A.C.D.deeper_method, root=A.C)
    #assert result == 'C.D.deeper_method'
    #assert get_object(result, root=A.C) == A.C.D.deeper_method
    
    #result = get_address(A.C.D.deeper_method, root='A.C.D')
    #assert result == 'D.deeper_method'
    #assert get_object(result, root='A.C.D') == A.C.D.deeper_method
    
    
    ###########################################################################
    # Testing for standard-library module:
    
    import email.encoders
    result = get_address(email.encoders)
    assert result == 'email.encoders'
    assert get_object(result) is email.encoders
    
    result = get_address(email.encoders, root=email.encoders)
    assert result == 'encoders'
    assert get_object(result, root=email.encoders) is email.encoders
    
    result = get_address(email.encoders, namespace=email)
    assert result == 'encoders'
    assert get_object(result, namespace=email) is email.encoders
    
    result = get_address(email.encoders, root=email.encoders, namespace=email)
    assert result == 'encoders'
    assert get_object(result, root=email.encoders, namespace=email) is \
           email.encoders
    
    
    ###########################################################################
    # Testing for garlicsim:
    
    import garlicsim
    result = get_address(garlicsim.data_structures.state.State)
    assert result == 'garlicsim.data_structures.state.State'
    assert get_object(result) is garlicsim.data_structures.state.State
    
    result = get_address(garlicsim.data_structures.state.State, shorten=True)
    assert result == 'garlicsim.data_structures.State'
    assert get_object(result) is garlicsim.data_structures.state.State
    
    result = get_address(garlicsim.Project, shorten=True)
    assert result == 'garlicsim.Project'
    assert get_object(result) is garlicsim.Project
    
    # When a root or namespace is given, it's top priority to use it, even if it
    # prevents shorterning and results in an overall longer address:
    result = get_address(garlicsim.Project, shorten=True,
                         root=garlicsim.asynchronous_crunching)
    assert result == 'asynchronous_crunching.Project'
    assert get_object(result, root=garlicsim.asynchronous_crunching) is \
           garlicsim.Project
    
    result = get_address(garlicsim.Project, shorten=True,
                         namespace=garlicsim)
    assert result == 'Project'
    assert get_object(result, namespace=garlicsim) is garlicsim.Project
    
    result = get_address(garlicsim.Project, shorten=True,
                         namespace=garlicsim.__dict__)
    assert result == 'Project'
    assert get_object(result, namespace=garlicsim.__dict__) is \
           garlicsim.Project
    
    result = get_address(garlicsim.Project, shorten=True,
                         namespace='garlicsim')
    assert result == 'Project'
    assert get_object(result, namespace='garlicsim') is garlicsim.Project
    
    result = get_address(garlicsim.Project, shorten=True,
                         namespace='garlicsim.__dict__')
    assert result == 'Project'
    assert get_object(result, namespace='garlicsim.__dict__') is \
           garlicsim.Project
    
    result = get_address(garlicsim.data_structures.state.State, root=garlicsim)
    assert result == 'garlicsim.data_structures.state.State'
    assert get_object(result, root=garlicsim) is \
           garlicsim.data_structures.state.State
    
    
    import garlicsim_lib.simpacks.life
    
    result = get_address(garlicsim_lib.simpacks.life.life.State.step)
    assert result == 'garlicsim_lib.simpacks.life.life.State.step'
    
    result = get_address(garlicsim_lib.simpacks.life.life.State.step,
                         shorten=True)
    assert result == 'garlicsim_lib.simpacks.life.State.step'
    
    result = get_address(garlicsim_lib.simpacks.life.life.State.step,
                         root=garlicsim_lib.simpacks.life)
    assert result == 'life.life.State.step'
    
    result = get_address(garlicsim_lib.simpacks.life.life.State.step,
                         namespace=garlicsim_lib.simpacks)
    assert result == 'life.life.State.step'
    
    result = get_address(garlicsim_lib.simpacks.life.life.State.step,
                         root=garlicsim_lib.simpacks.life, shorten=True)
    assert result == 'life.State.step'
    
    
    ###########################################################################
    # Testing for local modules:
    
    from .sample_module_tree import w
    
    z = get_object('w.x.y.z', root=w)

    result = get_address(z, root=w)
    assert result == 'w.x.y.z'
    
    result = get_address(z, shorten=True, root=w)
    assert result == 'w.y.z'
    
    result = get_address(z, shorten=True, root=w)
    assert result == 'w.y.z'
    
    result = get_address(z, shorten=True, root=w, namespace='email')
    assert result == 'w.y.z'
    
    result = get_address(z, shorten=True, root=garlicsim, namespace='w')
    assert result == 'x.y.z'
    
    result = get_address(z, shorten=True, root=w.x)
    assert result == 'x.y.z'
    
    

    
    
    
    
    
    