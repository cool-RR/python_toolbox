# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `temp_file_tools.TemporaryFolder`.'''

from __future__ import with_statement

import tempfile
import os.path

import nose.tools

import garlicsim

from garlicsim.general_misc.temp_file_tools import TemporaryFolder


def test_basic():
    '''Test the basic working of `TemporaryFolder`.'''
    with TemporaryFolder() as t1:
        assert str(t1) == t1.path
        assert os.path.exists(t1.path)
        assert os.path.isdir(t1.path)
        
        with TemporaryFolder() as t2:
            assert str(t2) == t2.path
            assert os.path.exists(str(t2))
            assert os.path.isdir(str(t2))
            
        assert not os.path.exists(str(t2))
        assert not os.path.isdir(str(t2))
                
        assert os.path.exists(t1.path)
        assert os.path.isdir(t1.path)
        
        file_path = os.path.join(t1.path, 'my_file')
        with open(file_path, 'w') as my_file:
            my_file.write('Woo hoo!')
        
        assert os.path.exists(file_path)
        assert os.path.isfile(file_path)
        
        with open(file_path, 'r') as my_file:
            assert my_file.read() == 'Woo hoo!'
            
    assert not os.path.exists(t1.path)
    assert not os.path.isdir(t1.path)
    
    assert not os.path.exists(file_path)
    assert not os.path.isdir(file_path)
    

