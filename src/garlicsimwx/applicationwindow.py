import os, sys

import wx

import garlicsim
from misc.stringsaver import s2i,i2s
import guiproject
import misc.notebookctrl as notebookctrl
import customwidgets

#import psyco
#psyco.full()

def get_program_path():
    module_file = __file__
    module_dir = os.path.split(os.path.abspath(module_file))[0]
    program_folder = os.path.abspath(module_dir)
    return program_folder

os.chdir(get_program_path())
sys.path.append(get_program_path())

class ApplicationWindow(wx.Frame):
    """
    An application window that allows the user to open multiple GuiProjects
    simultaneously.
    """
    def __init__(self,*args,**keywords):

        wx.Frame.__init__(self,*args,**keywords)
        self.SetDoubleBuffered(True)
        self.notebook=notebookctrl.NotebookCtrl(self,-1,style=notebookctrl.NC_TOP)


        self.gui_projects=[]

        filemenu=wx.Menu()
        filemenu.Append(s2i("New"),"&New"," New")
        filemenu.Append(s2i("Exit"),"E&xit"," Close the program")
        wx.EVT_MENU(self,s2i("New"),self.on_new)
        wx.EVT_MENU(self,s2i("Exit"),self.exit)
        menubar=wx.MenuBar()
        menubar.Append(filemenu,"&File")
        #menubar.Append(stuffmenu,"&Stuff")
        #menubar.Append(nodemenu,"&Node")
        self.SetMenuBar(menubar)
        self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        toolbar.AddSimpleTool(s2i("Button New"), wx.Bitmap("images\\new.png", wx.BITMAP_TYPE_ANY),"New", " Create a new file")
        #toolbar.AddSimpleTool(s2i("Button Open"), wx.Bitmap(folder+"images\\open.png", wx.BITMAP_TYPE_ANY),"Open", " Open a file")
        #toolbar.AddSimpleTool(s2i("Button Save"), wx.Bitmap(folder+"images\\save.png", wx.BITMAP_TYPE_ANY),"Save", " Save to file")
        toolbar.AddSeparator()
        toolbar.AddSimpleTool(s2i("Button Done editing"), wx.Bitmap("images\\check.png", wx.BITMAP_TYPE_ANY),"Done editing", " Done editing")
        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.on_new, id=s2i("Button New"))
        self.Bind(wx.EVT_TOOL, self.done_editing, id=s2i("Button Done editing"))


        self.Bind(wx.EVT_IDLE,self.sync_workers_wrapper)
        self.idle_block=False

        self.Show()

    def add_gui_project(self,gui_project):
        self.gui_projects.append(gui_project)
        self.notebook.AddPage(gui_project.main_window,"zort!",select=True)
        gui_project.set_parent_window(self.notebook)

    """
    def delete_gui_project(self,gui_project):
        I did this wrong.
        self.gui_projects.remove(gui_project)
        self.notebook.AddPage(gui_project.main_window,"zort!")
        self.notebook.DeletePage(0)
        del gui_project
    """

    def exit(self,e):
        self.Close()

    def done_editing(self,e=None):
        gui_project=self.get_active_gui_project()
        gui_project.done_editing()

    def get_active_gui_project(self):
        selected_tab=self.notebook.GetPage(self.notebook.GetSelection())
        for gui_project in self.gui_projects:
            if gui_project.main_window==selected_tab:
                return gui_project
        raise StandardError("No GuiProject selected.")

    def on_new(self,e):
        dialog=customwidgets.SimulationPackageSelectionDialog(self,-1)
        if dialog.ShowModal() == wx.ID_OK:
            specific_simulation_package=dialog.get_simulation_package_selection()
        else:
            dialog.Destroy()
            return
        dialog.Destroy()

        gui_project=guiproject.GuiProject(specific_simulation_package,self.notebook)
        self.add_gui_project(gui_project)
        root=gui_project.make_random_root(80,40)
        gui_project.project.edges_to_crunch[root]=50
        gui_project.make_active_node(root)

    def sync_workers_wrapper(self,e=None):
        """
        A function that calls `sync_workers` for all the
        open GuiProjects.
        """

        if self.idle_block==True:
            return


        for thing in self.gui_projects:
            thing.sync_workers()

        wx.CallLater(150,self._clear_idle_block_and_do) # Should make the delay customizable?
        self.idle_block=True

    def _clear_idle_block_and_do(self):
        self.idle_block=False
        event=wx.PyEvent()
        event.SetEventType(wx.wxEVT_IDLE)
        wx.PostEvent(self,event)


def main():
    app = wx.PySimpleApp()
    my_app_win=ApplicationWindow(None,-1,"GarlicSim",size=(600,600))

    """
    import cProfile
    cProfile.run("app.MainLoop()")
    """
    app.MainLoop()



if __name__=="__main__":
    main()
