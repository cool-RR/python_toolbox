from .state import State

import garlicsim


# CRUNCHERS = garlicsim.asynchronous_crunching.crunchers.ThreadCruncher

# A cruncher type that this simpack insists on using.  
# 
# This should be used only when a simpack has a special reason to use a specific
# cruncher type only.
#
# You may specify a cruncher type by string or by class. You may specify a
# sequence of cruncher types by priority, or a filter function that takes a
# cruncher type and returns whether the simpack allows using it.j



# DETERMINISM_FUNCTION = \
#     garlicsim.misc.simpack_grokker.misc.default_determinism_function

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
