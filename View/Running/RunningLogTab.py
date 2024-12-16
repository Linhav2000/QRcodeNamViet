from View.Common.VisionUI import *

class RunningLogTab(VisionFrame):

    logView: Text
    logFrame: VisionFrame

    printLogVar: BooleanVar
    printLogCheck: VisionCheckBox

    def __init__(self, root: ttk.Notebook, mainWindow):
        from MainWindow import MainWindow
        VisionFrame.__init__(self, root)
        self.root = root
        self.mainWindow: MainWindow = mainWindow

        self.setupView()
        self.pack(fill='both', expand=1)

    def setupView(self):
        # self.btnTest = Button(self, text="Test")
        # self.btnTest.place(relx=0.5, rely=0.5)
        self.setupLogView()


    def setupLogView(self):
        self.logFrame = VisionFrame(self)
        self.logFrame.place(x=0, rely=0, relwidth=1, relheight=1)

        scrollbar = Scrollbar(self.logFrame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.logView = Text(self.logFrame, yscrollcommand=scrollbar.set)
        self.logView.place(x=0, y=0, relwidth=0.95, relheight=0.92)

        scrollbar.config(command=self.logView.yview)

        self.printLogVar = BooleanVar()
        self.printLogCheck = VisionCheckBox(self, text="Print Log", variable=self.printLogVar,
                                            command=self.clickPrintLogCheck, font=VisionFont.boldFont(10))
        self.printLogCheck.place(relx=0.05, rely=0.92)

        self.printLogVar.set(self.mainWindow.commonSettingManager.settingParm.printLogFlag)

    def clickPrintLogCheck(self, event=None):
        self.mainWindow.commonSettingManager.settingParm.printLogFlag = self.printLogVar.get()
        self.mainWindow.commonSettingManager.save()
