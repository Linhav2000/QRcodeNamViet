from CommonAssit import VisionFont
from tkinter import messagebox
from tkinter import filedialog
import cv2 as cv
from Modules.CheckMissing.ResultStruct import ResultStruct
from View.Common.VisionUI import *

class MissingDetailFrame(LabelFrame):



    def __init__(self, master, mainWindow, title, side):
        LabelFrame.__init__(self, master=master, text=title, font=VisionFont.boldFont(10), bg=Color.resultBg(), fg=Color.winWhite())
        self.mainWindow = mainWindow
        self.side = side
        self.result = ResultStruct()
        self.setupView()
        self.showResult()



    def setupView(self):
        labelHeight = 40
        xPos = 200

        # self.dateLabel = ResultLabel(self, text="8/10/2020 - 17:30:20")
        # self.dateLabel.place(relx=0, rely=0, relwidth=1)

        self.algorithmName = ResultLabel(self, text="Algorithm  : Check missing")
        self.algorithmName.place(x=5, y=15)

        self.cameraSelected = ResultLabel(self, text="Camera      : NOT CONFIG")
        self.cameraSelected.place(x=5, y=15 + labelHeight)

        self.mainResultLabel = OKLabel(self, text="OK", size=52)
        self.mainResultLabel.place(relx=0.3, y=5 + 2*labelHeight)

        self.okLabel = OKLabel(self, text=self.mainWindow.languageManager.localized("missing_ok"))
        self.okLabel.place(x=5, y=15 + 4 * labelHeight)
        self.okNum = OKLabel(self, text="0")
        self.okNum.place(x=xPos, y=15 + 4 * labelHeight)

        self.ngLabel = NGLabel(self, text=self.mainWindow.languageManager.localized("missing_ng"))
        self.ngLabel.place(x=5, y=15 + 5 * labelHeight)
        self.ngNum = NGLabel(self, text="0")
        self.ngNum.place(x=xPos, y=15 + 5 * labelHeight)

        self.totalLabel = TotalLabel(self, text=self.mainWindow.languageManager.localized("missing_total"))
        self.totalLabel.place(x=5, y=15 + 6*labelHeight)
        self.totalNum = TotalLabel(self, text="0")
        self.totalNum.place(x=xPos, y=15 + 6 * labelHeight)

        # self.visionTimeLabel = ResultLabel(self, text=self.mainWindow.languageManager.localized("missing_visionTime"))
        # self.visionTimeLabel.place(x=5, y=15 + 6*labelHeight)
        # self.visionTime = ResultLabel(self, text="0s")
        # self.visionTime.place(x=xPos, y=15 + 6 * labelHeight)

        self.btnOpen = OpenButton(self, text="Open", command=self.clickBtnOpen, font=VisionFont.boldFont(13))
        self.btnOpen = ImageButton(self, imagePath="./resource/openFolder.png", command=self.clickBtnOpen, bg=Color.resultBg())
        self.btnOpen.place(relx=0.05, rely=0.88, relwidth=0.4, relheight=0.1)

    def clickBtnOpen(self):
        image = None
        if self.mainWindow.workingThread.runningFlag:
            messagebox.showwarning("Open existed Image", "You cannot open existed image during auto mode!")
            return
        path = filedialog.askopenfilename(title='Select Image',
                                          filetypes=(('Image files','*.jpg *.png *.ico *.bmp *.gif *.GIF *.jpeg'),('All files', '*.*')),
                                          initialdir="/áéá")
        print(path)
        try:
            image = cv.imdecode(np.fromfile(path, dtype=np.uint8), cv.IMREAD_COLOR)
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Open Old Image: {}".format(error))
            messagebox.showerror("Open Old Image", "{}".format(error))

        pathName = path[0:-4]
        pathName = str(pathName).split("/")[-1]

        self.result.date = pathName
        self.mainWindow.workingThread.rearCheckMissing.checkMissing(side=self.side, image=image)

    def showResult(self, result: ResultStruct=None):
        if result is not None:
            self.result = result
        self.mainResultLabel.place_forget()
        if self.result.ng > 0:
            self.mainResultLabel = NGLabel(self, text="NG", size=52)
            self.mainResultLabel.place(relx=0.3, y=5 + 80)
        else:
            self.mainResultLabel = OKLabel(self, text="OK", size=52)
            self.mainResultLabel.place(relx=0.3, y=5 + 80)

        # self.dateLabel.config(text=self.result.date)
        self.okNum.config(text=self.result.ok)
        self.ngNum.config(text=self.result.ng)
        self.totalNum.config(text=self.result.total)
        # try:
        #     self.visionTime.config(text="{}s".format(self.result.visionTime))
        # except:
        #     pass

    def updateAlgorithmName(self, name):
        self.algorithmName.config(text="Algorithm  : {}".format(name))

    def updateCameraSelected(self, camera):
        self.cameraSelected.config(text="Camera      : {}".format(camera))

class ResultLabel(Label):

    def __init__(self, master,  text, size=12):
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