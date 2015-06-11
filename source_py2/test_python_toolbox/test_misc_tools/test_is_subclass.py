# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.misc_tools import is_subclass


def test():
    assert is_subclass(object, object)
    assert is_subclass(object, (object, str))
    assert not is_subclass(object, str)
    
    assert not is_subclass(7, object)
    assert not is_subclass('meow', object)
