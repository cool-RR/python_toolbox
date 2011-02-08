# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim_wx`.'''


def test_import():
    '''
    Test that `garlicsim_wx` can be imported.
    
    This is mostly a dummy test used for testing the test mechanism itself.
    '''
    import garlicsim_wx
    
    assert 'widgets' in vars(garlicsim_wx)
    assert garlicsim_wx.widgets.__name__ == 'garlicsim_wx.widgets'
    
    