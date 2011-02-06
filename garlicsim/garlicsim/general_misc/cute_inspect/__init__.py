# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''A fork of the standard-library `inspect` module.'''

from . import forked_inspect

getargspec = forked_inspect.getargspec
getcallargs = forked_inspect.getcallargs
getsource = forked_inspect.getsource