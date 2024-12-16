from View.MissingMachine.MissingResultFrame import MissingResultFrame
from View.MissingMachine.MiddleFrame import MiddleFrame
from Modules.CheckMissing.ResultStruct import ResultStruct
from View.Common.VisionUI import *

class MissingMachineResultWindow(VisionTopLevel):

    leftFrame: MissingResultFrame
    rightFrame:MissingResultFrame
    middleFrame:MiddleFrame

    rightResult: ResultStruct
    leftResult: ResultStruct

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        VisionTopLevel.__init__(self)
        self.mainWindow: MainWindow = mainWindow
        # self.wm_attributes('-transparentcolor', self['bg'])
        self.setupWindow()

    def setupWindow(self):
        self.setupMainWindow()
        self.setupLefFrame()
        self.setupRightFrame()
        self.setupMiddleFrame()

    def setupMainWindow(self):
        width = 1240
        height = 665
        self.title(self.mainWindow.languageManager.localized("version"))
        iconPath = "./resource/appIcon.ico"
        self.iconbitmap(iconPath)
        self.geometry("{}x{}+{}+{}".format(width, height, int
        (self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width() / 2 - width / 2),
                                           int
                                               (
                                               self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height() / 2 - height / 2)))
        self.state("zoomed")
        # self.mainFrame.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.exit)

    def setupLefFrame(self):
        self.leftResult = self.mainWindow.workingThread.rearCheckMissing.leftResult
        self.leftFrame = MissingResultFrame(self, self.mainWindow, self.leftResult, "LEFT")
        self.leftFrame.place(relx=0, rely=0, relwidth=0.4, relheight=1)


    def setupRightFrame(self):
        self.rightResult = self.mainWindow.workingThread.rearCheckMissing.rightResult
        self.rightFrame=MissingResultFrame(self, self.mainWindow, self.rightResult, "RIGHT")
        self.rightFrame.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)

    def setupMiddleFrame(self):
        self.middleFrame = MiddleFrame(self, self.mainWindow)
        self.middleFrame.place(relx=0.4, rely=0, relwidth=0.2, relheight=1)

    def exit(self):
        if self.mainWindow.workingThread.runningFlag:
            if not self.middleFrame.clickBtnStart():
                return
        # self.middleFrame.clock.stop()
        self.mainWindow.show()
        self.hide()

    def show(self):
        self.update()
        self.deiconify()
        self.state("zoomed")
        self.mainWindow.workingThread.rearCheckMissing.updateModel()
        # self.middleFrame.clock.start()
        self.middleFrame.updateStartButton()
        self.middleFrame.updateModelName()
        try:
            self.leftFrame.missingDetailFrame.updateAlgorithmName(self.mainWindow.workingThread.rearCheckMissing.leftAlgorithm.algorithmParameter.name)
        except:
            self.leftFrame.missingDetailFrame.updateAlgorithmName("NOT CONFIG")
        try:
            self.rightFrame.missingDetailFrame.updateAlgorithmName(self.mainWindow.workingThread.rearCheckMissing.rightAlgorithm.algorithmParameter.name)
        except:
            self.rightFrame.missingDetailFrame.updateAlgorithmName("NOT CONFIG")

        try:
            self.rightFrame.missingDetailFrame.updateCameraSelected("Camera {}".format(self.mainWindow.workingThread.rearCheckMissing.currentModel.rightCameraId))
        except:
            self.rightFrame.missingDetailFrame.updateCameraSelected("NOT CONFIG")

        try:
            self.leftFrame.missingDetailFrame.updateCameraSelected("Camera {}".format(self.mainWindow.workingThread.rearCheckMissing.currentModel.leftCameraId))
        except:
            self.leftFrame.missingDetailFrame.updateCameraSelected("NOT CONFIG")


    def hide(self):
        self.withdraw()
