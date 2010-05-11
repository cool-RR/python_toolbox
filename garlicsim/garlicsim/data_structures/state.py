# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A module that defines the State class.

See its documentation for more info.
'''

from garlicsim.general_misc import misc_tools

class State(object):
    '''
    A state describes a world state in the world of the simulation.
    
    It contains information about a "frozen moment" in the simulation.

    All the information about the state of the simulation should be saved in
    attributes of the state object.

    When a state is created, a `.clock` attribute must be assigned to it,
    specifying what time it is in this state.

    A state object must always be picklable, as do all the attributes assigned
    to it.
    '''
    
    def __init__(self):
        self.end_result = None
        
    def calculate_end_result(self):
        return
    
    def __repr__(self): # todo: show end_result here
        '''
        Get a string representation of the state.
        
        Example output:
        <garlicsim.data_structures.State with clock 32.3 at 0x1c822d0>
        ''' 
        return '<%s %sat %s>' % \
               (
                   misc_tools.shorten_class_address(
                       self.__class__.__module__,
                       self.__class__.__name__
                       ),
                   'with clock %s ' % self.clock if hasattr(self, 'clock') \
                                      else '',
                   hex(id(self))
               )
        
