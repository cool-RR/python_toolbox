# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `Shell` class.

See its documentation for more info.
'''

from __future__ import with_statement

import sys
import pprint

import wx.py.shell

from garlicsim.general_misc import temp_value_setters

from garlicsim_wx.widgets import WorkspaceWidget
import garlicsim
import garlicsim_wx


def display_hook(thing):
    '''
    Print a representation of an object.
    
    This uses `pprint` rather than the default Python display hook which uses
    `print`. This is used as a temporary display hook when working in the shell
    so that the shell will pretty-print all objects.
    '''
    if thing is not None:
        try:
            import __builtin__
            __builtin__._ = thing
        except ImportError:
            __builtins__._ = thing
        pprint.pprint(thing)


class TempDisplayHookSetter(temp_value_setters.TempValueSetter):
    '''
    Temporarily sets the system's display hook to be our pretty-printing one.
    '''
    def __init__(self):
        temp_value_setters.TempValueSetter.__init__(
            self,
            (sys, 'displayhook'),
            display_hook
        )
        

class Shell(wx.py.shell.Shell, WorkspaceWidget):
    '''
    A shell widget, allowing to execute arbitrary Python code.
    
    This is useful for examining the simulation.
    '''
    # todo: After every command in shell, must make the top emitter emit
    def __init__(self, frame):
        wx.py.shell.Shell.__init__(self, frame, size=(100, 100),
                                   locals=frame.gui_project.namespace,
                                   style=wx.SUNKEN_BORDER)
        WorkspaceWidget.__init__(self, frame)
        
        # We used to import `site` here to get `help` and others when frozen,
        # but now `garlicsim` has `bootstrap_py2exe` which bundles its own
        # version of `site` which creates `help` and a few other builtins.
        import __builtin__
        assert 'help' in __builtin__.__dict__
        del __builtin__
        
    
    def setLocalShell(self):
        # Making it a no-op to avoid reference to retarded `ShellFacade`.
        pass
    
    
    def push(self, command, silent=False):
        '''
        Send command to the interpreter for execution.
        
        If the command evaluates to some Python object, it will be
        pretty-printed in the shell.
        '''
        with TempDisplayHookSetter():
            return wx.py.shell.Shell.push(self, command, silent=silent)