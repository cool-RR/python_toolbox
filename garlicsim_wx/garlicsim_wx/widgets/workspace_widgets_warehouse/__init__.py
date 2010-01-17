# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied or
# distributed without explicit written permission from Ram Rachum.

'''
A warehouse of various custom wxPython widgets used in the workspace.
'''

import sys
import garlicsim_wx
from garlicsim.general_misc import warehouse

workspace_widgets = warehouse.create(sys.modules[__name__])

assert all(isinstance(widget, garlicsim_wx.widgets.WorkspaceWidget) for widget
           in workspace_widgets)