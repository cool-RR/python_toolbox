from ..life import State, changes
from . import widgets
from state_creation_dialog import StateCreationDialog

SEEK_BAR_GRAPHS = [State.get_n_live_cells, changes]
BIG_WORKSPACE_WIDGETS = [widgets.BoardViewer]
SMALL_WORKSPACE_WIDGETS = []
STATE_CREATION_DIALOG = StateCreationDialog