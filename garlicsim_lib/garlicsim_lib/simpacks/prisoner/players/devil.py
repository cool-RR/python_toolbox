# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Devil` player type.

See its documentation for more information.
'''

from ..base_player import BasePlayer


class Devil(BasePlayer):
    '''Player which always plays mean.'''
    
    color = 'Black'
    
    def make_move(self, round):
        '''Play mean.'''
        return False