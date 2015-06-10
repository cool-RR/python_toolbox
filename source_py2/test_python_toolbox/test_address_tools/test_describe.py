# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.address_tools.describe`.'''


import nose

from python_toolbox import import_tools
from python_toolbox.temp_value_setting import TempValueSetter

import python_toolbox
from python_toolbox.address_tools import describe, resolve

# todo: Make test that when a root or namespace is given, it's top priority to
# use it, even if it prevents shorterning and results in an overall longer
# address.


prefix = __name__ + '.'



def test_on_locally_defined_class():
    
    ###########################################################################
    # Testing for locally defined class:
    
    
    raise nose.SkipTest("This test doesn't currently pass because `describe` "
                        "doesn't support nested classes yet.")
    
    result = describe(A.B)
    assert result == prefix + 'A.B'
    assert resolve(result) is A.B
    
    result = describe(A.C.D.deeper_method)
    assert result == prefix + 'A.C.D.deeper_method'
    assert resolve(result) == A.C.D.deeper_method
    
    result = describe(A.C.D.deeper_method, root=A.C)
    assert result == 'C.D.deeper_method'
    assert resolve(result, root=A.C) == A.C.D.deeper_method
    
    result = describe(A.C.D.deeper_method, root='A.C.D')
    assert result == 'D.deeper_method'
    assert resolve(result, root='A.C.D') == A.C.D.deeper_method
    
    
def test_on_stdlib():
    '''Test `describe` for various stdlib modules.'''
    
    import email.encoders
    result = describe(email.encoders)
    assert result == 'email.encoders'
    assert resolve(result) is email.encoders
    
    result = describe(email.encoders, root=email.encoders)
    assert result == 'encoders'
    assert resolve(result, root=email.encoders) is email.encoders
    
    result = describe(email.encoders, namespace=email)
    assert result == 'encoders'
    assert resolve(result, namespace=email) is email.encoders
    
    result = describe(email.encoders, root=email.encoders, namespace=email)
    assert result == 'encoders'
    assert resolve(result, root=email.encoders, namespace=email) is \
           email.encoders
    
    
def test_on_python_toolbox():
    '''Test `describe` for various `python_toolbox` modules.'''
    
    import python_toolbox.caching
    result = describe(python_toolbox.caching.cached_property.CachedProperty)
    assert result == 'python_toolbox.caching.cached_property.CachedProperty'
    assert resolve(result) is \
                          python_toolbox.caching.cached_property.CachedProperty
    
    result = describe(python_toolbox.caching.cached_property.CachedProperty,
                      shorten=True)
    assert result == 'python_toolbox.caching.CachedProperty'
    assert resolve(result) is \
                          python_toolbox.caching.cached_property.CachedProperty
    
    import python_toolbox.nifty_collections
    result = describe(python_toolbox.nifty_collections.weak_key_default_dict.
                                                            WeakKeyDefaultDict,
                      shorten=True,
                      root=python_toolbox.nifty_collections.
                                                         weak_key_default_dict)
    assert result == 'weak_key_default_dict.WeakKeyDefaultDict'
    assert resolve(
        result,
        root=python_toolbox.nifty_collections.weak_key_default_dict
        ) is python_toolbox.nifty_collections.WeakKeyDefaultDict
    
    result = describe(python_toolbox.caching.cached_property.CachedProperty,
                      shorten=True,
                      namespace=python_toolbox)
    assert result == 'caching.CachedProperty'
    assert resolve(result, namespace=python_toolbox) is \
                                          python_toolbox.caching.CachedProperty
    
    result = describe(python_toolbox.caching.CachedProperty, shorten=True,
                      namespace=python_toolbox.__dict__)
    assert result == 'caching.CachedProperty'
    assert resolve(result, namespace=python_toolbox.__dict__) is \
           python_toolbox.caching.CachedProperty
    
    result = describe(python_toolbox.caching.CachedProperty, shorten=True,
                      namespace='python_toolbox')
    assert result == 'caching.CachedProperty'
    assert resolve(result, namespace='python_toolbox') is \
                                          python_toolbox.caching.CachedProperty
    
    result = describe(python_toolbox.caching.CachedProperty, shorten=True,
                      namespace='python_toolbox.__dict__')
    assert result == 'caching.CachedProperty'
    assert resolve(result, namespace='python_toolbox.__dict__') is \
           python_toolbox.caching.CachedProperty
    
    result = describe(python_toolbox.caching.cached_property.CachedProperty,
                      root=python_toolbox)
    assert result == 'python_toolbox.caching.cached_property.CachedProperty'
    assert resolve(result, root=python_toolbox) is \
                          python_toolbox.caching.cached_property.CachedProperty
    
    
def test_on_local_modules():
    '''Test `describe` on local, relatively-imported modules.'''
    import python_toolbox
    
    from .sample_module_tree import w
    
    z = resolve('w.x.y.z', root=w)

    result = describe(z, root=w)
    assert result == 'w.x.y.z'
    
    result = describe(z, shorten=True, root=w)
    assert result == 'w.y.z'
    
    result = describe(z, shorten=True, root=w)
    assert result == 'w.y.z'
    
    result = describe(z, shorten=True, root=w, namespace='email')
    assert result == 'w.y.z'
    
    result = describe(z, shorten=True, root=python_toolbox, namespace=w)
    assert result == 'y.z'
    
    result = describe(z, shorten=True, root=w.x)
    assert result == 'x.y.z'
    
    
def test_on_ignore_confusing_namespace():
    '''Test that `describe` doesn't use a confusing namespace item.'''
    import email.encoders
    import marshal
    
    result = describe(
        email,
        shorten=True,
        namespace={'e': email}
    )
    assert result == 'email' # Not shortening to 'e', that would be confusing.
    
    result = describe(
        email.encoders,
        namespace={'e': email, 'email': email}
    )
    assert result == 'email.encoders'
    
    result = describe(
        email.encoders,
        root=marshal,
        namespace={'e': email, 'email': email}
    )
    assert result == 'email.encoders'
    
    
    
def test_address_in_expression():
    '''Test `describe` works for an address inside an expression.'''
    
    import email.encoders
    import marshal
    
    assert describe([object, email.encoders, marshal]) == \
           '[object, email.encoders, marshal]'
    
    assert describe([email.encoders, 7, (1, 3), marshal]) == \
           '[email.encoders, 7, (1, 3), marshal]'
    

def test_multiprocessing_lock():
    '''Test `describe` works for `multiprocessing.Lock()`.'''
    import multiprocessing
    lock = multiprocessing.Lock()
    describe(lock)
    
    
def test_bad_module_name():
    '''
    Test `describe` works for objects with bad `__module__` attribute.
    
    The `__module__` attribute usually says where an object can be reached. But
    in some cases, like when working in a shell, you can't really access the
    objects from that non-existant module. So `describe` must not fail for
    these cases.
    '''
    
    import email

    non_sensical_module_name = '__whoop_dee_doo___rrrar'
    
    my_locals = locals().copy()
    my_locals['__name__'] = non_sensical_module_name
    
    exec 'def f(): pass' in my_locals
    exec ('class A(object):\n'
          '    def m(self): pass\n') in my_locals
    
    f, A = my_locals['f'], my_locals['A']
    
    assert describe(f) == \
        '.'.join((non_sensical_module_name, 'f'))
    assert describe(f, shorten=True, root=email, namespace={}) == \
        '.'.join((non_sensical_module_name, 'f'))
    
    assert describe(A) == \
        '.'.join((non_sensical_module_name, 'A'))
    assert describe(A, shorten=True, root=email, namespace={}) == \
        '.'.join((non_sensical_module_name, 'A'))
    
    assert describe(A.m) == \
        '.'.join((non_sensical_module_name, 'A.m'))
    assert describe(A.m, shorten=True, root=email, namespace={}) == \
        '.'.join((non_sensical_module_name, 'A.m'))
    

def test_function_in_something():
    '''Test `describe` doesn't fail when describing `{1: sum}`.'''
    raise nose.SkipTest("This test doesn't pass yet.")
    assert describe({1: sum}) == '{1: sum}'
    assert describe((sum, sum, list, chr)) == '(sum, sum, list, chr)'
    

def test_function_in_main():
    '''Test that a function defined in `__main__` is well-described.'''

    ###########################################################################
    # We can't really define a function in `__main__` in this test, so we
    # emulate it:
    with TempValueSetter((globals(), '__name__'), '__main__'):
        def f(x):
            pass
        
        # Accessing `f.__module__` here so PyPy will calculate it:
        assert f.__module__ == '__main__'
        
    assert f.__module__ == '__main__'
    import __main__
    __main__.f = f
    del __main__
    #
    ###########################################################################
    
    assert describe(f) == '__main__.f'
    assert resolve(describe(f)) is f
    
    
