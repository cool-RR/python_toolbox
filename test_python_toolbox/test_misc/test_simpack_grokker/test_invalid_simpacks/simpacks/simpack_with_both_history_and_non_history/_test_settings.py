from garlicsim.general_misc import import_tools
from garlicsim.general_misc.reasoned_bool import ReasonedBool

import garlicsim
from garlicsim.misc import InvalidSimpack

from .state import State


ENDABLE = False
PROBLEM = None
VALID = ReasonedBool(
    False,
    reason=InvalidSimpack("The `simpack_with_both_history_and_non_history` "
                          "simpack is defining both a history-dependent step "
                          "and a non-history-dependent step - which is "
                          "forbidden.")
)
CONSTANT_CLOCK_INTERVAL = None
HISTORY_DEPENDENT = False
N_STEP_FUNCTIONS = 2
DEFAULT_STEP_FUNCTION = None
DEFAULT_STEP_FUNCTION_TYPE = None
CRUNCHERS_LIST = \
    [garlicsim.asynchronous_crunching.crunchers.ThreadCruncher] + \
    (
        [garlicsim.asynchronous_crunching.crunchers.ProcessCruncher] if 
        import_tools.exists('multiprocessing')
        else []
    )