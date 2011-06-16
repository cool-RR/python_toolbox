# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `FileMenu` class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu

from .export_menu import ExportMenu


class FileMenu(CuteMenu):
    '''Menu for file actions: New, open, save...'''
    def __init__(self, frame):
        super(FileMenu, self).__init__()
        self.frame = frame
        self._build()
    
    def _build(self):
        
        frame = self.frame

        
        self.new_button = self.Append(
            wx.ID_NEW, 
            '&New...\tCtrl+N',
            ' Create a new simulation'
        )
        frame.Bind(wx.EVT_MENU, lambda event: frame.create_new_gui_project(),
                   self.new_button)
        

        self.open_button = self.Append(
            wx.ID_OPEN,
            '&Open...\tCtrl+O',
            ' Open a saved simulation'
        )
        frame.Bind(wx.EVT_MENU, lambda event: frame.open_gui_project(),
                   self.open_button)        
        
        
        # todo: put open recent here

        
        self.AppendSeparator()

        
        self.close_button = self.Append(
            wx.ID_CLOSE,
            '&Close\tCtrl+W',
            ' Close the currently open simulation'
        )
        self.close_button.Enable(False)

        
        self.save_button = self.Append(
            wx.ID_SAVE,
            '&Save\tCtrl+S',
            ' Save the currently open simulation'
        )
        frame.Bind(wx.EVT_MENU, lambda event: frame.save_gui_project(),
                   self.save_button)
        
        
        self.save_as_button = self.Append(
            wx.ID_SAVEAS,
            'Save &as...\tShift+Ctrl+S',
            ' Save the currently open simulation under a different name'
        )
        self.save_as_button.Enable(False)
                
        
        self.AppendSeparator()
        
        
        self.new_simpack_button = self.Append(
            -1,
            'New simpack...',
            ' Create a new simulation package'
        )
        self.new_simpack_button.Enable(False)
                
        
        self.AppendSeparator()

        
        self.export_menu = ExportMenu(frame)
        self.export_menu_button = self.AppendMenu(
            -1,
            '&Export',
            self.export_menu,
            ' Export simulation data'
        )
        self.export_menu_button.Enable(False)
        
        
        self.AppendSeparator()
        
        
        self.print_button = self.Append(
            wx.ID_PRINT,
            '&Print...\tCtrl+P',
            ' Print the current state of the simulation'
        )
        self.print_button.Enable(False)
        
        
        self.AppendSeparator()
        

        self.exit_button = self.Append(
            wx.ID_EXIT,
            'E&xit',
            ' Close GarlicSim')              
        
        frame.Bind(wx.EVT_MENU, lambda event: frame.exit(), self.exit_button)

        
    def _recalculate(self):
        self.save_button.Enable(
            bool(self.frame.gui_project)
        )