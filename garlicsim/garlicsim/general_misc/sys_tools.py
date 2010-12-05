import os
import sys
import cStringIO

from garlicsim.general_misc.temp_value_setters import TempValueSetter


class OutputCapturer(object):
    '''

    
    with OutputCapturer as output_capturer:
        do_stuff()
    output_capturer.final_value # <-- String containing all output
    '''
    def __init__(self):
        self.string_io = cStringIO.StringIO()
        self._temp_stdout_setter = \
            TempValueSetter((sys, 'stdout'), self.string_io)
        self.final_value = None
    
    def __enter__(self):
        self._temp_stdout_setter.__enter__()
        return self
    
    def __exit__(self, *args, **kwargs):
        self._temp_stdout_setter.__exit__(*args, **kwargs)
        self.final_value = self.string_io.getvalue()


def execute(command):
    with OutputCapturer() as output_capturer:
        os.system(command) # Throwing away the exit status
    return output_capturer.final_value
    