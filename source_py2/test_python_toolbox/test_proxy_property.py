# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing modules for `python_toolbox.misc_tools.ProxyProperty`.'''

import uuid

from python_toolbox import cute_testing

from python_toolbox.misc_tools import ProxyProperty


class Object(object):
    pass


def test():
    
    class A(object):
        y = 'y'
        def __init__(self):
            self.x = 'x'
            self.obj = Object()
            self.obj.z = 'z'
            self.uuid = uuid.uuid4()
            
        x_proxy = ProxyProperty('.x')
        y_proxy = ProxyProperty(
            '.y',
            doc='Proxy for `y`.'
        )
        z_proxy = ProxyProperty('.obj.z', doc='aye, this my favorite z.')
        uuid_proxy = ProxyProperty(
            '.uuid',
            'Object-specific UUID.'
        )
        nonexistant_proxy = ProxyProperty('.whatevs')
        
    assert isinstance(A.x_proxy, ProxyProperty)
    assert isinstance(A.y_proxy, ProxyProperty)
    assert isinstance(A.z_proxy, ProxyProperty)
    assert isinstance(A.uuid_proxy, ProxyProperty)
    assert isinstance(A.nonexistant_proxy, ProxyProperty)
    
    a0 = A()
    a1 = A()
    
    assert a0.x_proxy == a1.x_proxy == 'x'
    assert a0.y_proxy == a1.y_proxy == 'y'
    assert a0.z_proxy == a1.z_proxy == 'z'
    assert isinstance(a0.uuid_proxy, uuid.UUID)
    assert isinstance(a1.uuid_proxy, uuid.UUID)
    assert a0.uuid == a0.uuid_proxy != a1.uuid_proxy == a1.uuid
    with cute_testing.RaiseAssertor(AttributeError):
        a0.nonexistant_proxy
    with cute_testing.RaiseAssertor(AttributeError):
        a1.nonexistant_proxy
        
    ### Setting proxy-properties to different values: #########################
    #                                                                         #
    a0.x_proxy = 7
    assert a0.x_proxy == 7 != a1.x_proxy == 'x'
        
    a0.y_proxy = 'meow'
    assert a0.y_proxy == 'meow' != a1.y_proxy == 'y'
        
    a0.z_proxy = [1, 2, 3]
    assert a0.z_proxy == [1, 2, 3] != a1.z_proxy == 'z'
    #                                                                         #
    ### Finished setting proxy-properties to different values. ################

    assert repr(A.x_proxy) == '''<ProxyProperty: '.x'>'''
    assert repr(A.z_proxy) == ('''<ProxyProperty: '.obj.z', doc='aye, this '''
                               '''my favorite z.'>''')


def test_dot():
    '''Text that `ProxyProperty` complains when there's no prefixing dot.'''
    
    with cute_testing.RaiseAssertor(text="The `attribute_name` must start "
                                    "with a dot to make it clear it's an "
                                    "attribute. 'y' does not start with a "
                                    "dot."):
        class A(object):
            y = 'y'
            x = ProxyProperty('y')
            
    