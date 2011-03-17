# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Devil` player type.

See its documentation for more information.
'''


class Devil(Player):
    def play(self, round):
        return False