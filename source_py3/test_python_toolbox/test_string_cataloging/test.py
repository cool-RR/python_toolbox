# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import string_cataloging


def test():
    x = string_cataloging.string_to_integer('ein')
    y = string_cataloging.string_to_integer('zwei')
    z = string_cataloging.string_to_integer('drei')
    
    assert string_cataloging.integer_to_string(x) == 'ein'
    assert string_cataloging.integer_to_string(y) == 'zwei'
    assert string_cataloging.integer_to_string(z) == 'drei'
    
    assert {string_cataloging.string_to_integer('zwei') for i in range(10)} \
                                                                         == {y}