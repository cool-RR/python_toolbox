# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim.general_misc.import_tools.exists`.'''

import nose.tools

from garlicsim.general_misc import import_tools
from garlicsim.general_misc.import_tools import exists

def test():
    '''Test the basic workings of `exists`.'''
    assert not exists('adfgadbnv5nrn')
    assert not exists('45gse_e5b6_DFDF')
    assert not exists('VWEV65hnrt___a4')
    assert exists('email')
    assert exists('re')
    assert exists('sys')
    nose.tools.assert_raises(NotImplementedError,
                             lambda: exists('email.encoders'))