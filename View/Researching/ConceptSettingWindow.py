import CommonAssit.CommonAssit as CommonAssit
import tkinter.messagebox as messagebox
from View.Common.VisionUI import *

class ConceptSetting(VisionTopLevel):
    okFlag = False

    def __init__(self, mainWindow, stepParameter):
        VisionTopLevel.__init__(self)
        self.stepParameter = stepParameter
        self.mainWindow = mainWindow
        self.setupView()
        self.showLastSetting()

    def setupView(self):
        self.settingWindow()
        self.setupParameterFrame()
        self.setupButton()

    def settingWindow(self):
        self.title("Setting Step {0}".format(self.stepParameter.stepId))
        self.iconbitmap(CommonAssit.resource_path('resource\\appIcon.ico'))
        width = 560
        height = 300
        self.geometry("{}x{}+{}+{}".format(width, height, int
        (self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width() / 2 - width / 2),
                                           int
                                               (
                                               self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height() / 2 - height / 2)))
        self.resizable(0, 0)
        self.grab_set()


    def setupParameterFrame(self):
        self.thresholdEntry = VisionEntry(self)
        self.thresholdEntry.place(x=10, y=10, width=200, height =30)

    def setupButton(self):
        self.okButton = OkButton(self, command=self.clickBtnOK)
        self.okButton.place(relx=0.25, rely=0.8, relwidth=0.2, relheight=0.1)

        self.exitButton = Button(self, text=self.mainWindow.languageManager.localized("exit"), command=self.clickBtnExit)
        self.exitButton.place(relx=0.55, rely=0.8, relwidth=0.2, relheight=0.1)


    def clickBtnOK(self):
        self.okFlag = True
        try:
            self.stepParameter.threshValue = int(float(self.thresholdEntry.get()))
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Step Setting : {}".format(error))
            messagebox.showerror("Step Setting", "{}".format(error))
        self.destroy()

    def clickBtnExit(self):
        self.okFlag = False
        self.destroy()

    def showLastSetting(self):
        return