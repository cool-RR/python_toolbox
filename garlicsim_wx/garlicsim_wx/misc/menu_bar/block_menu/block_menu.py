# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the BlockMenu class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu

class BlockMenu(CuteMenu):
    '''A menu for manipulating the active block.'''
    def __init__(self, frame):
        super(BlockMenu, self).__init__()
        self.frame = frame
        self._build()
    
    def _build(self):
        
        frame = self.frame
        
       
        self.split_button = self.Append(
            -1,
            '&Split active block...',
            " Split the active block into two separate blocks"
        )
        self.split_button.Enable(False)
        
        
        self.scatter_button = self.Append( # todo: rename
            -1,
            'S&catter active block...',
            ' Scatter the active block, leaving all its nodes blockless'
        )
        self.scatter_button.Enable(False)
        
        