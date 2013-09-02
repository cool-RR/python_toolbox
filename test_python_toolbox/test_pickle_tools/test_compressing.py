# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

# We're importing `pickle_module` from `pickle_tools`, so we get the exact same
# pickle module it's using. (Giving it the freedom to change between `cPickle`
# and `pickle`.)
from python_toolbox.pickle_tools import pickle_module

import nose

from python_toolbox import import_tools

from python_toolbox import pickle_tools
    

my_messy_object = (
    'Whatever',
    {1: 2,}, 
    set([3, 4]), 
    frozenset([3, 4]),
    ((((((((((((())))))))))))),
    u'unicode_too',
    (((((3, 4, 5j)))))
)

def test():
    pickled_and_compressed = pickle_tools.pickle_and_compress(my_messy_object)
    assert pickle_tools.decompress_and_unpickle(pickled_and_compressed) == \
                                                                my_messy_object