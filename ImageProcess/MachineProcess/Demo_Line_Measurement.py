from ImageProcess.Algorithm.Algorithm import Algorithm
from Modules.ModelSetting.ModelParameter import ModelParameter
from Connection.Camera import Camera
from tkinter import messagebox
from ImageProcess.Algorithm.MethodList import MethodList
from Modules.ModelSetting.CAS_Type import CAS_Type
from CommonAssit import Color
from ImageProcess import ImageProcess

import cv2 as cv

class Demo_Line_Measurement:
    algorithm: Algorithm = None
    currentModel: ModelParameter
    currentCamera: Camera

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def updateModel(self):
        # self.currentModel = self.mainWindow.runningTab.modelManager.models[self.mainWindow.runningTab.modelManager.currentModelPos]
        self.currentModel = self.mainWindow.runningTab.modelManager.getCurrentModel()
        if self.currentModel is None:
            return
        for algorithm in self.mainWindow.algorithmManager.algorithmList:
            if algorithm.algorithmParameter.name == self.currentModel.rotoAlgorithmStep0:
                self.algorithm = algorithm

        self.currentCamera = self.mainWindow.workingThread.cameraManager.currentCamera

    def startWorking(self):
        self.updateModel()
        if self.algorithm is None:
            messagebox.showwarning("Start Roto Weighing robot", "Still not choose the algorithm")
            return  False

        if not self.currentCamera.ready:
            self.currentCamera.connect()
        ret = self.currentCamera.ready
        return ret

    def isConnected(self):
        ret = self.currentCamera.ready and self.mainWindow.workingThread.connectionManager.isConnected()
        return ret

    def doProcess(self):
        ret, image = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
        imageShow = image.copy()
        text = "FAILED"
        color = Color.cvRed()

        if ret:
            try:
                imageWidth = image.shape[1]
                size = int(imageWidth / 250)

                ret, resultList, text = self.algorithm.executeAlgorithm(image=image)
                for result in resultList:
                    if result.methodName == MethodList.findContour.value:
                        if result.passed:
                            color = Color.cvGreen()
                            contour = result.contourList[0]

                            extTop, extRight, extBot, extLeft = ImageProcess.processFindExtremeOfContour(contour=contour)
                            pixelDistance1 = ImageProcess.calculateDistanceBy2Points(extTop, extRight)
                            pixelDistance2 = ImageProcess.calculateDistanceBy2Points(extTop, extLeft)

                            pixelDistance = pixelDistance1 if pixelDistance1 > pixelDistance2 else pixelDistance2

                            mmDistance = pixelDistance * self.currentModel.robot_pixel_mm_Scale_1
                            text = "Result = {} mm".format(mmDistance)
                        else:
                            color = Color.cvRed()
                            text = "FAILED"


                cv.putText(imageShow,text=text, org=(size, imageShow.shape[0] - 2 * size),
                           fontFace=cv.FONT_HERSHEY_COMPLEX,
                           fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                           color=color,
                           thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                           lineType=cv.LINE_AA)
            except Exception as error:
                messagebox.showwarning("Measure Line", "Cannot measure line\nDetail: {}".format(error))
                self.mainWindow.runningTab.insertLog("ERROR Measure Line: {}".format(error))
        else:
            self.mainWindow.runningTab.insertLog("ERROR Demo line measurement: Cannot take the picture")
        self.mainWindow.showImage(imageShow)
