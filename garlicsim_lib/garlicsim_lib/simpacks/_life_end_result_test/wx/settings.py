from ..life import live_cells, changes
from . import widgets
from state_creation_dialog import StateCreationDialog

SEEK_BAR_GRAPHS = [live_cells, changes]
BIG_WORKSPACE_WIDGETS = [widgets.BoardViewer]
SMALL_WORKSPACE_WIDGETS = []
STATE_CREATION_DIALOG = StateCreationDialog