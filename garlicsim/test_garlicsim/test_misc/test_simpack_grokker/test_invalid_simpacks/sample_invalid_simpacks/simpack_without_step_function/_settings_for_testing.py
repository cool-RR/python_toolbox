from garlicsim.general_misc.reasoned_bool import ReasonedBool

import garlicsim
from garlicsim.misc import InvalidSimpack


from .state import State

ENDABLE = False
VALID = ReasonedBool(
    False,
    reason=InvalidSimpack("The `simpack_without_step_function` simpack has "
                          "not defined any kind of step function.")
)
CONSTANT_CLOCK_INTERVAL = None
HISTORY_DEPENDENT = False
N_STEP_FUNCTIONS = 1
DEFAULT_STEP_FUNCTION = State.step
DEFAULT_STEP_FUNCTION_TYPE = \
    garlicsim.misc.simpack_grokker.step_types.SimpleStep
CRUNCHERS_LIST = \
    [garlicsim.asynchronous_crunching.crunchers.ThreadCruncher] + \
    (
        [garlicsim.asynchronous_crunching.crunchers.ProcessCruncher] if 
        hasattr(garlicsim.asynchronous_crunching.crunchers, 'ProcessCruncher')
        else []
    )