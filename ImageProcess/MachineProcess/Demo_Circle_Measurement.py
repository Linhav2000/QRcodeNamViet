from ImageProcess.Algorithm.Algorithm import Algorithm, AlgorithmResult
from Modules.ModelSetting.ModelParameter import ModelParameter
from Connection.Camera import Camera
from tkinter import messagebox
from ImageProcess.Algorithm.MethodList import MethodList
from Modules.ModelSetting.CAS_Type import CAS_Type
import cv2 as cv
from CommonAssit import Color
from ImageProcess import ImageProcess


class Demo_Circle_Measurement:
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

        # ret = self.currentCamera.ready
        return True

    def isConnected(self):
        ret = self.currentCamera.ready and self.mainWindow.workingThread.connectionManager.isConnected()

    def doProcess(self):
        if self.currentCamera.ready:
            ret, image = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
        else:
            if self.mainWindow.originalImage.copy() is not None:
                image = self.mainWindow.originalImage.copy()
                ret = True
            else:
                ret = False
                image = None
        imageShow = image.copy()
        text = "FAILED"
        color = Color.cvRed()

        if ret:
            try:
                current_as = self.mainWindow.as_manager.getCurrentAS()

                imageWidth = image.shape[1]
                size = int(imageWidth / 300)

                ret, resultList, text = self.algorithm.executeAlgorithm(image=image)
                result: AlgorithmResult
                for result in resultList:
                    if result.methodName == MethodList.findContour.value:
                        if result.passed:
                            color = Color.cvGreen()
                            x1, y1, x2, y2 = result.detectAreaList[0]
                            center = (int((x1 + x2) / 2), int((y1 + y2) / 2))

                            pixel_radius = ((x2 - x1) + (y2 - y1)) / 4
                            mm_radius = pixel_radius * current_as.robot_pixel_mm_Scale
                            text = "Center = {}, R = {} mm".format(center, mm_radius)
                            imageShow = cv.drawContours(imageShow, result.contourList, -1, color, int(size/2))
                        else:
                            color = Color.cvRed()
                            text = "FAILED"

                if mm_radius > 17.5:
                    cv.putText(imageShow,text=text, org=(size, imageShow.shape[0] - 2 * size),
                               fontFace=cv.FONT_HERSHEY_COMPLEX,
                               fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                               color=color,
                               thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                               lineType=cv.LINE_AA)
                else:
                    cv.putText(imageShow, text=text, org=(size, imageShow.shape[0] - 2 * size),
                               fontFace=cv.FONT_HERSHEY_COMPLEX,
                               fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                               color=(0, 0, 255),
                               thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                               lineType=cv.LINE_AA)
            except Exception as error:
                messagebox.showwarning("Circle measurement", "Cannot measure Circle\nDetail: {}".format(error))
                self.mainWindow.runningTab.insertLog("ERROR Measure Line: {}".format(error))
        else:
            self.mainWindow.runningTab.insertLog("ERROR Demo circle measurement: Cannot take the picture")
        self.mainWindow.showImage(imageShow)