from View.Common.VisionUI import *
from CommonAssit import Color
from View.MissingMachine.MissingDetailFrame import MissingDetailFrame
from View.MissingMachine.DateInfoFrame import DateInfoFrame
from View.MissingMachine.MissingDetailFrame import ResultStruct
from View.Common.ImageView import ImageView
from ImageProcess import ImageProcess
import cv2 as cv

class MissingResultFrame(Frame):

    imageView: ImageView
    missingDetailFrame: MissingDetailFrame
    dateFrame: DateInfoFrame
    side = "LEFT"

    def __init__(self, master, mainWindow, resultStrut, side):
        from View.MissingMachine.MissingMachineResultWindow import MissingMachineResultWindow
        Frame.__init__(self, master=master, bg=Color.resultBg())
        self.mainWindow = mainWindow
        self.side = side
        self.missingResultWindow: MissingMachineResultWindow = master
        self.result: ResultStruct = resultStrut
        self.setupFrame()

    def setupFrame(self):
        self.imageView = ImageView(self, self.mainWindow)
        self.imageView.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.58)

        self.missingDetailFrame = MissingDetailFrame(self, self.mainWindow, "Current Product", side=self.side)
        # self.missingDetailFrame.place(relx=0.01, rely=0.6, relwidth=0.48, relheight=0.4)

        self.dateFrame = DateInfoFrame(self, self.mainWindow, "Today information", side=self.side)
        # self.dateFrame.place(relx=0.51, rely=0.6, relwidth=0.48, relheight=0.4)

        if self.side == "LEFT":
            self.missingDetailFrame.place(relx=0.01, rely=0.6, relwidth=0.48, relheight=0.4)
            self.dateFrame.place(relx=0.51, rely=0.6, relwidth=0.33, relheight=0.4)
        else:
            self.missingDetailFrame.place(relx=0.16, rely=0.6, relwidth=0.48, relheight=0.4)
            self.dateFrame.place(relx=0.66, rely=0.6, relwidth=0.33, relheight=0.4)

    def showResult(self, result = None):
        if result is not None:
            self.result = result
        self.showImage(self.result.image)
        self.missingDetailFrame.showResult(self.result)
        if self.result.ng > 0:
            self.dateFrame.showResult(isOK=False)
        else:
            self.dateFrame.showResult(isOK=True)

    def showImage(self, image):
        if image is not None:
            self.imageView.showImage(image.copy())
        else:
            self.imageView.showImage(ImageProcess.createBlackImage())
