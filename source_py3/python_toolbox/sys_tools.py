# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various `sys`-related tools.'''


import sys
try:
    import pathlib
except:
    from python_toolbox.third_party import pathlib

import io

from python_toolbox.context_management import (ContextManager,
                                                    BlankContextManager)
from python_toolbox.temp_value_setting import TempValueSetter
from python_toolbox.reasoned_bool import ReasonedBool
from python_toolbox import sequence_tools


class OutputCapturer(ContextManager):
    '''
    Context manager for catching all system output generated during suite.

    Example:
    
        with OutputCapturer() as output_capturer:
            print('woo!')
            
        assert output_capturer.output == 'woo!\n'
        
    The boolean arguments `stdout` and `stderr` determine, respectively,
    whether the standard-output and the standard-error streams will be
    captured.
    '''
    def __init__(self, stdout=True, stderr=True):
        self.string_io = io.StringIO()
        
        if stdout:
            self._stdout_temp_setter = \
                TempValueSetter((sys, 'stdout'), self.string_io)
        else: # not stdout
            self._stdout_temp_setter = BlankContextManager()
            
        if stderr:
            self._stderr_temp_setter = \
                TempValueSetter((sys, 'stderr'), self.string_io)
        else: # not stderr
            self._stderr_temp_setter = BlankContextManager()
        
    def manage_context(self):
        '''Manage the `OutputCapturer`'s context.'''
        with self._stdout_temp_setter, self._stderr_temp_setter:
            yield self
        
    output = property(lambda self: self.string_io.getvalue(),
                      doc='''The string of output that was captured.''')

        
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
        self.addition = map(
            str,
            sequence_tools.to_tuple(addition,
                                    item_type=(str, pathlib.PurePath))
        )

        
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

is_pypy = ('__pypy__' in sys.builtin_module_names)

can_import_compiled_modules = \
    ReasonedBool(False, "Pypy can't import compiled "
                         "modules by default") if is_pypy else True



# May want in future:
#def execute(command):
    #with OutputCapturer() as output_capturer:
        #subprocess.Popen(command, shell=True)
    #return output_capturer.output
    