# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Python Toolbox is a collection of Python tools.

These tools include caching, context manager tools, data structures, binary
search, import tools, tools for manipulating Python's built-in types, and many
more.

Visit http://pypi.python.org/pypi/python_toolbox/ for more info.
'''

import python_toolbox._bootstrap
import python_toolbox.version_info
import python_toolbox.monkeypatch_copyreg
import python_toolbox.monkeypatch_envelopes

__version_info__ = python_toolbox.version_info.VersionInfo(0, 9, 2)
__version__ = __version_info__.version_text

