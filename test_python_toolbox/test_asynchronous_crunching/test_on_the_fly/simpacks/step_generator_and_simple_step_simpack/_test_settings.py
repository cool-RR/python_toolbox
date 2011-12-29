from garlicsim.general_misc import import_tools

import garlicsim

from .state import State

HISTORY_DEPENDENT = False
N_STEP_FUNCTIONS = 2
DEFAULT_STEP_FUNCTION_TYPE = \
    garlicsim.misc.simpack_grokker.step_types.StepGenerator
DEFAULT_STEP_FUNCTION = State.step_generator
CONSTANT_CLOCK_INTERVAL = 1
ENDABLE = False
PROBLEM = None
VALID = True
CRUNCHERS_LIST = \
    [garlicsim.asynchronous_crunching.crunchers.ThreadCruncher] + \
    (
        [garlicsim.asynchronous_crunching.crunchers.ProcessCruncher] if 
        import_tools.exists('multiprocessing')
        else []
    )