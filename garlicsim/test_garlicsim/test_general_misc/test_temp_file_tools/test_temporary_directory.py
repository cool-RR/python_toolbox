# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''

'''

from __future__ import with_statement

import tempfile
import os.path

import nose.tools

import garlicsim

from garlicsim.general_misc.temp_file_tools import TemporaryDirectory


def test_basic():
    
    with TemporaryDirectory() as t1:
        assert str(t1) == t1.path
        assert os.path.exists(t1.path)
        assert os.path.isdir(t1.path)
        
        with TemporaryDirectory() as t2:
            assert str(t2) == t2.path
            assert os.path.exists(str(t2))
            assert os.path.isdir(str(t2))
            
            
        assert not os.path.exists(t2.path)
        assert not os.path.isdir(t2.path)

