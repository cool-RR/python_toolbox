# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Various os-related tools.'''

import subprocess
import sys
import os.path


def start_file(path):
    '''Open a file by launching the program that handles its kind.'''
    path = pathlib.Path(path)
    assert path.exists()
    
    if sys.platform.startswith('linux'): # Linux:
        subprocess.check_call(['xdg-open', str(path)])
        
    elif sys.platform == 'darwin': # Mac:
        subprocess.check_call(['open', '--', str(path)])
        
    elif sys.platform in ('win32', 'cygwin'): # Windows:
        os.startfile(path)
        
    else:
        raise NotImplementedError(
            "Your operating system `%s` isn't supported by "
            "`start_file`." % sys.platform)    
    
    
