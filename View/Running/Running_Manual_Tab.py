from View.Common.VisionUI import *
from View.Running.DDK.DDK_Manual_Signal_Frame import DDK_Manual_Signal_Frame

class Running_Manual_Tab(VisionFrame):
    ddk_manual_signal_frame: DDK_Manual_Signal_Frame = None
    current_frame = None
    def __init__(self, root: ttk.Notebook, mainWindow):
        from MainWindow import MainWindow
        VisionFrame.__init__(self, root)
        self.root = root
        self.mainWindow: MainWindow = mainWindow

        self.setupView()
        self.pack(fill='both', expand=1)


    def setupView(self):
        return

    def updateView(self):
        machineName = self.mainWindow.startingWindow.machineName
        if machineName.is_ddk_inspection():
            if self.ddk_manual_signal_frame is None:
                self.ddk_manual_signal_frame = DDK_Manual_Signal_Frame(self)
            self.current_frame = self.ddk_manual_signal_frame
            self.current_frame.place(relx=0, rely=0, relheight=1, relwidth=1)