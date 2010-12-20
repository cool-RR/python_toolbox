# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `OrderedDict` class.

We are **not even `try`ing** to use the `OrderedDict` that might be in the
`collections` module, because that one doesn't have a `move_to_end` method.

See its documentation for more details.
'''

from .ordereddict import OrderedDict