# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Testing modules for `garlicsim.general_misc.proxy_property.ProxyProperty`.
'''

from __future__ import with_statement

import uuid

from garlicsim.general_misc import cute_testing

from garlicsim.general_misc.proxy_property import ProxyProperty


class Object(object):
    ''' '''        


def test():
    
    class A(object):
        ''' '''
        y = 'y'
        def __init__(self):
            self.x = 'x'
            self.obj = Object()
            self.obj.z = 'z'
            self.uuid = uuid.uuid4()
            
        x_proxy = ProxyProperty('x')
        y_proxy = ProxyProperty(
            'y',
            doc='Proxy for `y`.'
        )
        z_proxy = ProxyProperty('obj.z')
        uuid_proxy = ProxyProperty(
            'uuid',
            'Object-specific UUID.'
        )
        nonexistant_proxy = ProxyProperty('whatevs')
        
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