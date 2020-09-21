from PyQt5.QtCore import QThread
import time

class myThread(QThread):
   """docstring for myThread"""
   def __init__(self, name, _function, delay):
      super(myThread, self).__init__()
      self.name= name
      self._function= _function
      self.delay= delay
      self.isRunning = True     

   def run(self):
      print ("san sang chay " + self.name)
      while True:
         time.sleep(self.delay)
         if self.isRunning:
            self._function()

      print("finised Thread")  

         

      