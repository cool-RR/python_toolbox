# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import wx

from python_toolbox.misc_tools import ProxyProperty

from python_toolbox import sequence_tools
from python_toolbox.wx_tools.widgets.cute_control import CuteControl


class CuteTreeCtrl(wx.TreeCtrl, CuteControl):
    ''' '''

    def get_children_of_item(self, item, generations=1):
        '''
        Get all the child items of `item`.

        If `generations` is `1`, the children will be returned; if it's `2`,
        the grand-children will be returned, etc.
        '''
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

    OnCompareItems = ProxyProperty(
        '_compare_items',
        doc='''Hook for comparing items in the tree, used for sorting.'''
    )