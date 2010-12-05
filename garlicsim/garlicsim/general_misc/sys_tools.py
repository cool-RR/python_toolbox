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


def execute(command):
    with OutputCapturer() as output_capturer:
        subprocess.Popen('command', shell=True)
    return output_capturer.output
    