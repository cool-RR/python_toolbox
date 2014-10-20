# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.path_tools import get_root_path_of_module

def test():
    ''' '''
    import email.charset
    assert get_root_path_of_module(email) == \
           get_root_path_of_module(email.charset)
    
    import python_toolbox.path_tools
    assert get_root_path_of_module(python_toolbox) == \
           get_root_path_of_module(python_toolbox.path_tools)
    