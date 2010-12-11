import garlicsim

from .state import State

HISTORY_DEPENDENT = False
N_STEP_FUNCTIONS = 1
DEFAULT_STEP_FUNCTION = State.step
DEFAULT_STEP_FUNCTION_TYPE = \
    garlicsim.misc.simpack_grokker.step_types.SimpleStep
CONSTANT_CLOCK_INTERVAL = 1
ENDABLE = True
CRUNCHERS_LIST = \
    [garlicsim.asynchronous_crunching.crunchers.ThreadCruncher] + \
    (
        [garlicsim.asynchronous_crunching.crunchers.ProcessCruncher] if 
        hasattr(garlicsim.asynchronous_crunching.crunchers, 'ProcessCruncher')
        else []
    )
