# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from garlicsim.general_misc import sequence_tools
from garlicsim_wx.widgets.general_misc.cute_control import CuteControl


class CuteTreeCtrl(wx.TreeCtrl, CuteControl):
    ''' '''
    
    def get_children_of_item(self, item, generations=1):
        if generations == 0:
            return tuple(item)
        
        (first_child, cookie) = self.GetFirstChild(item)
        children = []
        
        current_child = first_child
        while current_child.IsOk():
            children.append(current_child)
            (current_child, cookie) = self.GetNextChild(item, cookie)
        
        if generations == 1:
            return tuple(children)
        else:
            return tuple(
                sequence_tools.flatten(
                    self.get_children_of_item(
                        child,
                        generations=generations-1
                    ) for child in children
                )
            )