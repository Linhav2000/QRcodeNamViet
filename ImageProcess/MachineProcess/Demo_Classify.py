from ImageProcess.Algorithm.Algorithm import Algorithm
from ImageProcess.Algorithm.MethodList import MethodList
from ImageProcess.Algorithm.AlgorithmResult import AlgorithmResult
import cv2 as cv
class Demo_Classify:

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow

    def check_ready(self):
        return True

    def execute(self, image):
        if image is None:
            return
        imageShow = image.copy()
        imageWidth = image.shape[1]
        size = int(imageWidth / 300)

        currentAlgorithm:Algorithm = self.mainWindow.algorithmManager.getCurrentAlgorithm()

        ret, result_list, text = currentAlgorithm.executeAlgorithm(image)
        result:AlgorithmResult
        if ret:
            for result in result_list:
                if result.methodName == MethodList.matchingTemplate.value:
                    if result.passed:
                        cv.putText(imageShow, text="TYPE 1", org=(size, imageShow.shape[0] - 2 * size),
                                   fontFace=cv.FONT_HERSHEY_COMPLEX,
                                   fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                                   color=(0, 255, 0),
                                   thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                   lineType=cv.LINE_AA)
                        self.mainWindow.showImage(imageShow)
                        self.mainWindow.runningTab.resultTab.classify_frame.setOK()

                    else:
                        cv.putText(imageShow, text="TYPE 2", org=(size, imageShow.shape[0] - 2 * size),
                                   fontFace=cv.FONT_HERSHEY_COMPLEX,
                                   fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                                   color=(255, 0, 255),
                                   thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                   lineType=cv.LINE_AA)
                        self.mainWindow.showImage(imageShow)
                        self.mainWindow.runningTab.resultTab.classify_frame.setNG()


