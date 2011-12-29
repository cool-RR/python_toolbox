# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Provides a list of human names as `name_list`.'''

from . import _name_list

name_list = _name_list.data.split('\n')
