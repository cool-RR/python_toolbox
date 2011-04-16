# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import imp

from garlicsim.general_misc import address_tools


def find_module(name, path=None):
    if '.' in name:
        if path:
            raise NotImplemented
        parent_name, child_name = name.rsplit('.', 1)
        parent = address_tools.resolve(parent_name)
        return imp.find_module(child_name, parent.__path__)
    else:
        return find_module(name, path)
        
