from garlicsim.general_misc import import_tools

import garlicsim

from .state import State


PROBLEM = SyntaxError
ENDABLE = False
VALID = False
CONSTANT_CLOCK_INTERVAL = None
HISTORY_DEPENDENT = False
N_STEP_FUNCTIONS = 0
DEFAULT_STEP_FUNCTION = None
DEFAULT_STEP_FUNCTION_TYPE = None
CRUNCHERS_LIST = \
    [garlicsim.asynchronous_crunching.crunchers.ThreadCruncher] + \
    (
        [garlicsim.asynchronous_crunching.crunchers.ProcessCruncher] if 
        import_tools.exists('multiprocessing')
        else []
    )