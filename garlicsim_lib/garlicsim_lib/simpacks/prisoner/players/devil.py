# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Devil` player type.

See its documentation for more information.
'''

from ..base_player import BasePlayer


class Devil(BasePlayer):
    
    color = 'Black'
    
    def make_move(self, round):
        return False