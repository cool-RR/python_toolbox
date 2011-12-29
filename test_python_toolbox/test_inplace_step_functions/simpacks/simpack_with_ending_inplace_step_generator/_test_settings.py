from garlicsim.general_misc import import_tools

import garlicsim

from .state import State

ENDABLE = False
PROBLEM = None
VALID = True
CONSTANT_CLOCK_INTERVAL = 1
HISTORY_DEPENDENT = False
N_STEP_FUNCTIONS = 1
DEFAULT_STEP_FUNCTION = State.inplace_step_generator
DEFAULT_STEP_FUNCTION_TYPE = \
    garlicsim.misc.simpack_grokker.step_types.InplaceStepGenerator
CRUNCHERS_LIST = \
    [garlicsim.asynchronous_crunching.crunchers.ThreadCruncher] + \
    (
        [garlicsim.asynchronous_crunching.crunchers.ProcessCruncher] if 
        import_tools.exists('multiprocessing')
        else []
    )