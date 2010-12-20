# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various `sys`-related tools.'''


from __future__ import with_statement

import os
import sys
import cStringIO
import subprocess

from garlicsim.general_misc.temp_value_setters import TempValueSetter


class OutputCapturer(object):
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
    
    def __enter__(self):
        self._temp_stdout_setter.__enter__()
        return self
    
    def __exit__(self, *args, **kwargs):
        self._temp_stdout_setter.__exit__(*args, **kwargs)
        self.output = self.string_io.getvalue()

        
class TempSysPathAdder(object):
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
        

# May want in future:
#def execute(command):
    #with OutputCapturer() as output_capturer:
        #subprocess.Popen(command, shell=True)
    #return output_capturer.output
    