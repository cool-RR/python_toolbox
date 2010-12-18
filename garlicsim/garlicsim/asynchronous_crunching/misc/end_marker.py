# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `EndMarker` class.

See its documentation for more info.
'''


class EndMarker(object):
    '''
    A marker used by crunchers to say that the simulation reached its end.
    
    This is used only in endable simulations. When the step function raises a
    `WorldEnded` exception, signifying that the simulation has ended, the
    cruncher will place an `EndMarker` in the work queue. (Where otherwise
    states will be placed.)
    
    The crunching manager will recognize the `EndMarker` and put an `End` to 
    the timeline.
    '''
    # todo: should allow putting a message, given by the `WorldEnded`, that 
    # will be attached to the `End`.
