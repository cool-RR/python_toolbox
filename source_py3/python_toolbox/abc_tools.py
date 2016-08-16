# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines tools related to abstract base classes from the `abc` module.'''

import abc


def abstract_whatever(_=None):
    return abc.abstractmethod(lambda: None)
    