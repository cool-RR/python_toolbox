# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
Package for bootstrapping `python_toolbox` when frozen by py2exe.

This runs a bundled version of Python's `site` module, which adds things like
`help` to `__builtins__`. This is useful because py2exe has problems with
packaging the standard `site` module.

The `python26_site` module in this package is simply the `site` module from
Python 2.6's standard library; if you want to package `python_toolbox` with
py2exe for a different version of Python, this package will need to be expanded
with that version's `site` module.
'''

import sys

frozen = getattr(sys, 'frozen', None)

if frozen:
    if sys.version_info[:2] != (2, 6):
        raise NotImplementedError('For Python versions other than 2.6, this '
                                  'package needs to be expanded to have a ' 
                                  'copy of their `site` module. ')
    assert 'site' not in sys.modules
    from . import python26_site
    