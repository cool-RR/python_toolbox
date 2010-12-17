# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `PiCloudCruncher` class, which is merely a placeholder.

See its documentation for more information.

The real `PiCloudCruncher` will probably be released in GarlicSim 0.7 in
mid-2011.
'''

from garlicsim.general_misc import string_tools
from garlicsim.general_misc.reasoned_bool import ReasonedBool

import garlicsim
from garlicsim.asynchronous_crunching import BaseCruncher


apology = ('PiCloudCruncher is not implemented in this version! This is just '
           'a placeholder. PiCloudCruncher is scheduled to be released in '
           'GarlicSim 0.7, which will be available in mid-2011.')


class PiCloudCruncher(BaseCruncher):
    '''
    Placeholder for the real `PiCloudCruncher`, which could crunch on PiCloud.
    
    The real `PiCloudCruncher` will probably be released in GarlicSim 0.7 in
    mid-2011.
    
    `PiCloudCruncher` will be able to crunch the simulation on the cloud using
    PiCloud, a proprietary cloud solution. Visit http://picloud.com for more
    details.
    
    This will relieve the user's computer from crunching the simulation,
    allowing parallel computation of many tree forks.
    
    Using `PiCloudCruncher` will require an internet connection and a paid
    PiCloud account. (It's really cheap though.)
    '''
    
    gui_explanation = string_tools.docstring_trim(
    '''
    `PiCloudCruncher`:
    
     - Works by using the `cloud` module supplied by PiCloud, Inc.
     
     - Offloads the crunching into the cloud, relieving this computer of the CPU
       stress.
       
     - Requires a working internet connection and a PiCloud account. Visit
       http://picloud.com to get one.
       
     - Costs money, charged by the millisecond. It's really cheap though. See
       the PiCloud website for pricing details.
    ''')
    
    
    
    @staticmethod
    def can_be_used_with_simpack_grokker(simpack_grokker):
        '''
        Return whether `PiCloudCruncher` can be used with a simpack grokker.
        
        Since this class is just a placeholder, the answer is invariably
        `False`.
        '''
        return ReasonedBool(
            False,
            apology
        )
    
    
    def __init__(self, *args, **kwargs):
        raise NotImplementedError(apology)