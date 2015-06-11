# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.misc_tools import is_magic_variable_name


def test():
    magic_variable_names = ('__init__', '__iter__', '__subclasscheck__')
    non_magic_variable_names = ('sup_yo', '__nope!__', )
    for magic_variable_name in magic_variable_names:
        assert is_magic_variable_name(magic_variable_name)
    for non_magic_variable_name in non_magic_variable_names:
        assert not is_magic_variable_name(non_magic_variable_name)
