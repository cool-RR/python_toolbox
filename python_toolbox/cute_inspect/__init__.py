# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.

'''A fork of the standard-library `inspect` module.'''

from . import forked_inspect

getargspec = forked_inspect.getargspec
getcallargs = forked_inspect.getcallargs
getsource = forked_inspect.getsource