# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines various player types, i.e. different strategies for playing.

They are all subclasses of `Player`.
'''

from .angel import Angel
from .devil import Devil
from .tit_for_tat import TitForTat


player_types_list = [Angel, Devil, TitForTat]