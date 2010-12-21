# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Testing module for `garlicsim.general_misc.re_tools`.
'''

import re

from garlicsim.general_misc import re_tools
from garlicsim.general_misc.re_tools import searchall


def test_searchall():
    '''Test the basic workings of `searchall`.'''
    s = 'asdf df sfg s'
    result = searchall('(\w+)', s)
    assert len(result) == 4