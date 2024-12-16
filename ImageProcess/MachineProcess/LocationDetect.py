from Connection.Camera import Camera
from tkinter import messagebox
from ImageProcess.Algorithm.Algorithm import Algorithm
from Modules.ModelSetting.ModelParameter import ModelParameter
from ImageProcess.Algorithm.MethodList import MethodList
import cv2 as cv


class LocationDetect:

    camera: Camera
    algorithm: Algorithm
    currentModel: ModelParameter
    def __init__(self, mainWindow):

        self.mainWindow = mainWindow

    def updateCamera(self):
        self.camera = self.mainWindow.workingThread.cameraManager.currentCamera

    def updateModel(self):
        self.currentModel = self.mainWindow.runningTab.modelManager.getCurrentModel()
        if self.currentModel is None:
            return
        for algorithm in self.mainWindow.algorithmManager.algorithmList:
            if algorithm.algorithmParameter.name == self.currentModel.detectLocationAlgorithm:
                self.algorithm = algorithm

    def startWorking(self):
        if not self.camera.ready:
            self.camera.connect()

        return self.camera.ready

    def processDetectLocation(self, image = None):
        _image = None
        areaContour = None
        centerPoint = (0, 0)

        if image is not None:
            ret = True
            _image = image.copy()
        else:
            ret, _image = self.camera.takePicture()

        if not ret:
            messagebox.showwarning("Take image", "Please check the camera connection!\or check the camera setting!")
        else:
            try:
                ret = False
                color = (0, 0, 255)
                ret, resultList, text = self.algorithm.executeAlgorithm(_image)
                imageShow = _image.copy()
                if len(resultList) > 0:
                    for result in resultList:
                        if result.passed:
                            if result.methodName == MethodList.findContour.value:
                                ret = True
                                color = (0, 255, 0)
                                imageShow = cv.drawContours(image=imageShow, contours=result.contourList,
                                                            contourIdx=-1, color=color, thickness=5, lineType=cv.LINE_AA)
                            elif result.methodName == MethodList.getImageInsideContour.value:
                                areaContour = result.contourList
                                x0, y0, x1, y1 = result.detectAreaList[0]
                                centerPoint = (int((x0 + x1) / 2), int((y0 + y1) / 2))
                            elif result.methodName == MethodList.matchingTemplate.value:
                                ret = True
                                color = (0, 255, 0)
                                x0, y0, x1, y1 = result.detectAreaList[0]
                                centerPoint = (int((x0 + x1) / 2), int((y0 + y1) / 2))
                                imageShow = cv.rectangle(imageShow, (x0, y0), (x1, y1), color, 5)
                if ret:
                    if areaContour is not None:
                        imageShow = cv.drawContours(image=imageShow, contours=areaContour,
                                                     contourIdx=-1, color=color, thickness=5, lineType=cv.LINE_AA)
                    # for contour in area[0]:
                    #     time = TimeControl.time()
                    #     extLeft = tuple(contour[contour[:, :, 0].argmin()][0])
                    #     extRight = tuple(contour[contour[:, :, 0].argmax()][0])
                    #     extTop = tuple(contour[contour[:, :, 1].argmin()][0])
                    #     extBot = tuple(contour[contour[:, :, 1].argmax()][0])
                    #     print(  )
                    #     drawContourImage = cv.circle(drawContourImage, extLeft, 150, (0, 255, 255), -1)
                    #     drawContourImage = cv.circle(drawContourImage, extRight, 150, (0, 255, 255), -1)
                    #     drawContourImage = cv.circle(drawContourImage, extTop, 150, (0, 255, 255), -1)
                    #     drawContourImage = cv.circle(drawContourImage, extBot, 150, (0, 255, 255), -1)

                    self.mainWindow.showImage(imageShow)
                else:
                    if areaContour is not None:
                        _image = cv.drawContours(image=_image, contours=areaContour,
                                                    contourIdx=-1, color=color, thickness=5)
                    self.mainWindow.showImage(_image)

            except Exception as error:
                self.mainWindow.runningTab.insertLog("ERROR Process location detect: {}".format(error))
                return False

        return ret