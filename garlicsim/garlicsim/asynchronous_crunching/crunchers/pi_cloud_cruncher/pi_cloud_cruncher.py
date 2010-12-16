# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import copy
import Queue
import sys
import os
import threading
import time

from garlicsim.general_misc import import_tools
from garlicsim.general_misc import string_tools
from garlicsim.general_misc.reasoned_bool import ReasonedBool

import garlicsim
from garlicsim.asynchronous_crunching import \
     BaseCruncher, CrunchingProfile, ObsoleteCruncherError


__all__ = ['PiCloudCruncher']    


apology = ("PiCloudCruncher is not implemented in this version! This is just "
           "a placeholder. PiCloudCruncher is scheduled to be released in "
           "GarlicSim 0.7, which will be available in mid-2011.")


class PiCloudCruncher(BaseCruncher, threading.Thread):
    
    gui_explanation = string_tools.docstring_trim(
    '''
    PiCloudCruncher:
    
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
        return ReasonedBool(
            False,
            apology
        )
    
    def __init__(self, *args, **kwargs):
        raise NotImplementedError(apology)