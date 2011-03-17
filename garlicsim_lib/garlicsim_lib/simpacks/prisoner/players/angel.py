# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Angel` player type.

See its documentation for more information.
'''

from ..player import Player


class Angel(BasePlayer):
    
    color = 'White'
    
    def play(self, round):
        return True
