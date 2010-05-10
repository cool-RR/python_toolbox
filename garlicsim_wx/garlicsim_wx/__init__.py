# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
A wxPython-based GUI for garlicsim.

The final goal of this project is to become a fully-fledged application for
working with simulations, friendly enough that it may be used by
non-programmers.

This program is intended for Python versions 2.5 and 2.6.
'''



import bootstrap

import sys
import os.path

import wx

import misc
from frame import Frame
from gui_project import GuiProject
from app import App

__all__ = ['Frame', 'GuiProject', 'start']

__version__ = '0.4'

def start():
    '''Start the GUI.'''
    
    args = sys.argv[:]
    # todo: Consider removing the args we can understand from sys.argv, so
    # program inside will not be confused by them.
    
    # If we're not frozen, the first argument is the path of the script, and
    # that should be cut off:
    if not hasattr(sys, 'frozen'):
        del args[:1]
        
    new_gui_project_simpack_name = None
    load_gui_project_file_path = None
    
    if args:
        arg = args[0]        
        if arg.startswith('__garlicsim_wx_new='):
            new_gui_project_simpack_name = arg[19:]
        elif os.path.isfile(arg):
            load_gui_project_file_path = arg
    
    app = App(new_gui_project_simpack_name=new_gui_project_simpack_name,
              load_gui_project_file_path=load_gui_project_file_path)
    
    app.MainLoop()
    
    
if __name__ == "__main__":
    
    start()