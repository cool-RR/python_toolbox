# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Settings module for the `wx` component of the `life` simpack.'''


from . import widgets

#SEEK_BAR_GRAPHS = [State.get_n_live_cells, changes]
BIG_WORKSPACE_WIDGETS = [widgets.StateViewer]
SMALL_WORKSPACE_WIDGETS = []
STATE_CREATION_FUNCTION = \
    widgets.StateCreationDialog.create_show_modal_and_get_state