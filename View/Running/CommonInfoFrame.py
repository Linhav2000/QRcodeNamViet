from View.Common.VisionUI import *
from View.Common.InfoFrame import InfoFrame

class CommonInfoLabelFrame(ResultLabelFrame):
    labelHeight = 35

    def __init__(self, master, title, mainWindow):
        from MainWindow import MainWindow
        ResultLabelFrame.__init__(self, master=master, title=title)
        self.mainWindow: MainWindow = mainWindow
        self.setupView()

    def setupView(self):
        from Connection.CommandFrame import LocationDemoComFrame
        self.machineName = InfoFrame(self, "Machine :", "")
        self.machineName.place(relx=0, y=5 + 0 * self.labelHeight, relwidth=1, height=self.labelHeight)

        self.commonConection = InfoFrame(self, "Connection :", self.mainWindow.commonSettingManager.settingParm.communicationType)
        self.commonConection.place(relx=0, y=5 + 1 * self.labelHeight, relwidth=1, height=self.labelHeight)

        self.currentCamera = InfoFrame(self, "Camera ID :",
                                         self.mainWindow.commonSettingManager.settingParm.currentCamera)
        self.currentCamera.place(relx=0, y=5 + 2 * self.labelHeight, relwidth=1, height=self.labelHeight)

        self.takePicCmd = InfoFrame(self, "Check cmd :", "TakePic")
        self.takePicCmd.place(relx=0, y=5 + 3 * self.labelHeight, relwidth=1, height=self.labelHeight)

        self.okCmd = InfoFrame(self, "OK cmd :", LocationDemoComFrame.sendOK.value)
        self.okCmd.place(relx=0, y=5 + 4 * self.labelHeight, relwidth=1, height=self.labelHeight)

        self.ngCmd = InfoFrame(self, "NG cmd :", LocationDemoComFrame.sendNG.value)
        self.ngCmd.place(relx=0, y=5 + 5 * self.labelHeight, relwidth=1, height=self.labelHeight)

    def updateInfo(self):
        self.machineName.setValue(self.mainWindow.startingWindow.machineName.value)
        self.commonConection.setValue(self.mainWindow.commonSettingManager.settingParm.communicationType)
        self.currentCamera.setValue(self.mainWindow.commonSettingManager.settingParm.currentCamera)
