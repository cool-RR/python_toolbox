# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various `sys`-related tools.'''


from __future__ import with_statement

import os
import sys
import cStringIO
import subprocess

from garlicsim.general_misc.context_manager import ContextManager
from garlicsim.general_misc.temp_value_setters import TempValueSetter


class OutputCapturer(ContextManager):
    '''
    Context manager for catching all system output generated during suite.

    Example:
    
        with OutputCapturer() as output_capturer:
            print('woo!')
            
        assert output_capturer.output == 'woo!\n'
        
    '''
    def __init__(self):
        self.string_io = cStringIO.StringIO()
        self._temp_stdout_setter = \
            TempValueSetter((sys, 'stdout'), self.string_io)
        self.output = None
        
    def manage_context(self):
        '''Manage the `OutputCapturer`'s context.'''
        with self._temp_stdout_setter:
            yield self
        self.output = self.string_io.getvalue()

        
class TempSysPathAdder(ContextManager):
    '''
    Context manager for temporarily adding paths to `sys.path`.
    
    Removes the path(s) after suite.
    
    Example:
    
        with TempSysPathAdder('path/to/fubar/package'):
            import fubar
            fubar.do_stuff()
            
    '''
    def __init__(self, addition):
        '''
        Construct the `TempSysPathAdder`.
        
        `addition` may be a path or a sequence of paths.
        '''
        if isinstance(addition, basestring):
            addition = [addition]
        for entry in addition:
            assert isinstance(entry, basestring)
        self.addition = addition

        
    def __enter__(self):
        self.entries_not_in_sys_path = [entry for entry in self.addition if
                                        entry not in sys.path]
        sys.path += self.entries_not_in_sys_path
        return self
    

    def __exit__(self, *args, **kwargs):
        
        for entry in self.entries_not_in_sys_path:
            
            # We don't allow anyone to remove it except for us:
            assert entry in sys.path 
            
            sys.path.remove(entry)

            
frozen = getattr(sys, 'frozen', None)
'''
The "frozen string", if we are frozen, otherwise `None`.

This is useful for checking if we are frozen, e.g. with py2exe.
'''


# May want in future:
#def execute(command):
    #with OutputCapturer() as output_capturer:
        #subprocess.Popen(command, shell=True)
    #return output_capturer.output
    