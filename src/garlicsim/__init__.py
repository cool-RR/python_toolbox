"""
GarlicSim is a platform for writing, running and analyzing simulations. It can
handle any kind of simulation: Physics, game theory, epidemic spread,
electronics, etc.

Visit http://garlicsim.com for more info.

todo: fix documentation everywhere to reflect that `touched` is now a node
attribute.
"""

from asynchronous_crunching import Project
from synchronous_crunching import simulate, list_simulate
from persistent_read_only_object import PersistentReadOnlyObject
import data_structures

__all__ = ["Project", "simulate", "list_simulate", "PersistentReadOnlyObject",
           "data_structures"]