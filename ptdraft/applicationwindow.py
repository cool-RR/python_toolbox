import wx
import os
from misc.stringsaver import s2i,i2s
import simulations.life.life as life
import simulations.life.lifegui as lifegui
import functools
import core
import guiproject
import misc.notebookctrl as notebookctrl

#import psyco
#psyco.full()




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
        filemenu.Append(s2i("Booga"),"&Booga"," Do the booga!")
        filemenu.Append(s2i("Agoob"),"&Agoob"," Do the agoob!")
        filemenu.Append(s2i("Exit"),"E&xit"," Close the program")
        wx.EVT_MENU(self,s2i("Exit"),self.exit)
        wx.EVT_MENU(self,s2i("Booga"),self.booga)
        wx.EVT_MENU(self,s2i("Agoob"),self.agoob)
        menubar=wx.MenuBar()
        menubar.Append(filemenu,"&File")
        #menubar.Append(stuffmenu,"&Stuff")
        #menubar.Append(nodemenu,"&Node")
        self.SetMenuBar(menubar)
        self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        toolbar.AddSimpleTool(s2i("Button New"), wx.Bitmap("images\\new.png", wx.BITMAP_TYPE_ANY),"New", " Create a new file")
        toolbar.AddSimpleTool(s2i("Button Open"), wx.Bitmap("images\\open.png", wx.BITMAP_TYPE_ANY),"Open", " Open a file")
        toolbar.AddSimpleTool(s2i("Button Save"), wx.Bitmap("images\\save.png", wx.BITMAP_TYPE_ANY),"Save", " Save to file")
        toolbar.Realize()

        self.Bind(wx.EVT_IDLE,self.sync_workers_wrapper)
        self.idle_block=False

        self.Show()

    def add_gui_project(self,gui_project):
        self.gui_projects.append(gui_project)
        self.notebook.AddPage(gui_project.main_window,"zort!")

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

    def booga(self,e):
        """
        This is something temporary that should be deleted eventually
        """
        gui_project=lifegui.LifeGuiProject(core.Project(life.Life),self.notebook)
        root=gui_project.make_random_root(28,40)
        gui_project.project.edges_to_crunch[root]=50

        self.add_gui_project(gui_project)

    def agoob(self,e):
        #self.delete_gui_project(self.gui_projects[0])
        pass

    def sync_workers_wrapper(self,e=None):
        """
        A function that calls `sync_workers` for all the
        open GuiProjects.
        """
        self.Refresh()
        if self.idle_block==True:
            return
        for thing in self.gui_projects:
            thing.project.sync_workers()
        wx.CallLater(150,self._clear_idle_block_and_do) # Should make the delay customizable?
        self.idle_block=True

    def _clear_idle_block_and_do(self):
        self.idle_block=False
        event=wx.PyEvent()
        event.SetEventType(wx.wxEVT_IDLE) # todo: change this to whatever wx constant name is given to the type of EVT_IDLE
        wx.PostEvent(self,event)




if __name__=="__main__":
    app = wx.PySimpleApp()
    my_app_win=ApplicationWindow(None,-1,"ViperSim",size=(600,600))

    app.MainLoop()