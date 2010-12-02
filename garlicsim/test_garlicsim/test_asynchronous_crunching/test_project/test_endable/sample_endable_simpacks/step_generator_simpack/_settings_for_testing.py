import garlicsim

from .state import State

HISTORY_DEPENDENT = False
N_STEP_FUNCTIONS = 1
STEP_FUNCTION_TYPE = garlicsim.misc.simpack_grokker.step_types.StepGenerator
DEFAULT_STEP_FUNCTION = State.step_generator
CRUNCHERS_LIST = [garlicsim.asynchronous_crunching.crunchers.ThreadCruncher,
                  garlicsim.asynchronous_crunching.crunchers.ProcessCruncher]
# tododoc: probably add ENDABLE flag