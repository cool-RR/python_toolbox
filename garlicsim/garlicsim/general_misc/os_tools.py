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
    if os.name == 'posix':
        subprocess.check_call(['xdg-open', '--', path])
    elif os.name == 'mac':
        subprocess.check_call(['open', '--', path])
    else:
        assert os.name == 'nt'
        os.startfile(path)