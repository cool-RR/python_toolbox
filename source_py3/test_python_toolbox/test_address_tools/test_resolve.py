# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.address_tools.resolve`.'''

import nose.tools

from python_toolbox.address_tools import describe, resolve


# Class tree we'll try to do some resolvings on:
class A:
    def method(self):
        pass
    class B:
        def deep_method(self):
            pass
    class C:
        def deep_method(self):
            pass
        class D:
            def deeper_method(self):
                pass
            

prefix = __name__ + '.'


def test_on_locally_defined_class():
    '''Test `resolve` on a locally defined class tree.'''
    
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

    
def test_on_stdlib():    
    '''Test `resolve` on stdlib modules.'''
    
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
    
    #result = resolve('email.email.encoders.base64.b32decode')
    #assert result is email.encoders.base64.b32decode
    
    #result = resolve('base64.b32decode',
                        #root='email.email.encoders.base64')
    #assert result is email.encoders.base64.b32decode
    
    #result = resolve('base64.b32decode',
                        #namespace='email.email.encoders')
    #assert result is email.encoders.base64.b32decode
    
    #result = resolve('base64.b32decode', root=marshal,
                        #namespace='email.email.encoders')
    #assert result is email.encoders.base64.b32decode
    
    assert resolve('object') is object
    
def test_python_toolbox():
    '''Test `resolve` on `python_toolbox` modules.'''
    
    result = resolve('python_toolbox.caching')
    import python_toolbox
    assert python_toolbox.caching is result
    
    ###########################################################################
    #                                                                         #
    result_0 = resolve('caching.cached_property.CachedProperty',
                       root=python_toolbox.caching)
    result_1 = resolve('caching.CachedProperty',
                       root=python_toolbox.caching)
    result_2 = resolve('caching.CachedProperty', namespace='python_toolbox')
    assert result_0 is result_1 is result_2 is \
                          python_toolbox.caching.cached_property.CachedProperty
    #                                                                         #
    ###########################################################################
    
    import email
    assert resolve('python_toolbox', namespace={'e': email}) == python_toolbox
    
    
def test_address_in_expression():
        
    result = resolve('[object, email.encoders, marshal]')
    import email, marshal, python_toolbox
    assert result == [object, email.encoders, marshal]
    
    assert resolve('[email.encoders, 7, (1, 3), marshal]') == \
           [email.encoders, 7, (1, 3), marshal]
    
    result = \
         resolve('{email: marshal, object: 7, python_toolbox: python_toolbox}')
    import python_toolbox
    assert result == {email: marshal, object: 7,
                      python_toolbox: python_toolbox}
    
    assert resolve('{email: marshal, '
                   'object: 7, '
                   'python_toolbox: python_toolbox}') == \
                    {email: marshal, object: 7, python_toolbox: python_toolbox}
    
    assert resolve('{CachedProperty: cache}',
                   namespace=python_toolbox.caching) == {
        python_toolbox.caching.CachedProperty: python_toolbox.caching.cache
    }
    
    assert resolve('{caching.CachedProperty: cute_testing}',
                   root=python_toolbox.caching,
                   namespace=python_toolbox) == \
          {python_toolbox.caching.CachedProperty: python_toolbox.cute_testing}

    assert resolve('python_toolbox if 4 else e', namespace={'e': email}) is \
           python_toolbox
    

def test_illegal_input():
    '''Test `resolve` raises exception when given illegal input.'''
    
    nose.tools.assert_raises(Exception,
                             resolve,
                             'asdgfasdgas if 4 else asdfasdfa ')
    
    nose.tools.assert_raises(Exception,
                             resolve,
                             'dgf sdfg sdfga ')
    
    nose.tools.assert_raises(Exception,
                             resolve,
                             '4- ')