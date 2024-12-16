from CommonAssit import VisionFont
from CommonAssit import TimeControl
from tkinter import messagebox
from tkinter import filedialog
import cv2 as cv
from Modules.CheckMissing.ResultStruct import ResultStruct
from CommonAssit.FileManager import JsonFile
import jsonpickle
from View.Common.VisionUI import *

class DateInfoFrame(LabelFrame):

    def __init__(self, master, mainWindow, title, side):
        LabelFrame.__init__(self, master=master, text=title, font=VisionFont.boldFont(10), bg=Color.resultBg(), fg=Color.winWhite())
        self.mainWindow = mainWindow
        self.side = side
        self.result = ResultStruct()
        self.getInfo()
        self.setupView()
        self.showResult()

    def setupView(self):
        labelHeight = 40
        xPos = 150

        self.dateLabel = ResultLabel(self, text=TimeControl.ymdFormat())
        self.dateLabel.place(relx=0, rely=0, relwidth=1)

        self.okLabel = OKLabel(self, text=self.mainWindow.languageManager.localized("missing_ok"))
        self.okLabel.place(x=5, y=15 + 1 * labelHeight)
        self.okNum = OKLabel(self, text="0")
        self.okNum.place(x=xPos, y=15 + 1 * labelHeight)

        self.ngLabel = NGLabel(self, text=self.mainWindow.languageManager.localized("missing_ng"))
        self.ngLabel.place(x=5, y=15 + 2 * labelHeight)
        self.ngNum = NGLabel(self, text="0")
        self.ngNum.place(x=xPos, y=15 + 2 * labelHeight)

        self.totalLabel = TotalLabel(self, text=self.mainWindow.languageManager.localized("missing_total"))
        self.totalLabel.place(x=5, y=15 + 3*labelHeight)
        self.totalNum = TotalLabel(self, text="0")
        self.totalNum.place(x=xPos, y=15 + 3 * labelHeight)

        self.btnReset = ResetButton(self, command=self.clickBtnReset, bg=Color.resultBg())
        self.btnReset.place(relx=0.05, rely=0.88, relwidth=0.4, relheight=0.1)

    def clickBtnReset(self):
        self.result.ok = 0
        self.result.ng = 0
        self.result.total = 0
        self.showResult()

    def showResult(self, isOK=None):
        if self.result.date is not None:
            if self.result.date != TimeControl.ymdFormat():
                self.result.date = TimeControl.ymdFormat()
                self.result.ok = 0
                self.result.ng = 0
                self.result.total = 0
            self.dateLabel.config(text=self.result.date)
        else:
            self.result.date = TimeControl.ymdFormat()
            self.dateLabel.config(text=self.result.date)

        if isOK is None:
            pass
        elif isOK:
            self.result.ok += 1
            self.result.total += 1
        else:
            self.result.ng += 1
            self.result.total += 1

        self.okNum.config(text=self.result.ok)
        self.ngNum.config(text=self.result.ng)
        self.totalNum.config(text=self.result.total)
        self.saveInfo()

    def saveInfo(self):
        if self.side == "LEFT":
            file = JsonFile("./config/left_missing_result.json")
        else:
            file = JsonFile("./config/right_missing_result.json")
        try:
            file.data = jsonpickle.encode(self.result)
            file.saveFile()
        except:
            pass

    def getInfo(self):
        if self.side == "LEFT":
            file = JsonFile("./config/left_missing_result.json")
        else:
            file = JsonFile("./config/right_missing_result.json")
        data = file.readFile()
        try:
            self.result: ResultStruct = jsonpickle.decode(data)
            if self.result.date != TimeControl.y_m_dFormat():
                self.result = ResultStruct()
        except:
            self.result = ResultStruct()
            self.result.date = TimeControl.y_m_dFormat()

class ResultLabel(Label):

    def __init__(self, master,  text, size=14):
        Label.__init__(self, master=master, text=text, font=VisionFont.boldFont(size), fg=Color.winWhite(), bg=Color.resultBg())

class OKLabel(Label):

    def __init__(self, master,  text, size=14):
        Label.__init__(self, master=master, text=text, font=VisionFont.boldFont(size), fg=Color.okColor(), bg=Color.resultBg())

class NGLabel(Label):

    def __init__(self, master,  text, size=14):
        Label.__init__(self, master=master, text=text, font=VisionFont.boldFont(size), fg=Color.winRed(), bg=Color.resultBg())

class TotalLabel(Label):

    def __init__(self, master,  text, size=14):
        Label.__init__(self, master=master, text=text, font=VisionFont.boldFont(size), fg=Color.winYellow(), bg=Color.resultBg())