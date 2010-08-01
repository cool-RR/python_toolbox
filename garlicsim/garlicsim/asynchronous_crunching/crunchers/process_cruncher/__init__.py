# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the ProcessCruncher class.

See its documentation for more information.

This module requires the multiprocessing package to be installed. It is part of
the standard library for Python 2.6 and above, but not for earlier versions. A
backport of it for Python 2.5 is available at
http://pypi.python.org/pypi/multiprocessing.
'''

from garlicsim.general_misc import import_tools

multiprocessing = import_tools.import_if_exists('multiprocessing', silent_fail=True)
if not multiprocessing:
    raise ImportError('The backported multiprocessing package is '
                      'needed. Please download it from '
                      'http://pypi.python.org/pypi/multiprocessing and '
                      'install it.')


from .process_cruncher import ProcessCruncher
