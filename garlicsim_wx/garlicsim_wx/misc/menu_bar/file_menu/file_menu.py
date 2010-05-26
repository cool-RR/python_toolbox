# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the FileMenu class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu

from export_menu import ExportMenu


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
        frame.Bind(wx.EVT_MENU, frame.on_new, self.new_button)
        

        self.open_button = self.Append(
            wx.ID_OPEN,
            '&Open...\tCtrl+O',
            ' Open a saved simulation'
        )
        frame.Bind(wx.EVT_MENU, frame.on_open, self.open_button)        
        
        
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
        frame.Bind(wx.EVT_MENU, frame.on_save, self.save_button)
        
        
        self.save_as_button = self.Append(
            wx.ID_SAVEAS,
            'Save &as...\tShift+Ctrl+S',
            ' Save the currently open simulation under a different name'
        )
        self.save_as_button.Enable(False)
                
        
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
            'Print...\tCtrl+P',
            ' Print the current state of the simulation'
        )
        self.print_button.Enable(False)
        
        
        self.AppendSeparator()
        

        self.exit_button = self.Append(
            wx.ID_EXIT,
            'E&xit',
            ' Close GarlicSim')              
        
        frame.Bind(wx.EVT_MENU, frame.on_exit_menu_button, self.exit_button)