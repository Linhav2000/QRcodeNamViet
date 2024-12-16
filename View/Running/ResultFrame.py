
from tkinter import messagebox
from View.Common.VisionUI import *
from tkinter import filedialog
from CommonAssit import VisionFont
from CommonAssit import Color

class ResultFrame(LabelFrame):

    def __init__(self, master, mainWindow, title, isCurrentFrame=False):
        LabelFrame.__init__(self, master=master, text=title, font=VisionFont.boldFont(10), bg=Color.resultBg(), fg=Color.winWhite())
        self.mainWindow = mainWindow
        self.isCurrentFrame = isCurrentFrame
        self.result = ResultStruct()
        self.setupView()
        self.showResult()



    def setupView(self):
        labelHeight = 25
        xPos = 135

        self.state = OKLabel(self, text="OK", size=55)
        self.state.place(relx=0.3, y=5)

        self.serialNoLabel = ResultLabel(self, text=self.mainWindow.languageManager.localized("serialNo"))
        self.serialNoLabel.place(x=5, y=5 + 4 * labelHeight)

        self.okLabel = OKLabel(self, text=self.mainWindow.languageManager.localized("okLbl"))
        self.okLabel.place(x=5, y=5 + 5 * labelHeight)
        self.okNum = OKLabel(self, text="0")
        self.okNum.place(x=xPos, y=5 + 5 * labelHeight)

        self.ngTorqueLabel = NGTorqueLabel(self, text=self.mainWindow.languageManager.localized("ngTorque"))
        self.ngTorqueLabel.place(x=5, y=5 + 6*labelHeight)
        self.ngTorqueNum = NGTorqueLabel(self, text="0")
        self.ngTorqueNum.place(x=xPos, y=5 + 6 * labelHeight)

        self.ngHeightLabel = NGHeightLabel(self, text=self.mainWindow.languageManager.localized("ngHeight"))
        self.ngHeightLabel.place(x=5, y=5 + 7*labelHeight)
        self.ngHeightNum = NGHeightLabel(self, text="0")
        self.ngHeightNum.place(x=xPos, y=5 + 7 * labelHeight)

        self.totalLabel = ResultLabel(self, text=self.mainWindow.languageManager.localized("total"))
        self.totalLabel.place(x=5, y=5 + 8*labelHeight)
        self.totalNum = ResultLabel(self, text="0")
        self.totalNum.place(x=xPos, y=5 + 8 * labelHeight)

        self.visionTimeLabel = ResultLabel(self, text=self.mainWindow.languageManager.localized("visionTime"))
        self.visionTimeLabel.place(x=5, y=5 + 9*labelHeight)
        self.visionTime = ResultLabel(self, text="0s")
        self.visionTime.place(x=xPos, y=5 + 9 * labelHeight)

        self.totalTimeLabel = ResultLabel(self, text=self.mainWindow.languageManager.localized("totalTime"))
        self.totalTimeLabel.place(x=5, y=5 + 10*labelHeight)
        self.totalTime = ResultLabel(self, text="0s")
        self.totalTime.place(x=xPos, y=5 + 10 * labelHeight)

        if self.isCurrentFrame:
            # self.btnOpen = OpenButton(self, lblText="Open", command=self.clickBtnOpen, font=Font.boldFont(12))
            self.btnOpen = ImageButton(self, imagePath="./resource/openFolder.png", command=self.clickBtnOpen, bg=Color.resultBg())
            self.btnOpen.place(x=5, y=5 + 12*labelHeight, relwidth=0.4, relheight=0.1)

    def clickBtnOpen(self):
        if self.mainWindow.workingThread.runningFlag:
            messagebox.showwarning("Open Old Product", "You cannot open previous product when running!")
            return
        path = filedialog.askdirectory(title="Open product image path")
        self.mainWindow.workingThread.ru_connectorCheckMissing.getResult(path)
        print(path)

    def showResult(self, result = None):
        if result is not None:
            self.result = result
        if self.result.ngHeight + self.result.ngTorque > 0:
            self.state = NGTorqueLabel(self, text="NG", size=55)
            self.state.place(relx=0.3, y=5)
        else:
            self.state = OKLabel(self, text="OK", size=55)
            self.state.place(relx=0.3, y=5)

        self.serialNoLabel.config(text="{} {}".format(self.mainWindow.languageManager.localized("serialNo"), self.result.serialNo))
        self.okNum.config(text=self.result.ok)
        self.ngTorqueNum.config(text=self.result.ngTorque)
        self.ngHeightNum.config(text=self.result.ngHeight)
        self.totalNum.config(text=self.result.total)
        self.visionTime.config(text="{}s".format(self.result.visionTime))
        self.totalTime.config(text="{}s".format(self.result.progressTime))


class ResultStruct:
    serialNo = "0000-0000-0000"
    total = 0
    ok = 0
    ngHeight = 0
    ngTorque = 0
    visionTime = 0
    progressTime = 0


class ResultLabel(Label):

    def __init__(self, master,  text):
        Label.__init__(self, master=master, text=text, font=VisionFont.boldFont(11), fg=Color.winWhite(), bg=Color.resultBg())

class OKLabel(Label):

    def __init__(self, master,  text, size=11):
        Label.__init__(self, master=master, text=text, font=VisionFont.boldFont(size=size), fg=Color.okColor(), bg=Color.resultBg())

class NGTorqueLabel(Label):

    def __init__(self, master,  text, size=11):
        Label.__init__(self, master=master, text=text, font=VisionFont.boldFont(size=size), fg=Color.winRed(), bg=Color.resultBg())

class NGHeightLabel(Label):

    def __init__(self, master,  text, size=11):
        Label.__init__(self, master=master, text=text, font=VisionFont.boldFont(size=size), fg=Color.winYellow(), bg=Color.resultBg())