# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_control import CuteControl


class CuteTreeCtrl(wx.TreeCtrl, CuteControl):
    ''' '''
    
    def get_children_of_item(self, item):
        (first_child, cookie) = self.GetFirstChild(item)
        children = []
        
        current_child = first_child
        while current_child.IsOk():
            children.append(current_child)
            (current_child, cookie) = self.GetNextChild(item, cookie)
        
        return tuple(children)