# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import wx
import wx.lib.scrolledpanel as scrolled

'''
tododoc
'''



from enthought.traits.api import HasTraits, Range, Instance, \
     on_trait_change
from enthought.traits.ui.api import View, Item, HGroup
from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.mayavi.tools.mlab_scene_model import \
     MlabSceneModel
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene


from numpy import linspace, pi, cos, sin

def curve(n_mer, n_long):
    phi = linspace(0, 2*pi, 2000)
    return [ cos(phi*n_mer) * (1 + 0.5*cos(n_long*phi)),
            sin(phi*n_mer) * (1 + 0.5*cos(n_long*phi)),
            0.5*sin(n_long*phi),
            sin(phi*n_mer)]



class Visualization(HasTraits):
    meridional = Range(1, 30,  6)
    transverse = Range(0, 30, 11)
    scene      = Instance(MlabSceneModel, ())

    def __init__(self):
        # Do not forget to call the parent's __init__
        HasTraits.__init__(self)
        x, y, z, t = curve(self.meridional, self.transverse)
        self.plot = self.scene.mlab.plot3d(x, y, z, t, colormap='Spectral')

    @on_trait_change('meridional,transverse')
    def update_plot(self):
        x, y, z, t = curve(self.meridional, self.transverse)
        self.plot.mlab_source.set(x=x, y=y, z=z, scalars=t)


    # the layout of the dialog created
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                    height=250, width=300, show_label=False),
                HGroup(
                        '_', 'meridional', 'transverse',
                    ),
                )
                
    
class StateViewer(wx.lib.scrolledpanel.ScrolledPanel):
    '''
    
    '''
    def __init__(self, parent, id, gui_project, *args, **kwargs):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, id,
                                                    style=wx.SUNKEN_BORDER,
                                                    *args,
                                                    **kwargs)
        self.SetupScrolling()
        #self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        #self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)

        self.gui_project = gui_project
        
        self.visualization = Visualization()
        self.control = \
            self.visualization.edit_traits(parent=self, kind='subpanel').control
        
        self.state = None
        
        self.font = wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD, face='Courier New')

        
    def load_state(self, state):
        '''Set the state to be displayed.'''
        self.state = state
        #self.Refresh()

    
    def on_size(self, e=None):
        '''Refresh the widget.'''
        self.Refresh()
        if e is not None:
            e.Skip()

