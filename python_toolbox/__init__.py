# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''
Python Toolbox is a collection of Python tools.

These tools include caching, context manager tools, data structures, binary
search, import tools, tools for manipulating Python's built-in types, and many
more.

Visit http://pypi.python.org/pypi/python_toolbox/ for more info.
'''

import python_toolbox.version_info

__version__ = '1.0.11'
__version_info__ = python_toolbox.version_info.VersionInfo(
    *(map(int, __version__.split('.')))
)
