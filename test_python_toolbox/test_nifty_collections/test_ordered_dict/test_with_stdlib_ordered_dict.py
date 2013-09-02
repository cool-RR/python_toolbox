# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import sys

from python_toolbox import cute_testing

from python_toolbox.nifty_collections.ordered_dict import OrderedDict


def test():
    if sys.version_info[:2] <= (2, 6):
        raise nose.SkipTest
    
    ordered_dict = OrderedDict(((1, 'a'), (2, 'b'), (3, 'c')))
    raise NotImplementedError