# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `App` class.

See its documentation for more information.
'''

import functools
import sys

import wx

from garlicsim.general_misc import import_tools

import garlicsim_wx


class App(wx.PySimpleApp):
    '''
    A `garlicsim_wx` application.
    
    The `App` is responsible for spawning a `Frame`.
    '''
    # todo: need to think if i allow frames with no app. on one hand good idea,
    # to allow people to start a garlicsim_wx frame in their own app. on other
    # hand frames will need to know how to start another frame.
    def __init__(self, new_gui_project_simpack_name=None,
                 load_gui_project_file_path=None):
        '''
        Constructor.
        
        In order to start a new simulation on startup, pass the name of the
        simpack as `new_gui_project_simpack_name`.
        
        In order to load a simulation from file on startup, pass the path to
        the file as `load_gui_project_file_path`.
        
        (At most one of these can be done.)
        '''
        self.frame = None
        assert not (new_gui_project_simpack_name and
                    load_gui_project_file_path)
        self.new_gui_project_simpack_name = new_gui_project_simpack_name
        self.load_gui_project_file_path = load_gui_project_file_path
        super(App, self).__init__()
        
        if '--wx-debug=on' not in sys.argv:
            self.SetAssertMode(wx.PYAPP_ASSERT_SUPPRESS)
        
    
    def OnInit(self):
        
        frame = garlicsim_wx.Frame(
            parent=None,
            title='GarlicSim',
            size=(1140, 850)
        )
        
        self.frame = frame
        
        self.SetTopWindow(frame)
        
        self.simple_help_provider = wx.SimpleHelpProvider()
        wx.HelpProvider_Set(self.simple_help_provider)
        
        if self.new_gui_project_simpack_name is not None:
            simpack = \
                import_tools.normal_import(self.new_gui_project_simpack_name)
            
            wx.CallAfter(
                functools.partial(
                    self.frame._new_gui_project_from_simpack,
                    simpack
                )
            )
            
        if self.load_gui_project_file_path is not None:
            
            wx.CallAfter(
                functools.partial(
                    self.frame._open_gui_project_from_path,
                    self.load_gui_project_file_path
                )
            )
            
        return True
    