# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `WeakKeyIdentityDict`.'''

import nose

from python_toolbox.nifty_collections import WeakKeyDefaultDict
from python_toolbox import gc_tools


class WeakreffableObject(object):
    ''' '''
        

def test():
    '''Test the basic workings of `WeakKeyDefaultDict`.'''
    wkd_dict = WeakKeyDefaultDict(default_factory=lambda: 7)

    weakreffable_object_0 = WeakreffableObject()
    weakreffable_object_1 = WeakreffableObject()
    weakreffable_object_2 = WeakreffableObject()
    weakreffable_object_3 = WeakreffableObject()
    
    wkd_dict[weakreffable_object_0] = 2
    assert wkd_dict[weakreffable_object_0] == 2
    assert wkd_dict[weakreffable_object_1] == 7
    assert wkd_dict[weakreffable_object_2] == 7
    
    weakreffable_object_3 = WeakreffableObject()
    wkd_dict[weakreffable_object_3] = 123
    assert len(wkd_dict.keys()) == 4
    del weakreffable_object_3
    gc_tools.collect()
    assert len(wkd_dict.keys()) == 3