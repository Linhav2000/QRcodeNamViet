from ImageProcess.Algorithm.Algorithm import Algorithm
from Modules.ModelSetting.ModelParameter import ModelParameter
from ImageProcess.Algorithm.MethodList import *
from CommonAssit import Color
from tkinter import messagebox
import cv2 as cv


class Demo_Location:
    algorithm: Algorithm = None

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow

    def checkReady(self):
        if not self.mainWindow.workingThread.cameraManager.currentCamera.ready:
            self.mainWindow.workingThread.cameraManager.currentCamera.connect()

        self.updateModel()

        if self.algorithm is None:
            messagebox.showwarning("Algorithm config", "Please choose the algorithm for model!")
            return False

        return self.mainWindow.workingThread.cameraManager.currentCamera.ready

    def updateModel(self):
        currentModel: ModelParameter = self.mainWindow.runningTab.modelManager.getCurrentModel()
        if currentModel is None:
            return
        for algorithm in self.mainWindow.algorithmManager.algorithmList:
            if algorithm.algorithmParameter.name == currentModel.demo_location_algorithm:
                self.algorithm = algorithm

    def doProcess(self):
        ret, image = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
        color = Color.cvGreen()
        imageShow = image.copy()
        if ret:
            imageHeight = image.shape[0]
            size = int(imageHeight / 150)

            ret, resultList, text = self.algorithm.executeAlgorithm(image=image)
            for result in resultList:
                if result.methodName in LocationMethodList.list():
                    for detectArea in result.detectAreaList:
                        x1, y1, x2, y2 = detectArea
                        center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
                        text = "{}".format(center)

                        cv.putText(imageShow,text=text, org=center, fontFace=cv.FONT_HERSHEY_COMPLEX,
                                   fontScale= self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                                   color=color,
                                   thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                   lineType=cv.LINE_AA)

        else:
            self.mainWindow.runningTab.insertLog("ERROR Demo color detect: Cannot take the picture")
        self.mainWindow.showImage(imageShow)