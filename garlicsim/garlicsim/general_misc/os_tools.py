# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import subprocess
import sys
import os.path


def open_folder_in_explorer(path):
    assert os.path.isdir(path)
    if sys.platform == 'linux2':
        subprocess.check_call(['gnome-open', '--', path])
    elif sys.platform == 'darwin':
        subprocess.check_call(['open', '--', path])
    else:
        assert sys.platform == 'windows'
        subprocess.check_call(['explorer', path])