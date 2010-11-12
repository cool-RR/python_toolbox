# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import copy
import Queue
import sys
import os
import threading
import time

from garlicsim.general_misc import import_tools
from garlicsim.general_misc import string_tools

import garlicsim
from garlicsim.asynchronous_crunching import \
     BaseCruncher, CrunchingProfile, ObsoleteCruncherError


__all__ = ['PiCloudCruncher']    


class PiCloudCruncher(BaseCruncher, threading.Thread):
    
    gui_explanation = string_tools.docstring_trim(
    '''
    PiCloudCruncher:
    
     - Works by using the `cloud` module supplied by PiCloud, Inc.
     
     - Offloads the crunching into the cloud, relieving this computer of the CPU
       stress.
     
     - Requires a working internet connection and a PiCloud account. Visit
       http://picloud.com to get one.
     '''
    )
    
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("PiCloudCruncher is not implemented in this "
                                  "version! This is just a dummy class. "
                                  "PiCloudCruncher is scheduled to be "
                                  "released in GarlicSim 0.7, which will be "
                                  "available in mid-2011.")