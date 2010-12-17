from __future__ import with_statement

import os
import sys
import cStringIO
import subprocess

from garlicsim.general_misc.temp_value_setters import TempValueSetter


class OutputCapturer(object):
    '''

    
    with OutputCapturer as output_capturer:
        do_stuff()
    output_capturer.output # <-- String containing all output
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

    def __init__(self, addition):
        if isinstance(addition, basestring):
            addition = [addition]
        for entry in addition:
            assert isinstance(entry, basestring)
        self.addition = addition
        
        #self.string_io = cStringIO.StringIO()
        #self._temp_stdout_setter = \
            #TempValueSetter((sys, 'stdout'), self.string_io)
        #self.output = None

        
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
        

#def execute(command):
    #with OutputCapturer() as output_capturer:
        #subprocess.Popen(command, shell=True)
    #return output_capturer.output
    