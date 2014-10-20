# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Provides a list of human names as `name_list`.'''

from . import _name_list

name_list = _name_list.data.split('\n')
