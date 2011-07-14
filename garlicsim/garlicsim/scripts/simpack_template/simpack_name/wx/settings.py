# from .widgets import state_viewer as _
# from .widgets import state_creation_dialog as _
# from . import widgets


########### *All* of the settings in this module are optional. ################


# BIG_WORKSPACE_WIDGETS = [widgets.state_viewer.StateViewer]

# Widgets to show in the middle of the frame. These must be subclasses of
# `garlicsim_wx.widgets.workspace_widget.WorkspaceWidget`.
#
# This is where you usually put your main widget that displays your states.



# SMALL_WORKSPACE_WIDGETS = []

# (08.08.2011 - Still not implemented, sorry.)
#
# Small widgets to show in the frame. These must be subclasses of
# `garlicsim_wx.widgets.workspace_widget.WorkspaceWidget`.
#
# This is where you usually put small tools.



# SEEK_BAR_GRAPHS = []

# (08.08.2011 - Still not implemented, sorry.)
#
# List of scalar functions that should be shown as graphs in the seek bar.
#
# These may be either scalar state functions or scalar history functions.



# STATE_CREATION_FUNCTION = widgets.state_creation_dialog.\
#                           StateCreationDialog.create_show_modal_and_get_state

# Function for creating a new state. Takes the main GarlicSim `Frame`.
#
# This setting is usually set to a dialog's `.create_show_modal_and_get_state`
# class method, which creates the dialog with the frame as parent, calls
# `.ShowModal` on it, asks the user all kinds of questions about what kind of
# state he wants to create, and if the dialog ends with `wx.ID_OK` returns the
# state. (Or `None` if the user hit "Cancel".)
# 
# *But*, you can do it in any other way you'd like, as long as
# `STATE_CREATION_FUNCTION` is a function that takes the GarlicSim frame and
# returns the new state.


