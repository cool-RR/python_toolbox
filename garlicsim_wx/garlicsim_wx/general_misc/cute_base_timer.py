# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CuteBaseTimer` class.

See its documentation for more information.
'''

class CuteBaseTimer(object):
    '''A base class for timers, allowing easy central stopping.'''    
    __timers = [] # todo: change to weakref list
    
    def __init__(self, parent):
        self.__parent = parent
        CuteBaseTimer.__timers.append(self)
        
        
    @staticmethod # should be classmethod?
    def stop_timers_by_frame(frame):
        '''Stop all the timers that are associated with the given frame.'''
        for timer in CuteBaseTimer.__timers:
            ancestor = timer.__parent
            while ancestor:
                if ancestor == frame:
                    timer.Stop()
                    break
                ancestor = ancestor.GetParent()
    