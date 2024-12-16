from ImageProcess.Algorithm.Algorithm import Algorithm
from Modules.ModelSetting.ModelParameter import ModelParameter
from ImageProcess.Algorithm.MethodList import MethodList
from CommonAssit import Color
from tkinter import messagebox
import cv2 as cv

class Demo_Color_Detect:
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
            if algorithm.algorithmParameter.name == currentModel.demo_color_detect_algorithm:
                self.algorithm = algorithm


    def doProcess(self, image=None):
        ret = True
        if image is None:
            ret, image = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
        imageShow = image.copy()
        text = "FAILED : 0"
        color = Color.cvRed()

        if ret:
            imageWidth = image.shape[1]
            size = int(imageWidth / 150)

            ret, resultList, text = self.algorithm.executeAlgorithm(image=image)
            for result in resultList:
                if result.methodName == MethodList.bgr_hlsRange.value \
                    or result.methodName == MethodList.bgr_hsvRange.value \
                    or result.methodName == MethodList.bgrInRange.value \
                    or result.methodName == MethodList.hsv_hlsRange.value \
                    or result.methodName == MethodList.hsvInRange.value \
                    or result.methodName == MethodList.hlsInRange.value \
                    or result.methodName == MethodList.countNonzero.value \
                    or result.methodName == MethodList.colorDetect.value:

                    if result.passed:
                        color = Color.cvGreen()
                        text = "Pass : {}".format(result.value)
                    else:
                        color = Color.cvRed()
                        text = "FAILED : {}".format(result.value)


            cv.putText(imageShow,text=text, org=(size, imageShow.shape[0] - 2 * size),
                       fontFace=cv.FONT_HERSHEY_COMPLEX,
                       fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                       color=color,
                       thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)

        else:
            self.mainWindow.runningTab.insertLog("ERROR Demo color detect: Cannot take the picture")
        self.mainWindow.showImage(imageShow)
