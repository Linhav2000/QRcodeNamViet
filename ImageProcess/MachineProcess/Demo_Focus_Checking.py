from ImageProcess.Algorithm.Algorithm import Algorithm
from Modules.ModelSetting.ModelParameter import ModelParameter
from Connection.Camera import Camera
from tkinter import messagebox
from ImageProcess.Algorithm.MethodList import MethodList
from Modules.ModelSetting.CAS_Type import CAS_Type
import cv2 as cv
from CommonAssit import Color
from ImageProcess import ImageProcess

class Demo_Focus_Checking:
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
            messagebox.showwarning("Start Demo", "Still not choose the algorithm")
            return  False

        if not self.currentCamera.ready:
            self.currentCamera.connect()
        # if not self.mainWindow.workingThread.connectionManager.isReady():
        #     self.mainWindow.workingThread.connectionManager.connect()

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
                    if result.methodName == MethodList.focusChecking.value:
                        if result.passed:
                            color = Color.cvGreen()
                            text = "OK    Val = {}".format(result.value)
                        else:
                            color = Color.cvRed()
                            text = "FAILED    Val = {}".format(result.value)
                    else:
                        color = Color.cvRed()
                        text = "WRONG ALGORITHM"
                cv.putText(imageShow,text=text, org=(size, imageShow.shape[0] - 2 * size),
                           fontFace=cv.FONT_HERSHEY_COMPLEX,
                           fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                           color=color,
                           thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness)
            except Exception as error:
                messagebox.showwarning("Demo Focus checking", "Detail: {}".format(error))
                self.mainWindow.runningTab.insertLog("ERROR Measure Line: {}".format(error))
        else:
            self.mainWindow.runningTab.insertLog("ERROR Demo Focus Checking: Cannot take the picture")
        self.mainWindow.showImage(imageShow)