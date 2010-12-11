# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This package provides a list of human names as `name_list`.'''

import pkg_resources

__all__ = ['name_list']

(male_raw, female_raw) = \
    [
        pkg_resources.resource_string(__name__, file_name) for 
        file_name in ['male.txt', 'female.txt']
    ]

del file_name

name_list = male_raw.split(':') + female_raw.split(':')
