import wx
import os
from misc.stringsaver import s2i,i2s
from misc.dumpqueue import dump_queue
import time
import customwidgets
from core import *
import simulations.life.life as life
import simulations.life.lifegui as lifegui
import threading
#from renderingmanager import RenderingManager
from edgerenderer import EdgeRenderer
import niftylock
import random




class time_to_talk_with_manager_event(wx.PyCommandEvent):
    pass

myEVT_TIME_TO_TALK_WITH_MANAGER=wx.NewEventType()
EVT_TIME_TO_TALK_WITH_MANAGER=wx.PyEventBinder(myEVT_TIME_TO_TALK_WITH_MANAGER,1)



class myframe(wx.Frame):
    def __init__(self,*args,**keywords):
        wx.Frame.__init__(self,*args,**keywords)
        self.nib_icon=wx.Bitmap("images\\circle.png", wx.BITMAP_TYPE_ANY)
        self.touched_nib_icon=wx.Bitmap("images\\star.png", wx.BITMAP_TYPE_ANY)

        filemenu=wx.Menu()
        filemenu.Append(s2i("Open"),"&Open"," Open a file")
        filemenu.AppendSeparator()
        filemenu.Append(s2i("Exit"),"E&xit"," Close the program")

        stuffmenu=wx.Menu()
        stuffmenu.Append(s2i("Calculate"),"&Calculate","")
        stuffmenu.Append(s2i("Play"),"&Play","")


        wx.EVT_MENU(self,s2i("Exit"),self.exit)

        wx.EVT_MENU(self,s2i("Calculate"),self.calculate)
        wx.EVT_MENU(self,s2i("Play"),self.play)



        menubar=wx.MenuBar()
        menubar.Append(filemenu,"&File")
        menubar.Append(stuffmenu,"&Stuff")
        self.SetMenuBar(menubar)
        self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        toolbar.AddSimpleTool(s2i("Button New"), wx.Bitmap("images\\new.png", wx.BITMAP_TYPE_ANY),"New", " Create a new file")
        toolbar.AddSimpleTool(s2i("Button Open"), wx.Bitmap("images\\open.png", wx.BITMAP_TYPE_ANY),"Open", " Open a file")
        toolbar.AddSimpleTool(s2i("Button Save"), wx.Bitmap("images\\save.png", wx.BITMAP_TYPE_ANY),"Save", " Save to file")
        toolbar.Realize()

        self.thing=wx.ScrolledWindow(self,-1)
        self.timeline=customwidgets.Timeline(self,-1)



        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.thing,1,wx.EXPAND)
        self.sizer.Add(self.timeline,0,wx.EXPAND)


        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        #self.sizer.Fit(self)

        #self.Bind(wx.EVT_PAINT, self.draw)

        self.Show()
        #self.draw()

        self.mygui=lifegui.LifeGuiPlayon(Playon(life.Life),self.thing)
        self.root=self.mygui.playon.make_random_root(30,30)
        self.path=nib.Path(self.mygui.playon.nibtree,self.root)
        self.timeline.set_path(self.path)
        self.edges_to_render=[self.root]
        self.workers={}

        #self.rendering_manager=RenderingManager()

        #self.Bind(EVT_TIME_TO_TALK_WITH_MANAGER,self.talk_with_manager)
        self.Bind(wx.EVT_IDLE,self.talk_with_manager)

    def calculate(self,e):
        try:
            self.deus=self.tres
        except:
            self.deus=self.tres=self.root

        self.tres=self.mygui.playon.multistep(self.deus,steps=100)
        self.timeline.Refresh()


    def play(self,e):
        self.mygui.play_path(self.path,0.1)


    def draw(self,e=None):
        pass


    def exit(self,e):
        self.Close()

    def talk_with_manager(self,e=None): #Actually, I think I'll deprecate the manager
        for edge in self.workers:
            if not (edge in self.edges_to_render):
                #TAKE WORK FROM WORKER AND RETIRE IT, ALSO DELETE FROM self.workers
                print("shit")
                worker=self.workers[edge]
                result=dump_queue(worker.work_queue)

                worker.message_queue.put("Terminate")

                current=edge
                for nib in result:
                    current=self.mygui.playon.nibtree.add_nib(nib,parent=current)

                del self.workers[edge]
                worker.join()



        for edge in self.edges_to_render[:]:
            if self.workers.has_key(edge):
                #TAKE WORK FROM WORKER, CHANGE EDGE
                #IMPLEMENT INTO NIBTREE
                worker=self.workers[edge]
                result=dump_queue(worker.work_queue)
                """
                if result!=[]:
                    print(result)
                """
                #print worker

                current=edge
                for nib in result:
                    current=self.mygui.playon.nibtree.add_nib(nib,parent=current)

                self.edges_to_render.remove(edge)
                self.edges_to_render.append(current)

                del self.workers[edge]
                self.workers[current]=worker

            else:
                #CREATE WORKER
                thing=self.workers[edge]=EdgeRenderer(edge)
                thing.start()

        if random.randint(0,4)==0:
            self.Refresh()



if __name__=="__main__":
    app = wx.PySimpleApp()
    fugi=myframe(None,-1,"Title",size=(600,600))
    app.MainLoop()