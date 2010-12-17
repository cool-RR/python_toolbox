from garlicsim.general_misc import import_tools
from garlicsim.general_misc.reasoned_bool import ReasonedBool

import garlicsim
from garlicsim.misc import InvalidSimpack

from .state import State


ENDABLE = False
PROBLEM = None
VALID = ReasonedBool(
    False,
    reason=InvalidSimpack("The `CRUNCHERS` setting must be either a "
                          "cruncher type (or name string), a list of "
                          "cruncher types, or a filter function for "
                          "cruncher types. You supplied `None`, which is "
                          "neither.")
)
CONSTANT_CLOCK_INTERVAL = None
HISTORY_DEPENDENT = False
N_STEP_FUNCTIONS = 1
DEFAULT_STEP_FUNCTION = None
DEFAULT_STEP_FUNCTION_TYPE = None
CRUNCHERS_LIST = \
    [garlicsim.asynchronous_crunching.crunchers.ThreadCruncher] + \
    (
        [garlicsim.asynchronous_crunching.crunchers.ProcessCruncher] if 
        import_tools.exists('multiprocessing')
        else []
    )