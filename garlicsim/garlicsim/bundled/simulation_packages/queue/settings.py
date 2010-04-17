from __init__ import *
from garlicsim.misc import settings

DETERMINISM = settings.DETERMINISTIC
SCALAR_STATE_FUNCTIONS = [live_cells]
SCALAR_HISTORY_FUNCTIONS = [changes]