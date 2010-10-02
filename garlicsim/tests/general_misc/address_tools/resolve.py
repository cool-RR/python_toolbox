from garlicsim.general_misc.address_tools import describe, resolve


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


def test_locally_defined_class():
    
    assert resolve(prefix + 'A') is A
    assert resolve(prefix + 'A.B') is A.B
    assert resolve(prefix + 'A.method') == A.method
    assert resolve('method', namespace=A) == A.method
    assert resolve(prefix + 'A.B.deep_method') == A.B.deep_method
    assert resolve('B.deep_method', namespace=A) == A.B.deep_method
    assert resolve(prefix + 'A.C.D') is A.C.D
    assert resolve(prefix + 'A.C.D.deeper_method') == \
           A.C.D.deeper_method
    
    assert resolve('D.deeper_method', root=(prefix + 'A.C.D')) == \
           A.C.D.deeper_method
    assert resolve('D.deeper_method', root=A.C.D, namespace='email') == \
           A.C.D.deeper_method
    assert resolve('A', root=A) == A

    
def test_stdlib():
    
    result = resolve('email')
    import email
    import marshal
    assert result is email
    
    assert resolve('email') is \
           resolve('email.email') is \
           resolve('email.email.email') is \
           resolve('email.email.email.email') is email
    
    result = resolve('email.base64mime.a2b_base64')
    assert result is email.base64mime.a2b_base64
    
    result = resolve('email.email.encoders.base64.b32decode')
    assert result is email.encoders.base64.b32decode
    
    result = resolve('base64.b32decode',
                        root='email.email.encoders.base64')
    assert result is email.encoders.base64.b32decode
    
    result = resolve('base64.b32decode',
                        namespace='email.email.encoders')
    assert result is email.encoders.base64.b32decode
    
    result = resolve('base64.b32decode', root=marshal,
                        namespace='email.email.encoders')
    assert result is email.encoders.base64.b32decode
    
    
def test_garlicsim():
    
    result = resolve('garlicsim.general_misc')
    import garlicsim
    assert garlicsim.general_misc is result
    
    result = resolve('garlicsim.misc.persistent.cross_process_persistent.'
                        'CrossProcessPersistent.personality')
    result2 = resolve('misc.CrossProcessPersistent.personality',
                         namespace=garlicsim)
    result3 = resolve('persistent.CrossProcessPersistent.personality',
                         root=garlicsim.misc.persistent,
                         namespace='email')
    assert result is result2 is result3 is garlicsim.misc.persistent.\
           cross_process_persistent.CrossProcessPersistent.personality
    
    result = resolve('data_structures.end.End',
                        root=garlicsim.data_structures)
    result2 = resolve('data_structures.End',
                        root=garlicsim.data_structures)
    result3 = resolve('data_structures.End', namespace='garlicsim')
    assert result is result2 is garlicsim.data_structures.end.End
    
    import email
    assert resolve('garlicsim', namespace={'e': email})
    
    
def test_address_in_expression():
        
    result = resolve('[object, email.encoders, marshal]')
    import email, marshal, garlicsim
    assert result == [object, email.encoders, marshal]
    
    assert resolve('[email.encoders, 7, (1, 3), marshal]') == \
           [email.encoders, 7, (1, 3), marshal]
    
    result = resolve('{email: marshal, object: 7, garlicsim: garlicsim}')
    import garlicsim
    assert result == {email: marshal, object: 7, garlicsim: garlicsim}
    
    assert resolve('{email: marshal, object: 7, garlicsim: garlicsim}') == \
           {email: marshal, object: 7, garlicsim: garlicsim}
    
    assert resolve('{Project: simulate}', namespace=garlicsim) == \
           {garlicsim.Project: garlicsim.simulate}
    
    assert resolve('{asynchronous_crunching.Project: simulate}',
                   root=garlicsim.asynchronous_crunching,
                   namespace=garlicsim) == \
           {garlicsim.asynchronous_crunching.Project: garlicsim.simulate}

    assert resolve('garlicsim if 4 else e', namespace={'e': email}) is \
           garlicsim
    
    