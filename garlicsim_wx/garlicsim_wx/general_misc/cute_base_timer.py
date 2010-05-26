# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the CuteBaseTimer class.

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
            while ancestor is not None:
                if ancestor == frame:
                    timer.Stop()
                    break
                ancestor = ancestor.GetParent()
    