# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim_lib`.'''


def test_import():
    '''
    Test that `garlicsim_lib` can be imported.
    
    This is mostly a dummy test used for testing the test mechanism itself.
    '''
    import garlicsim_lib
    
    import garlicsim_lib.simpacks
    assert 'simpacks' in vars(garlicsim_lib)
    assert garlicsim_lib.simpacks.__name__ == 'garlicsim_lib.simpacks'
    
    