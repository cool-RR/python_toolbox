# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''A collection of simulation packages to be used with garlicsim.'''

import sys

import garlicsim.general_misc.version_info

import garlicsim


__version_info__ = garlicsim.general_misc.version_info.VersionInfo(0, 6, 2)
__version__ = '0.6.2'


if sys.version_info[0] >= 3:
    raise Exception('This package is not compatible with Python 3.x. Use '
                    '`garlicsim_lib_py3` instead.')
if sys.version_info[1] <= 4:
    raise Exception('This package requires Python 2.5 and upwards. (Not '
                    'including 3.x).')