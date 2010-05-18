from state import *

import garlicsim


# FORCE_CRUNCHER = garlicsim.asynchronous_crunching.crunchers.CruncherThread

# A cruncher that this simpack insists on using.  
# 
# This is useful because some simpacks can't be used with certain kinds of
# crunchers.



# DETERMINISM_FUNCTION = garlicsim.misc.simpack_grokker.misc.default_determinism_function

# Function that takes a step profile and says whether its deterministic.
#
# What this function says is, "If you do a simulation using this step profile,
# then you will have a deterministic simulation." (Or undeterministic, depends
# on the step profile.)
#
# This is useful because it allows garlicsim to detect if a simulation has
# reached a repititive state, so it can stop the crunching right there and avoid
# wasting resources. (05.15.2010 - Still not implemented, sorry.)
#
# Note that this function does not return True or False: It returns a
# `DeterminismSetting` class. For details about those, see documentation in
# garlicsim.misc.settings_constants.settings.
#
# The function will return None if it's unknown whether the step profile is
# deterministic.
