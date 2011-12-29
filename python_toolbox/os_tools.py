# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import subprocess
import sys
import os.path


def start_file(path):
    assert os.path.exists(path)
    
    if sys.platform.startswith('linux'): # Linux:
        subprocess.check_call(['xdg-open', path])
        
    elif sys.platform == 'darwin': # Mac:
        subprocess.check_call(['open', '--', path])
        
    elif sys.platform in ('win32', 'cygwin'): # Windows:
        os.startfile(path)
        
    else:
        raise NotImplementedError(
            "Your operating system `%s` isn't supported by "
            "`start_file`." % sys.platform)