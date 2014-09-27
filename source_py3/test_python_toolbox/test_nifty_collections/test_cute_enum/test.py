# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `WeakKeyIdentityDict`.'''

import nose

from python_toolbox.nifty_collections import CuteEnum


def test():
    class Flavor(CuteEnum):
        CHOCOLATE = 'chocolate'
        VANILLA = 'vanilla'
        RASPBERRY = 'raspberry'
        BANANA = 'banana'
        
    assert tuple(Flavor) == (Flavor.CHOCOLATE, Flavor.VANILLA,
                             Flavor.RASPBERRY, Flavor.BANANA)
    
    assert sorted((Flavor.VANILLA, Flavor.RASPBERRY, Flavor.RASPBERRY,
                   Flavor.CHOCOLATE)) == [
        Flavor.CHOCOLATE, Flavor.VANILLA, Flavor.RASPBERRY, Flavor.RASPBERRY, 
    ]
    
    assert Flavor.VANILLA.number == 1
        
        
            
