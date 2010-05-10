from life import *
import garlicsim

DETERMINISM_FUNCTION = determinism_function
SCALAR_STATE_FUNCTIONS = [live_cells]
SCALAR_HISTORY_FUNCTIONS = [changes]
FORCE_CRUNCHER = garlicsim.asynchronous_crunching.crunchers.CruncherThread