from CommonAssit import TimeControl
from View.Common.VisionUI import *
import threading

class Clock(VisionLabel):
    runningFlag = False
    def __init__(self, master):
        VisionLabel.__init__(self, master)
        thread = threading.Thread(target=self.tiktokThread, args=())
        thread.start()

    def tiktokThread(self):
        while self.runningFlag:
            time = TimeControl.ymd_HMSFormat()
            self.config(text=time)
            TimeControl.sleep(5)

    def stop(self):
        self.runningFlag = False

    def start(self):
        if self.runningFlag:
            return
        else:
            self.runningFlag = True
        thread = threading.Thread(target=self.tiktokThread, args=())
        thread.start()
