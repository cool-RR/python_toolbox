# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `temp_file_tools.TemporaryFolder`.'''

import tempfile
import os.path

import nose.tools

import python_toolbox

from python_toolbox.temp_file_tools import TemporaryFolder


def test_basic():
    '''Test the basic working of `TemporaryFolder`.'''
    with TemporaryFolder() as tf1path:
        assert isinstance(tf1path, str)
        assert os.path.exists(tf1path)
        assert os.path.isdir(tf1path)
        
        tf2 = TemporaryFolder()
        with tf2 as tf2path:
            assert str(tf2) == tf2.path == tf2path
            assert os.path.exists(str(tf2))
            assert os.path.isdir(str(tf2))
            
        assert not os.path.exists(str(tf2))
        assert not os.path.isdir(tf2path)
                
        assert os.path.exists(tf1path)
        assert os.path.isdir(tf1path)
        
        file_path = os.path.join(tf1path, 'my_file')
        with open(file_path, 'w') as my_file:
            my_file.write('Woo hoo!')
        
        assert os.path.exists(file_path)
        assert os.path.isfile(file_path)
        
        with open(file_path, 'r') as my_file:
            assert my_file.read() == 'Woo hoo!'
            
    assert not os.path.exists(tf1path)
    assert not os.path.isdir(tf1path)
    
    assert not os.path.exists(file_path)
    assert not os.path.isdir(file_path)
    

