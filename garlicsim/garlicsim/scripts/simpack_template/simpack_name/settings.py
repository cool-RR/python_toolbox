from .state import State

import garlicsim


########### *All* of the settings in this module are optional. ################


# CRUNCHERS = garlicsim.asynchronous_crunching.crunchers.ThreadCruncher

# Cruncher types that this simpack says it can use.
#
# Cruncher types can be specified in different ways. You may specify either (a)
# a cruncher type, or (b) the string name of a cruncher type, or (c) a list of
# either of those (sorted by priority,) or (d) a filter function for cruncher
# types.
# 
# This is useful because some simpacks can't be used with certain kinds of
# crunchers.



# DETERMINISM_FUNCTION = \
#     garlicsim.misc.simpack_grokker.misc.default_determinism_function

# Function that takes a step profile and says whether its deterministic.
#
# What this function says is, "If you do a simulation using this step profile,
# then you will have a deterministic simulation." (Or undeterministic, depends
# on the step profile.)
#
# This is useful because it allows garlicsim to detect if a simulation has
# reached a repititive state, so it can stop the crunching right there and
# avoid wasting resources. (08.08.2011 - Still not implemented, sorry.)
#
# Note that this function does not return `True` or `False`: It returns a
# `DeterminismSetting` class. For details about those, see documentation in
# `garlicsim.misc.settings_constants.settings`.
#
# The function will return `None` if it's unknown whether the step profile is
# deterministic.
