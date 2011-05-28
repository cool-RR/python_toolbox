# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `NotMainProgramWarningDialog` class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_message_dialog \
                                                       import CuteMessageDialog


class NotMainProgramWarningDialog(CuteMessageDialog): 
    '''
    Dialog warning that `garlicsim_wx` is not the main program.
    
    This is something that can cause problems in several operations, like
    load/save, so we warn the user about it.
    '''
    
    def __init__(self, frame):
   
        content = (
            "GarlicSim has detected that it's not being run as the main "
            "program. (Perhaps you have imported it from another script?)\n"
            "\n"
            "If this is the case, it will probably not succeed in starting "
            "another instance of GarlicSim, which is needed for the action "
            "you just tried to do. It can try to continue, but it might not "
            "work. If you want to be safe from this problem, run GarlicSim by "
            "itself, not importing it from another script.\n"
            "\n"
            "Do you want to try to continue?"
        )
        
        CuteMessageDialog.__init__(
            self,
            frame,
            content,
            caption='Warning',
            style=(wx.YES_NO | wx.ICON_EXCLAMATION)
        )
        
        