import cv2 as cv
import numpy as np
from ImageProcess import ImageProcess
from ImageProcess.Algorithm import StepParamter
from ImageProcess.Algorithm.Algorithm import Algorithm
from Connection.Camera import Camera
from Modules.ModelSetting.ModelParameter import ModelParameter
from tkinter import messagebox
from ImageProcess.Algorithm.MethodList import MethodList
from Modules.CheckMissing.ResultStruct import ResultStruct
from CommonAssit import TimeControl
from CommonAssit import PathFileControl, CommonAssit

import math
from View.MissingMachine.MissingMachineResultWindow import MissingMachineResultWindow


class RearCheckMissing:
    cameraLeft: Camera = None
    cameraRight: Camera = None
    leftAlgorithm: Algorithm = None
    rightAlgorithm: Algorithm = None
    currentModel: ModelParameter

    leftResult: ResultStruct
    rightResult: ResultStruct

    leftDataPath = "./data/Rear Missing"
    rightDataPath = "./data/Rear Missing"

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow
        self.initValue()

    def initValue(self):
        self.rightResult = ResultStruct()
        self.leftResult = ResultStruct()

    def updateModel(self):
        # self.currentModel = self.mainWindow.runningTab.modelManager.models[self.mainWindow.runningTab.modelManager.currentModelPos]
        self.currentModel = self.mainWindow.runningTab.modelManager.getCurrentModel()
        if self.currentModel is None:
            return
        for algorithm in self.mainWindow.algorithmManager.algorithmList:
            if algorithm.algorithmParameter.name == self.currentModel.leftAlgorithm:
                self.leftAlgorithm = algorithm

            if algorithm.algorithmParameter.name == self.currentModel.rightAlgorithm:
                self.rightAlgorithm = algorithm

        self.cameraLeft = self.mainWindow.workingThread.cameraManager.cameraList[self.currentModel.leftCameraId]
        self.cameraRight = self.mainWindow.workingThread.cameraManager.cameraList[self.currentModel.rightCameraId]

    def startWorking(self):
        if not self.cameraLeft.ready:
            self.cameraLeft.connect()
        if not self.cameraRight.ready:
            self.cameraRight.connect()

        ret = self.cameraRight.ready and self.cameraLeft.ready
        return ret

    def checkMissing(self, side, image):
        if side == "LEFT":
            self.checkLeftImage(image=image)
        else:
            self.checkRightImage(image=image)

    def checkLeftImage(self, image = None):
        drawImage = None
        nOK = 0
        nNG = 0

        if image is None:
            if self.cameraLeft is not None and self.cameraLeft.ready:
                ret, leftImage = self.cameraLeft.takePicture()
            else:
                messagebox.showwarning("Check left image", "Left camera still not connected or not ready for take picture!")
                ret = False
                leftImage = None
        else:
            leftImage = image.copy()
        ret = False
        if self.leftAlgorithm is not None:
            color = (0, 255, 0)
            if leftImage is not None:
                drawImage = leftImage.copy()
                try:
                    ret, resultList, text = self.leftAlgorithm.executeAlgorithm(image=leftImage, camera=self.cameraLeft, imageName="LEFT")
                    print("execute done")

                    for result in resultList:
                        if result.passed:
                            print("pass")
                            color = (0, 255, 0)
                            nOK += 1
                            drawImage = cv.rectangle(drawImage,
                                                       (result.workingArea[0], result.workingArea[1]),
                                                       (result.workingArea[2], result.workingArea[3]),
                                                       (0, 255, 0), math.ceil(self.cameraLeft.parameter.textScale))
                            print("draw ok rec")

                            if result.methodName == MethodList.houghCircle.value or result.methodName == MethodList.averageHoughCircle.value:
                                if len(result.circleList) > 0:
                                    for circle in result.circleList:
                                        if circle is not None:
                                            cv.circle(drawImage, (circle[0][0], circle[0][1]), circle[1],
                                                      (0, 255, 0), 5)
                                            cv.circle(drawImage, (circle[0][0], circle[0][1]), 10, (0, 255, 0),
                                                      -1)
                        else:
                            print("draw NG rec")

                            color = (0, 0, 255)
                            drawImage = cv.rectangle(drawImage,
                                                       (result.workingArea[0], result.workingArea[1]),
                                                       (result.workingArea[2], result.workingArea[3]),
                                                       (0, 0, 255), math.ceil(self.cameraLeft.parameter.textScale))
                            nNG += 1
                            print("draw OK rec")

                        drawImage = cv.putText(drawImage,"{}".format(result.stepId),
                                               (result.workingArea[0], result.workingArea[1] - int(self.cameraLeft.parameter.textThickness)),
                                               cv.FONT_HERSHEY_SIMPLEX,
                                               self.cameraLeft.parameter.textScale,
                                               color,
                                               self.cameraLeft.parameter.textThickness, lineType=cv.LINE_AA)
                        print("draw text rec")

                except Exception as error:
                    self.mainWindow.runningTab.insertLog("ERROR Check Left Image: {}".format(error))
                    messagebox.showwarning("Check Left Image", "{}".format(error))
                self.leftResult.image = drawImage
                self.leftResult.ok = nOK
                self.leftResult.ng = nNG
                self.leftResult.total = nNG + nOK
                self.mainWindow.checkMissingWindow.leftFrame.showResult()
                if self.leftResult.ng > 0:
                    ret = False
                else:
                    ret = True

        # ret, resultList, text = self.leftAlgorithm.executeAlgorithm(leftImage)
        # if ret:
            # self.mainWindow.checkMissingWindow.leftFrame.showImage(leftImage)
        return ret, drawImage

    def checkRightImage(self, image=None):
        drawImage = None
        nOK = 0
        nNG = 0

        if image is None:
            if self.cameraRight is not None and self.cameraRight.ready:
                ret, rightImage = self.cameraRight.takePicture()
            else:
                messagebox.showwarning("Check right image",
                                       "Right camera still not connected or not ready for take picture!")
                ret = False
                rightImage = None
        else:
            rightImage = image.copy()
        ret = False
        if self.rightAlgorithm is not None:
            color = (0, 255, 0)

            if rightImage is not None:
                drawImage = rightImage.copy()
                try:
                    ret, resultList, text = self.rightAlgorithm.executeAlgorithm(image=rightImage, camera=self.cameraRight, imageName="RIGHT")
                    for result in resultList:
                        if result.passed:
                            color = (0, 255, 0)
                            nOK += 1
                            drawImage = cv.rectangle(drawImage,
                                                     (result.workingArea[0], result.workingArea[1]),
                                                     (result.workingArea[2], result.workingArea[3]),
                                                     (0, 255, 0), math.ceil(self.cameraRight.parameter.textScale))

                            if result.methodName == MethodList.houghCircle.value or result.methodName == MethodList.averageHoughCircle.value:
                                if len(result.circleList) > 0:
                                    for circle in result.circleList:
                                        if circle is not None:
                                            cv.circle(drawImage, (circle[0][0], circle[0][1]), circle[1],
                                                      (0, 255, 0), 5)
                                            cv.circle(drawImage, (circle[0][0], circle[0][1]), 10, (0, 255, 0),
                                                      -1)
                        else:
                            color = (0, 0, 255)
                            drawImage = cv.rectangle(drawImage,
                                                     (result.workingArea[0], result.workingArea[1]),
                                                     (result.workingArea[2], result.workingArea[3]),
                                                     (0, 0, 255), math.ceil(self.cameraRight.parameter.textScale))
                            nNG += 1

                        drawImage = cv.putText(drawImage, "{}".format(result.stepId),
                                               (result.workingArea[0], result.workingArea[1] - int(self.cameraRight.parameter.textThickness)), cv.FONT_HERSHEY_SIMPLEX,
                                               self.cameraRight.parameter.textScale,
                                               color,
                                               self.cameraRight.parameter.textThickness, lineType=cv.LINE_AA)

                except Exception as error:
                    self.mainWindow.runningTab.insertLog("ERROR Check Right Image: {}".format(error))
                    messagebox.showwarning("Check Right Image", "{}".format(error))
                self.rightResult.image = drawImage
                self.rightResult.ok = nOK
                self.rightResult.ng = nNG
                self.rightResult.total = nNG + nOK
                self.mainWindow.checkMissingWindow.rightFrame.showResult()
                if self.rightResult.ng > 0:
                    ret = False
                else:
                    ret = True

        return ret, drawImage

    def showResult(self):


        return

    def saveLeftImage(self, image):
        if self.leftDataPath == "./data/Rear Missing":
            dataPath = "./data"
            rearMissingPath = "./data/Rear Missing"
            leftDataPath = "./data/Rear Missing/Left"
            datePath = leftDataPath + "/" + TimeControl.y_m_dFormat()

            PathFileControl.generatePath(dataPath)
            PathFileControl.generatePath(rearMissingPath)
            PathFileControl.generatePath(leftDataPath)
        else:
            leftDataPath = self.leftDataPath
            datePath = leftDataPath + "/" + TimeControl.y_m_dFormat()

        try:
            PathFileControl.generatePath(datePath)
            imagePath = datePath + "/" + TimeControl.H_M_SFormat() + ".jpg"
            cv.imencode(".jpg", image)[1].tofile(imagePath)
            # cv.imwrite(filename=imagePath, img=image)
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Left Image: {}".format(error))
            messagebox.showerror("Save Left Image", "{}".format(error))

    def saveRightImage(self, image):
        if self.rightDataPath == "./data/Rear Missing":
            dataPath = "./data"
            rearMissingPath = "./data/Rear Missing"
            rightDataPath = "./data/Rear Missing/Right"
            datePath = rightDataPath + "/" + TimeControl.y_m_d_H_M_S_format()

            PathFileControl.generatePath(dataPath)
            PathFileControl.generatePath(rearMissingPath)
            PathFileControl.generatePath(rightDataPath)
        else:
            rightDataPath = self.rightDataPath
            datePath = rightDataPath + "/" + TimeControl.y_m_dFormat()

        try:
            PathFileControl.generatePath(datePath)
            imagePath = datePath + "/" + TimeControl.y_m_d_H_M_S_format() + ".jpg"
            cv.imencode(".jpg", image)[1].tofile(imagePath)
            # cv.imwrite(filename=imagePath, img=image)
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Right Image: {}".format(error))
            messagebox.showerror("Save Right Image", "{}".format(error))
    def saveData(self, image, path):
        imageType, imagePath = CommonAssit.getImageTypeFromName(path)
        cv.imencode(imageType, image)[1].tofile(imagePath)
        # cv.imwrite(path, image)

    def getDate(self):
        return