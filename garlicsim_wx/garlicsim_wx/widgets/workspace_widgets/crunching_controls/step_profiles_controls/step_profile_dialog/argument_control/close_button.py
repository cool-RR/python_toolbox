# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CloseButton` class.

See its documentation for more details.
'''

import wx
import pkg_resources

from garlicsim.general_misc import caching
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_bitmap_button import \
                                                               CuteBitmapButton

from . import images as __images_package
images_package = __images_package.__name__


@caching.cache()
def get_bitmap():
    '''Get the "X" bitmap used for the close button.'''
    return wx_tools.bitmap_tools.bitmap_from_pkg_resources(
        images_package,
        'close.png'
    )


class CloseButton(CuteBitmapButton):
    '''Button for deleting a star-arg or star-kwarg.'''
    def __init__(self, parent):
        self.parent = parent
        CuteBitmapButton.__init__(
            self,
            parent,
            bitmap=get_bitmap(),
            tool_tip='Remove this argument.',
            help_text='Remove this argument.',
        )
                
            
        
