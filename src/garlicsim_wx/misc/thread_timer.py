# Copyright 2009 Ram Rachum.
# This program is not licensed for distribution and may not be distributed.

"""
todo: daemonize? destroy on __del__?
"""


import threading
import time
import wx

wxEVT_THREAD_TIMER = wx.NewEventType()
EVT_THREAD_TIMER = wx.PyEventBinder(wxEVT_THREAD_TIMER, 1)

class ThreadTimer(object):
   n = 0
   def __init__(self, parent):
      self.parent = parent
      ThreadTimer.n += 1
      thread_name = "ThreadTimer Thread no. " + str(self.n)
      self.thread = Thread(name=thread_name)
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
      interval_in_seconds = self.parent.interval / 1000.0
      def sleep():
            time.sleep(interval_in_seconds)

      sleep()
      try:
         while self.parent.alive:
            event = wx.PyEvent()
            event.SetEventType(wxEVT_THREAD_TIMER)
            wx.PostEvent(self.parent.parent, event)
            sleep()
      except:
         return # Just so it wouldn't raise an error when wx is shutting down