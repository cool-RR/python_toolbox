import garlicsim

from .state import State

HISTORY_DEPENDENT = False
N_STEP_FUNCTIONS = 1
DEFAULT_STEP_FUNCTION = State.step
CRUNCHERS_LIST = [garlicsim.asynchronous_crunching.crunchers.ThreadCruncher]