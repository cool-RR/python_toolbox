# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Angel` player type.

See its documentation for more information.
'''

from ..base_player import BasePlayer


class Angel(BasePlayer):
    '''Player which always plays nice.'''
    
    color = 'White'
    
    def make_move(self, round):
        '''Play nice.'''
        return True
