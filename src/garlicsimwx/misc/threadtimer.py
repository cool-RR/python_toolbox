import threading
import time
import wx

wxEVT_THREAD_TIMER = wx.NewEventType()
EVT_THREAD_TIMER = wx.PyEventBinder(wxEVT_THREAD_TIMER, 1)

class ThreadTimer(object):
   def __init__(self, parent):
        self.parent = parent
        self.thread = Thread()
        self.thread.parent = self
        self.alive = False

   def start(self, interval):
       self.interval = interval
       self.alive = True
       self.thread.start()

   def stop(self):
       self.alive = False

class Thread(threading.Thread):
    def run(self):
       while self.parent.alive:
           time.sleep(self.parent.interval / 1000.0)
           event = wx.PyEvent()
           event.SetEventType(wxEVT_THREAD_TIMER)
           wx.PostEvent(self.parent.parent, event)