import tkinter.messagebox as messagebox
import CommonAssit.CommonAssit as CommonAssit
from View.Common.VisionUI import *


class EthernetSettingView(VisionTopLevel):

    ipEntry: VisionEntry
    portEntry: VisionEntry
    btnSave: Button

    def __init__(self, mainWindow, sockInfo, title = ''):
        from MainWindow import MainWindow
        from Connection.SocketManager import SocketInfo
        VisionTopLevel.__init__(self)
        self._title = title
        self.socketInfo:SocketInfo = sockInfo
        self.mainWindow: MainWindow = mainWindow
        self.windowSetting()
        self.createView()
        self.showLastSetting()

    def windowSetting(self):
        self.title(self._title)
        self.iconbitmap(CommonAssit.resource_path('resource\\appIcon.ico'))
        self.geometry("436x222+{}+{}".format(int(self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width()/2 - 436/2),
                                             int(self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height()/2 - 222/2)))
        self.resizable(0, 0)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.close)

    def createView(self):
        ipLabel = VisionLabel(self, text="IP adress : ")
        ipLabel.place(x=10, y =30)
        self.ipEntry = VisionEntry(self)
        self.ipEntry.place(relx=0.2, y=30, relwidth=0.7, height=25)

        portLabel = VisionLabel(self, text="Port : ")
        portLabel.place(x=10, y=70)
        self.portEntry = VisionEntry(self)
        self.portEntry.place(relx=0.2, y=70, relwidth=0.3, height=25)

        self.btnSave = SaveButton(self, command=self.save)
        self.btnSave.place(relx= 0.35, y=120, relwidth=0.3, height=40)

    def save(self):
        self.socketInfo.port = self.getPort()
        self.socketInfo.host = self.ipEntry.get()
        self.socketInfo.save()
        self.destroy()

    def getPort(self):
        try:
            value = int(self.portEntry.get())
        except:
            value = 0
            messagebox.showerror("error", "{} is not int value".format(self.portEntry.get()))

        return value


    def showLastSetting(self):
        self.ipEntry.insert(0, "{}".format(self.socketInfo.host))
        self.portEntry.insert(0, "{}".format(self.socketInfo.port))

    def close(self):
        if self.dataIsChanged():
            ask = messagebox.askyesno("Save information", "Do you want to save data")
            if ask == "yes":
                self.save()
        self.destroy()

    def dataIsChanged(self):
        if (self.socketInfo.host != self.ipEntry.get()) or (self.socketInfo.port != self.getPort()):
            return True
        else:
            return False
