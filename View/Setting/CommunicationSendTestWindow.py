
from View.Common.VisionUI import *

class CommunicationSendTestWindow(VisionTopLevel):
    messageEntry: VisionEntry
    btnSend: VisionButton

    def __init__(self, mainWindow):
        VisionTopLevel.__init__(self)
        self.mainWindow = mainWindow
        self.setupWindow()
        self.setupView()

    def setupWindow(self):
        self.title("Communication Send Test")
        self.iconbitmap('resource\\appIcon.ico')
        self.geometry("678x222+{}+{}".format(int(self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width()/2 - 436/2),
                                             int(self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height()/2 - 222/2)))
        self.resizable(0, 0)
        self.grab_set()

    def setupView(self):
        self.messageEntry = VisionEntry(self)
        self.messageEntry.place(relx = 0.05, rely=0.4, relwidth=0.6, relheight=0.15)
        self.btnSend = VisionButton(self, text="Send",command=self.sendTest)
        self.btnSend.place(relx = 0.7, rely=0.4, relwidth=0.25, relheight=0.15)

    def sendTest(self):
        self.mainWindow.workingThread.connectionManager.sendData(self.messageEntry.get())
