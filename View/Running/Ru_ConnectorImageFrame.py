from tkinter import *
import cv2 as cv
import numpy as np
from CommonAssit import CommonAssit
from CommonAssit import Color
from ImageProcess import ImageProcess
from View.Common.ImageView import ImageView
from ImageProcess.Algorithm.AlgorithmResult import AlgorithmResult
from ImageProcess.Algorithm.MethodList import MethodList

class Ru_ConnectorImageFrame(Frame):

    baseImageView: ImageView
    screwOKView: ImageView
    ringOKView: ImageView
    currentImageView: ImageView
    currentImage = None
    # listArea = []
    lastArea = None
    baseImage = cv.imdecode(np.fromfile("./resource/baseConnectorImage.png", dtype=np.uint8), cv.IMREAD_COLOR)

    imageList = []

    def __init__(self, master, mainWindow):
        from MainWindow import MainWindow
        Frame.__init__(self, master, bg='gray')
        self.mainWindow: MainWindow = mainWindow
        self.initValue()
        self.setupImageView()

    def initValue(self):
        self.imageList = []
        for index in range(22):
            self.imageList.append(None)

    def setupImageView(self):
        self.baseImageView = ImageView(self, self.mainWindow)
        self.baseImageView.place(relx=0, rely=0, relwidth=0.35, relheight=1)
        self.baseImageView.bind("<Button-1>", self.baseImageViewMouseEvent)

        self.screwOKView = ImageView(self, self.mainWindow)
        self.screwOKView.place(relx=0.35, rely=0, relwidth=0.325, relheight=0.35)

        self.ringOKView = ImageView(self, self.mainWindow)
        self.ringOKView.place(relx=0.675, rely=0, relwidth=0.325, relheight=0.35)

        self.currentImageView = ImageView(self, self.mainWindow)
        self.currentImageView.place(relx=0.35, rely=0.35, relwidth=0.65, relheight=0.65)

    def baseImageViewMouseEvent(self, event):
        chosenWidth = 40
        chosenHeight = 42
        currentArea = None
        realPosX = int(event.x * self.baseImageView.widthCoef)
        realPosY = int(event.y * self.baseImageView.heightCoef)
        inAreaFlag = False
        for index in range(len(self.mainWindow.workingThread.ru_connectorCheckMissing.checkingPointList)):
            if abs(self.mainWindow.workingThread.ru_connectorCheckMissing.checkingPointList[index][0][0] - realPosX) < chosenWidth / 2 and\
                    abs(self.mainWindow.workingThread.ru_connectorCheckMissing.checkingPointList[index][0][1] - realPosY) < chosenHeight / 2:
                currentArea = self.mainWindow.workingThread.ru_connectorCheckMissing.checkingPointList[index]
                inAreaFlag = True
                self.showCurrentImage(imageIndex=index)
                break

        if inAreaFlag and self.lastArea is not None:
            if self.lastArea[1] == False:
                color = (0, 0, 255)
            elif self.lastArea[1] == True:
                color = (0, 255, 0)
            else:
                color = Color.bgrMagenta()

            self.drawBaseImageWithArea(self.lastArea, color)

        if inAreaFlag and currentArea is not None:
            self.drawBaseImageWithArea(currentArea, (255, 255, 0))
            self.lastArea = currentArea
        self.baseImageView.showImage(self.baseImage)

    def drawBaseImageWithArea(self, area, color):
        chosenWidth = 40
        chosenHeight = 42
        cv.rectangle(self.baseImage,
                     (int(area[0][0] - chosenWidth / 2), int(area[0][1] - chosenHeight / 2)),
                     (int(area[0][0] + chosenWidth / 2),int(area[0][1] + chosenHeight / 2)),
                     color,
                     3)

        cv.putText(self.baseImage, "{}".format(area[2]),
                   (int(area[0][0] - chosenWidth / 3), int(area[0][1] + chosenHeight / 3)),
                   cv.FONT_HERSHEY_SIMPLEX,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, color,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                   lineType=cv.LINE_AA)

    def drawBaseImageWithPos(self, pos, color):
        chosenWidth = 40
        chosenHeight = 42
        cv.rectangle(self.baseImage,
                     (int(self.mainWindow.workingThread.ru_connectorCheckMissing.checkingPointList[pos][0][0] - chosenWidth / 2),
                      int(self.mainWindow.workingThread.ru_connectorCheckMissing.checkingPointList[pos][0][1] - chosenHeight / 2)),
                     (int(self.mainWindow.workingThread.ru_connectorCheckMissing.checkingPointList[pos][0][0] + chosenWidth / 2),
                      int(self.mainWindow.workingThread.ru_connectorCheckMissing.checkingPointList[pos][0][1] + chosenHeight / 2)),
                     color,
                     3)
        cv.putText(self.baseImage, "{}".format(self.mainWindow.workingThread.ru_connectorCheckMissing.checkingPointList[pos][2]),
                   (int(self.mainWindow.workingThread.ru_connectorCheckMissing.checkingPointList[pos][0][0] - chosenWidth / 3),
                    int(self.mainWindow.workingThread.ru_connectorCheckMissing.checkingPointList[pos][0][1] + chosenHeight / 3)),
                   cv.FONT_HERSHEY_SIMPLEX,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, color,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)

    def showDesignImage(self):
        chosenWidth = 40
        chosenHeight = 42
        for point in self.mainWindow.workingThread.ru_connectorCheckMissing.checkingPointList:
            cv.rectangle(self.baseImage,
                         (int(point[0][0] - chosenWidth / 2), int(point[0][1] - chosenHeight / 2)),
                         (int(point[0][0] + chosenWidth / 2), int(point[0][1] + chosenHeight / 2)),
                         Color.bgrMagenta(),
                         3)
            cv.putText(self.baseImage, "{}".format(point[2]),
                       (int(point[0][0] - chosenWidth / 3), int(point[0][1] + chosenHeight / 3)),
                       cv.FONT_HERSHEY_SIMPLEX,
                       self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, Color.bgrMagenta(),
                       self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)

        self.baseImageView.showImage(self.baseImage)

    def showOkScrewImage(self):
        image = "./resource/baseConnectorImage.png"("./resource/screwOk.png")
        self.mainWindow.originalImage = image.copy()
        ret, resultList, text = self.mainWindow.workingThread.ru_connectorCheckMissing.screwRecognizeAlgorithm.executeAlgorithm()
        result: AlgorithmResult = resultList[0]
        imageShow = result.drawImage.copy()
        cv.putText(imageShow, "Screw OK Template", (50, 150), cv.FONT_HERSHEY_SIMPLEX,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, (0, 255, 0),
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)
        if result.methodName == MethodList.matchingTemplate.value:
            detectArea = result.detectAreaList[0]
            cv.rectangle(imageShow,
                         (detectArea[0], detectArea[1]), (detectArea[2], detectArea[3]),
                         (0, 255, 0),
                         10)
        self.screwOKView.showImage(imageShow)

    def showOkRingImage(self):
        image = cv.imdecode(np.fromfile("./resource/ringOk.png", dtype=np.uint8), cv.IMREAD_COLOR)
        self.mainWindow.originalImage = image.copy()
        ret, resultList, text = self.mainWindow.workingThread.ru_connectorCheckMissing.ringRecognizeAlgorithm.executeAlgorithm()
        result: AlgorithmResult = resultList[0]
        detectArea = result.workingArea
        imageShow = result.drawImage.copy()
        if len(imageShow.shape) < 3:
            imageShow = ImageProcess.processCvtColor(imageShow, cv.COLOR_GRAY2BGR)
        cv.putText(imageShow, "O-ring OK Template", (50, 150), cv.FONT_HERSHEY_SIMPLEX,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, (0, 255, 0),
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)

        cv.rectangle(imageShow,
                     (detectArea[0], detectArea[1]),
                     (detectArea[2], detectArea[3]),
                     (0, 255, 0),
                     10)
        self.ringOKView.showImage(imageShow)

    def showCurrentImage(self, image = None, imageIndex = None, state="NG"):
        if image is not None and imageIndex is not None:
            processImage = cv.putText(image.copy(), "Current", (50, 100), cv.FONT_HERSHEY_SIMPLEX,
                                      self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                                      (255, 255, 0),
                                      self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                      lineType=cv.LINE_AA)
            self.currentImage = processImage
            self.imageList[imageIndex] = processImage
            self.currentImageView.showImage(image)
            if state == "NG":
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)

            self.drawBaseImageWithPos(imageIndex, color)
            self.baseImageView.showImage(self.baseImage)
        elif image is not None and imageIndex is None:
            self.currentImageView.showImage(image)
        elif self.imageList[imageIndex] is not None:
            self.currentImageView.showImage(self.imageList[imageIndex])
        else:
            self.currentImageView.showImage(ImageProcess.createBlackImage())

    def hide(self):
        self.place_forget()

    def show(self):
        self.place(x=0, y=0, relwidth=1, relheight=1)