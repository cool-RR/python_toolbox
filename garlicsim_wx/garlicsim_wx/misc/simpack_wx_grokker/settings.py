# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Settings` class.

See its documentation for more info.
'''

import garlicsim_wx

class Settings(object):
    '''A set of settings for a simpack_wx.'''
    #todo: subclass from a pretty vars-shower
    def __init__(self):
        
        self.BIG_WORKSPACE_WIDGETS = []
        '''Widgets to show in the middle of the frame.'''
        
        self.SMALL_WORKSPACE_WIDGETS = []
        '''Small widgets to show.'''
        
        self.SEEK_BAR_GRAPHS = []
        '''
        List of scalar functions to be shown as graphs in the seek bar.
        
        These may be either scalar state functions or scalar history functions.
        '''
        
        self.STATE_CREATION_FUNCTION = garlicsim_wx.widgets.misc.\
            DefaultStateCreationDialog.create_show_modal_and_get_state
        '''
        Function for creating a new state. Takes the main GarlicSim `Frame`.
        '''
