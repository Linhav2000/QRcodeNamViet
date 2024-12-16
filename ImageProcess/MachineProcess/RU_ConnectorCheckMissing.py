import cv2 as cv
import numpy as np
from ImageProcess.Algorithm.MethodList import MethodList
from View.Common.LoadingView import LoadingView
import tkinter.messagebox as messagebox
from Modules.ModelSetting.ModelParameter import ModelParameter
from ImageProcess.Algorithm.Algorithm import Algorithm
from View.Running.ResultFrame import ResultStruct
from CommonAssit import TimeControl
from CommonAssit import PathFileControl
import threading
import os

class RU_ConnectorCheckMissing:

    designImage = None
    resultImage = None

    currentModel: ModelParameter
    screwRecognizeAlgorithm: Algorithm = None
    ringRecognizeAlgorithm: Algorithm = None
    checkingPointList = []
    result: ResultStruct
    originalImageList = []

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.initValue()

    def initValue(self):
        self.result = ResultStruct()
        self.initCheckPointList()

    def initCheckPointList(self):
        self.originalImageList = []
        self.checkingPointList = [
            [(71, 212), None, 18],
            [(176, 212), None, 19],
            [(71, 317), None, 16],
            [(176, 317), None, 17],
            [(87, 377), None, 14],
            [(213, 377), None, 15],
            [(87, 503), None, 12],
            [(213, 503), None, 13],
            [(87, 570), None, 10],
            [(213, 570), None, 11],
            [(87, 694), None, 8],
            [(213, 694), None, 9],
            [(78, 751), None, 6],
            [(169, 751), None, 7],
            [(78, 840), None, 4],
            [(169, 840), None, 5],
            [(78, 900), None, 2],
            [(169, 900), None, 3],
            [(78, 990), None, 0],
            [(169, 990), None, 1],
            [(209, 443), None, 20],
            [(209, 632), None, 21]
        ]

        self.checkingPointList.sort(key=self.pointListSort)

        for index in range(len(self.checkingPointList)):
            self.originalImageList.append(None)

    def pointListSort(self, e):
        return e[2]

    def takeImageForCheckMissing(self, plcReceive):
        try:
            position = int(float(plcReceive[8:10]))
            typePos = plcReceive[11:13]
            ret, image = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
            if ret:
                self.mainWindow.showImage(image, True)
            return self.checkMissingProcessThread(image, position, typePos)
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Take Image for check missing: {}".format(error))
            messagebox.showerror("Take Image for check missing", "{}".format(error))
            return "NG", None

    def checkMissingProcessThread(self,image, position, typePos):
        self.mainWindow.originalImage = image.copy()
        res = "OK"
        if position <= 19:
            ret, resultList, text = self.screwRecognizeAlgorithm.executeAlgorithm()
        else:
            ret, resultList, text = self.ringRecognizeAlgorithm.executeAlgorithm()

        if len(resultList) < 1:
            res = "NG"
        elif position == 21:
            res = "CR"
        else:
            res = "OK"

        for result in resultList:
            if result.passed:
                self.checkingPointList[position][1] = True
                image = cv.rectangle(image,
                                             (result.workingArea[0], result.workingArea[1]),
                                             (result.workingArea[2], result.workingArea[3]),
                                             (0, 255, 0), 3)

                if result.methodName == MethodList.houghCircle.value or result.methodName == MethodList.averageHoughCircle.value:
                    if len(result.circleList) > 0:
                        for circle in result.circleList:
                            if circle is not None:
                                cv.circle(image, (circle[0][0], circle[0][1]), circle[1], (0, 255, 0), 5)
                                cv.circle(image, (circle[0][0], circle[0][1]), 10, (0, 255, 0), -1)

                if result.methodName == MethodList.findContour.value or result.methodName == MethodList.boltHeaderDetectionWithPytorchYolo4.value:
                    for area in result.detectAreaList:
                        cv.rectangle(image, (area[0], area[1]), (area[2], area[3]), (0, 255, 0), 5)
                        center = (int((area[0] + area[2]) / 2), int((area[1] + area[3]) / 2))
                        cv.circle(image, center, 10, (0, 255, 0), -1)

                if result.methodName == MethodList.threshold.value:
                    self.mainWindow.showImage(result.drawImage)
            else:
                res = "NG"
                self.checkingPointList[position][1] = False
                image = cv.rectangle(image,
                                     (result.workingArea[0], result.workingArea[1]),
                                     (result.workingArea[2], result.workingArea[3]),
                                     (0, 0, 255), 3)

            self.mainWindow.ru_connectorImageFrame.showCurrentImage(image, position, res)
            self.originalImageList[position] = self.mainWindow.originalImage.copy()
        # for result in resultList:
        #     if not result.passed:
        #         res = "NG"
        #         color = (0, 255, 0)
        #         self.checkingPointList[position][1] = False
        #     else:
        #         color = (0, 0, 255)
        #         self.checkingPointList[position][1] = True
        #
        #     if result.drawImage is not None:
        #         self.mainWindow.ru_connectorImageFrame.showCurrentImage(result.drawImage, position, res)
        #         self.originalImageList[position] = self.mainWindow.originalImage.copy()

        self.showResult()
        return res, position

    def updateModel(self):
        # self.currentModel = self.mainWindow.runningTab.modelManager.models[self.mainWindow.runningTab.modelManager.currentModelPos]
        self.currentModel = self.mainWindow.runningTab.modelManager.getCurrentModel()
        if self.currentModel is None:
            return
        self.screwRecognizeAlgorithm = None
        for algorithm in self.mainWindow.algorithmManager.algorithmList:
            if algorithm.algorithmParameter.name == self.currentModel.screwRecognizeAlgorithm:
                self.screwRecognizeAlgorithm = algorithm

            if algorithm.algorithmParameter.name == self.currentModel.ringRecognizeAlgorithm:
                self.ringRecognizeAlgorithm = algorithm

    def showResult(self):
        nOk = 0
        nNG = 0
        for checkingPoint in self.checkingPointList:
            if checkingPoint[1] == False:
                nNG += 1
            elif checkingPoint[1] == True:
                nOk += 1

        self.result.ngTorque = nNG
        self.result.ok = nOk
        self.result.total = nOk + nNG
        self.mainWindow.runningTab.resultTab.currentResultFrame.result = self.result
        self.mainWindow.runningTab.resultTab.currentResultFrame.showResult()

    def reset(self):
        self.initCheckPointList()
        self.mainWindow.ru_connectorImageFrame.showDesignImage()


    def posFormSend(self, pos):
        valueSend = ""
        try:
            numOfPosLengthSend = 2
            realNumOfPosLength = len(str(int(pos)))
            for i in range(numOfPosLengthSend - realNumOfPosLength):
                valueSend += '0'
            valueSend = "{}{}".format(valueSend, pos)
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Number of Position Form Send: {}".format(error))
            messagebox.showerror("Number of Position Form Send", "{}".format(error))
        return valueSend

    def saveData(self):
        dataFolder = "./data/RU_Connector"
        dateFolder = "./data/RU_Connector/" + TimeControl.y_m_dFormat()
        serialFolder = dateFolder + "/" + str(self.result.serialNo) + "_" + TimeControl.H_M_SFormat()

        PathFileControl.generatePath(dataFolder)
        PathFileControl.generatePath(dateFolder)
        PathFileControl.generatePath(serialFolder)

        for index in range(len(self.originalImageList)):
            if self.originalImageList[index] is not None:
                imagPath = serialFolder + "/" + str(index) + ".png"
                cv.imencode(".png", self.originalImageList[index])[1].tofile(imagPath)
                # cv.imwrite(imagPath, self.originalImageList[index])

        self.mainWindow.runningTab.resultTab.lastResultFrame.result = self.result
        self.mainWindow.runningTab.resultTab.lastResultFrame.showResult()

    def getResult(self, path):
        if path == "" or path is None:
            return
        loadingView = LoadingView(self.mainWindow.mainFrame, self.mainWindow, text="Loading...")
        thread = threading.Thread(target=self.loadingThread, args=(path, loadingView))
        thread.start()

    def loadingThread(self, path, loadingView):
        for file in os.scandir(path):
            try:
                # imageName = list(file.split("/"))[-1]
                index = int(file.name[0:len(file.name) - 4])
                image = cv.imdecode(np.fromfile(file.path, dtype=np.uint8), cv.IMREAD_COLOR)
                self.originalImageList[index] = image.copy()
                self.checkMissingProcessThread(image, index, "OK")
            except Exception as error:
                self.mainWindow.runningTab.insertLog("ERROR Loading path file: {}".format(error))

        if len(self.mainWindow.ru_connectorImageFrame.imageList) > 0:
            self.mainWindow.ru_connectorImageFrame.showCurrentImage(imageIndex=0)
        loadingView.done()

class missingPointParameter:
    position = 0
    originalImage = None
    processImage = None
    passed = False


