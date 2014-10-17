# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.sys_tools.TempSysPathAdder`.'''

import sys

from python_toolbox.sys_tools import TempSysPathAdder


def test_single():
    '''Test using `TempSysPathAdder` to add a single path.'''
    other_path = 'afdgfasgg38gjh3908ga'
    assert other_path not in sys.path
    with TempSysPathAdder(other_path):
        assert other_path in sys.path
    assert other_path not in sys.path
    
    
def test_multiple():
    '''Test using `TempSysPathAdder` to add multiple paths.'''
    other_paths = ['wf43f3_4f', 'argaer\\5g_']
    for other_path in other_paths:
        assert other_path not in sys.path
    with TempSysPathAdder(other_paths):
        for other_path in other_paths:
            assert other_path in sys.path
    for other_path in other_paths:
        assert other_path not in sys.path
    