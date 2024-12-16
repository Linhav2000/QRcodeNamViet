from CommonAssit import TimeControl
from CommonAssit import PathFileControl
from CommonAssit.FileManager import *
from Modules.CheckMissing.ResultStruct import ResultStruct
from CommonAssit.FileManager import JsonFile
import jsonpickle
from View.Common.VisionUI import *
from View.Common.Clock import Clock
import cv2 as cv


class ResultLabel(Label):

    def __init__(self, master,  text, size=14):
        Label.__init__(self, master=master, text=text, font=VisionFont.boldFont(size), fg=Color.winWhite(), bg=Color.resultBg())

class OKLabel(Label):

    def __init__(self, master,  text, size=20):
        Label.__init__(self, master=master, text=text, font=VisionFont.boldFont(size), fg=Color.okColor(), bg=Color.resultBg())

class NGLabel(Label):

    def __init__(self, master,  text, size=14):
        Label.__init__(self, master=master, text=text, font=VisionFont.boldFont(size), fg=Color.winRed(), bg=Color.resultBg())

class TotalLabel(Label):

    def __init__(self, master,  text, size=14):
        Label.__init__(self, master=master, text=text, font=VisionFont.boldFont(size), fg=Color.winYellow(), bg=Color.resultBg())


class Counting_In_Conveyor_Result_Frame(LabelFrame):

    countingLabel: OKLabel
    dateLabel: ResultLabel
    countingNum: OKLabel
    btnReset: ResetButton

    def __init__(self, master, mainWindow, title):
        from MainWindow import MainWindow
        LabelFrame.__init__(self, master=master, text=title, font=VisionFont.boldFont(10), bg=Color.resultBg(), fg=Color.winWhite())
        self.mainWindow: MainWindow = mainWindow
        self.result = ResultStruct()
        self.getInfo()
        self.setupView()
        self.showResult()


    def setupView(self):
        labelHeight = 40
        xPos = 150
        # Clock
        self.clock = Clock(self)
        self.clock.place(relx=0, rely=0.01, relwidth=1)
        self.clock.config(font=VisionFont.regularFont(16), fg=Color.winWhite(), anchor="center", bg=Color.resultBg())
        self.clock.start()

        # self.dateLabel = ResultLabel(self, text=TimeControl.ymdFormat())
        # self.dateLabel.place(relx=0, rely=0, relwidth=1)

        self.countingLabel = OKLabel(self, text="Count :")
        self.countingLabel.place(x=5, y=15 + 1 * labelHeight)
        self.countingNum = OKLabel(self, text="0")
        self.countingNum.place(x=xPos, y=15 + 1 * labelHeight)

        self.one_click_save_image = VisionButton(self, font=VisionFont.boldFont(14), text="One click save", command=self.click_one_click_save_image)
        self.one_click_save_image.place(x=5, y=15 + 4 * labelHeight, width=200, height=60)

        self.btnReset = ResetButton(self, command=self.clickBtnReset, bg=Color.resultBg())
        self.btnReset.place(relx=0.05, rely=0.88, relwidth=0.4, relheight=0.1)


    def clickBtnReset(self):
        file = TextFile("./resource/control.txt")
        file.dataList = ["reset"]
        file.saveFile()
        return
        self.mainWindow.workingThread.counting_in_conveyor.save()
        self.showResult()

    def click_one_click_save_image(self):
        save_image_dir = "./Save_image"
        image_path = f"./Save_image/{TimeControl.time()}.bmp"

        PathFileControl.generatePath(save_image_dir)
        if self.mainWindow.workingThread.captureVideoFlag:
            if self.mainWindow.originalImage is None:
                self.mainWindow.runningTab.insertLog("ERROR The original image is empty")
            cv.imencode(".bmp", self.mainWindow.originalImage)[1].tofile(image_path)
            # cv.imwrite(filename=image_path, img=self.mainWindow.originalImage)
        else:
            ret, image = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
            if ret:
                self.mainWindow.showImage(image, original=True)
                cv.imencode(".bmp", self.mainWindow.originalImage)[1].tofile(image_path)
                # cv.imwrite(filename=image_path, img=self.mainWindow.originalImage)
            else:
                self.mainWindow.runningTab.insertLog("ERROR Cannot take image. Please check camera")

    def showResult(self, count=0):
        self.countingNum.config(text=count)

    def saveInfo(self):
        file = JsonFile("./config/coconut_counting_result.json")
        try:
            file.data = jsonpickle.encode(self.result)
            file.saveFile()
        except:
            pass

    def getInfo(self):
        file = JsonFile("./config/coconut_counting_result.json")
        data = file.readFile()
        try:
            self.result: ResultStruct = jsonpickle.decode(data)
            if self.result.date != TimeControl.y_m_dFormat():
                self.result = ResultStruct()
        except:
            self.result = ResultStruct()
            self.result.date = TimeControl.y_m_dFormat()
