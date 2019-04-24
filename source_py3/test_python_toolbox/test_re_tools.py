# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.re_tools`.'''

import re

from python_toolbox import re_tools
from python_toolbox.re_tools import searchall


def test_searchall():
    '''Test the basic workings of `searchall`.'''
    s = 'asdf df sfg s'
    result = searchall(r'(\w+)', s)
    assert len(result) == 4