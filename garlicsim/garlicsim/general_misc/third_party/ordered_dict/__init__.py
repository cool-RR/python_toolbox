# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `OrderedDict` class.

See its documentation for more details.

If we're using a sufficiently advanced Python version which has
`collections.OrderedDict`, we'll use that instead.
'''

import collections


if 'OrderedDict' in vars(collections):
    from collections import OrderedDict
else:
    from .ordereddict import OrderedDict

    
del collections