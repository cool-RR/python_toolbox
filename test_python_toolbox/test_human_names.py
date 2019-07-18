# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import human_names


def test():
    assert 'John' in human_names.name_list
    assert 'Janet' in human_names.name_list