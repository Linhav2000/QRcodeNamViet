
import cv2 as cv
import numpy as np
from ImageProcess import ImageProcess
from CommonAssit import CommunicationReceiveAnalyze
from Modules.ModelSetting.ModelParameter import ModelParameter
from ImageProcess import ImageProcess
from Connection.Camera import Camera
from ImageProcess.Algorithm.Algorithm import Algorithm
from ImageProcess.Algorithm.MethodList import MethodList
from tkinter import messagebox

class RefInfo:
    name = ""
    image: np
    imagePosition = None
    pixelPosition = None
    realPosition = None
    plcPos = None
    def __init__(self, name):
        self.name = name

class unitInfo:
    name = ""

    def __init__(self, name):
        self.name = name
        self.ref1 = RefInfo(name)
        self.ref2 = RefInfo(name)
        self.ref3 = RefInfo(name)
        self.angle = 0

class FU_AssyAdjusting:

    currentModel: ModelParameter
    plcLengthScale = 100
    mirrorXValue = 100 # mm
    fuCamera: Camera = None
    ruCamera: Camera = None
    fuLightId = 0
    ruLightId = 1
    ruAlgorithm: Algorithm
    fuAlgorithm: Algorithm

    gripPosition = None

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow
        self.ruInfo = unitInfo("RU")
        self.fuInfo = unitInfo("FU")

    #update when change the model
    def updateModel(self):
        self.currentModel = self.mainWindow.runningTab.modelManager.getCurrentModel()
        if self.currentModel is None:
            return
        # self.currentModel = self.mainWindow.runningTab.modelManager.models[self.mainWindow.runningTab.modelManager.currentModelPos]
        for algorithm in self.mainWindow.algorithmManager.algorithmList:
            if algorithm.algorithmParameter.name == self.currentModel.ruAlgorithm:
                self.ruAlgorithm = algorithm

            if algorithm.algorithmParameter.name == self.currentModel.fuAlgorithm:
                self.fuAlgorithm = algorithm

        self.ruCamera = self.mainWindow.workingThread.cameraManager.cameraList[self.currentModel.ruCameraId]
        self.fuCamera = self.mainWindow.workingThread.cameraManager.cameraList[self.currentModel.fuCameraId]
        self.ruLightId = self.currentModel.ruLightId
        self.fuLightId = self.currentModel.fuLightId

    def startWorking(self):
        self.updateModel()
        if not self.ruCamera.ready:
            self.ruCamera.connect()
        if not self.fuCamera.ready:
            self.fuCamera.connect()
        if not self.mainWindow.workingThread.light.isOpened:
            self.mainWindow.workingThread.light.connect()
        if not self.mainWindow.workingThread.plcReadingFlag:
            self.mainWindow.workingThread.connectionManager.connect()

        ret = self.fuCamera.ready and self.ruCamera.ready and self.mainWindow.workingThread.light.isOpened
        return ret

    def isReady(self):
        try:
            return self.fuCamera.ready and self.ruCamera.ready and self.mainWindow.workingThread.light.isOpened and self.mainWindow.workingThread.plcReadingFlag
        except:
            return False

    # get the RU reference point 1, then calculate the plc for take Ru reference point 2
    def takeRuRef1Pos(self, plcRev):
        ret, image = self.ruCamera.takePicture()
        if not ret:
            return ret, None
        ret = self.takeReferenceImage(self.ruInfo.ref1, plcRev, image, self.ruAlgorithm)
        if ret:
            print("image Ru ref 1: {}".format(self.ruInfo.ref1.imagePosition))
        return ret
        if ret:
            print("image Ru ref 1: {}".format(self.ruInfo.ref1.imagePosition))
            deltaX = int(self.plcLengthScale * float(self.currentModel.ruRef2Design[0])) - int(self.plcLengthScale * float(self.currentModel.ruRef1Design[0]))
            deltaY = int(self.plcLengthScale * float(self.currentModel.ruRef2Design[1])) - int(self.plcLengthScale * float(self.currentModel.ruRef1Design[1]))

            plcPos2 = (int(float(self.currentModel.plcRuRef1Pos[0]) + deltaX),
                       int(float(self.currentModel.plcRuRef1Pos[1]) + deltaY),
                       int(float(self.currentModel.plcRuRef1Pos[2])),
                       int(float(self.currentModel.plcRuRef1Pos[3])))
            self.ruInfo.ref2_Time1.plcPos = plcPos2
            return ret, plcPos2
        else:
            return ret, None

    # get the RU reference point 2, then calculate deviation angle in Ru
    def takeRuRef2Pos(self, plcRev):
        ret, image = self.ruCamera.takePicture()
        if not ret:
            return ret, None

        ret = self.takeReferenceImage(self.ruInfo.ref2, plcRev, image, self.ruAlgorithm)
        print("image RU ref 2: {}".format(self.ruInfo.ref2.imagePosition))
        return ret

    # get the FU reference point 1, then calculate the plc for take Fu reference point 2
    def takeFuRef1Pos(self, plcRev):
        ret, image = self.fuCamera.takePicture()
        if not ret:
            return ret, None

        ret = self.takeReferenceImage(self.fuInfo.ref1, plcRev, image, self.fuAlgorithm)
        if ret:
            print("image Fu ref 1: {}".format(self.fuInfo.ref1.imagePosition))
            angle = self.findDeviationAngle()
            plcAngle = int(angle * self.plcLengthScale)
            self.fuInfo.ref3.plcPos = (self.currentModel.plcFuRef1Pos[0],
                                       self.currentModel.plcFuRef1Pos[1],
                                       self.currentModel.plcFuRef1Pos[2],
                                       self.currentModel.plcFuRef1Pos[3] + plcAngle)
            print("PLC ref 3 position: {}".format(self.fuInfo.ref3.plcPos))
        return ret
        if ret:
            print("image Fu ref 1: {}".format(self.fuInfo.ref1.imagePosition))
            deltaX = int(self.plcLengthScale * float(self.currentModel.fuRef2Design[0])) - int(self.plcLengthScale* float(self.currentModel.fuRef1Design[0]))
            deltaY = int(self.plcLengthScale * float(self.currentModel.fuRef2Design[1])) - int(self.plcLengthScale * float(self.currentModel.fuRef1Design[1]))

            plcFuRef2Pos = (int(float(self.currentModel.plcFuRef1Pos[0]) + deltaX),
                       int(float(self.currentModel.plcFuRef1Pos[1]) + deltaY),
                       int(float(self.currentModel.plcFuRef1Pos[2])))
            return ret, plcFuRef2Pos
        else:
            return ret, None


    # get the FU reference point 2 for the first time, then calculate deviation angle in Fu, then combine with the deviation in Ru -> alpha
    def takeFuRef2Pos(self, plcRev):
        ret, image = self.fuCamera.takePicture()
        if not ret:
            return ret, None
        ret = self.takeReferenceImage(self.fuInfo.ref2, plcRev, image, self.fuAlgorithm)
        print("image Fu Ref 2 time 1: {}".format(self.ruInfo.ref2.imagePosition))
        return ret

    # get the FU reference point 2 for the sencond time after rotating,
    # then calculate the deviation of X and Y axis
    def takeFuRef3Pos(self, plcRev):
        ret, image = self.fuCamera.takePicture()
        if not ret:
            return ret, None
        ret = self.takeReferenceImage(self.fuInfo.ref3, plcRev, image, self.fuAlgorithm)
        print("image Fu Ref 2 time 2: {}".format(self.fuInfo.ref3.imagePosition))
        if ret:
            ret = self.findGripPosition()
        return ret

    # take picture, then find the coordinate of reference point
    def takeReferenceImage(self, ref: RefInfo, plcRev, image, algorithm: Algorithm):
        processImage = image.copy()
        plcRevInfo = CommunicationReceiveAnalyze.getFuAssyInfo(plcRev)
        plcPos = (plcRevInfo.x, plcRevInfo.y, plcRevInfo.z, plcRevInfo.u)
        try:
            ref.image = processImage.copy()
            ref.plcPosition = plcPos
            print("PLC position: {}".format(plcPos))
            ret, circle, _ = self.getRefPosition(ref.image, algorithm)
            ref.imagePosition = circle[0]
            return ret
        except:
            print("cannot find the reference point")
        return False

    # find the coordinate of reference point into the inage
    def getRefPosition(self, _image, algorithm: Algorithm):
        if len(_image) < 1:
            return False, ((0, 0), 0), None
        image = _image.copy()
        circle = None
        processImage = None

        ret, resultList, text = algorithm.executeAlgorithm(image)
        for result in resultList:
            if result.methodName == MethodList.averageHoughCircle.value:
                if len(result.circleList) > 0:
                    circles = result.circleList
                    circle = circles[0]
                    processImage = result.drawImage
            elif result.methodName == MethodList.findContour.value:
                if len(result.detectAreaList) > 0:
                    detectArea = result.detectAreaList[0]
                    center = (int((detectArea[0] + detectArea[2]) / 2), int((detectArea[1] + detectArea[3]) / 2))
                    radius = abs(int((detectArea[0] - detectArea[2]) / 2))
                    circle = (center, radius)
                    processImage = self.mainWindow.originalImage.copy()
                    cv.circle(processImage, center, radius, (0, 255, 0), 5)
                    cv.circle(processImage, center, 5, (0, 255, 0), -1)

        self.mainWindow.showImage(image=processImage)
        if circle is None:
            return False, ((0, 0), 0), processImage
        else:
            return True, circle, processImage

    def findFUDeviationAngle(self):
        fu_pixelDesignRef1 = self.mm2PixelPoint(self.currentModel.fuRef1Design, self.currentModel.fuConversionCoef)
        fu_pixelDesignRef2 = self.mm2PixelPoint(self.currentModel.fuRef2Design, self.currentModel.fuConversionCoef)
        fu_pixelRealRef1 = self.getDeviationPointCoordinate(self.fuInfo.ref1, fu_pixelDesignRef1)
        fu_pixelRealRef2 = self.getDeviationPointCoordinate(self.fuInfo.ref2, fu_pixelDesignRef2)

        vec1 = (int(fu_pixelDesignRef2[0] - fu_pixelDesignRef1[0]), int(fu_pixelDesignRef2[1] - fu_pixelDesignRef1[1]))
        vec2 = (int(fu_pixelRealRef2[0] - fu_pixelRealRef1[0]), int(fu_pixelRealRef2[1] - fu_pixelRealRef1[1]))

        angle = ImageProcess.angleFrom2Vec(vec1, vec2)
        return angle

    def findRUDeviationAngle(self):
        ru_pixelDesignRef1 = self.mm2PixelPoint(self.currentModel.ruRef1Design, self.currentModel.ruConversionCoef)
        ru_pixelDesignRef2 = self.mm2PixelPoint(self.currentModel.ruRef2Design, self.currentModel.ruConversionCoef)
        ru_pixelRealRef1 = self.getDeviationPointCoordinate(self.fuInfo.ref1, ru_pixelDesignRef1)
        ru_pixelRealRef2 = self.getDeviationPointCoordinate(self.fuInfo.ref2, ru_pixelDesignRef2)

        vec1 = (int(ru_pixelDesignRef2[0] - ru_pixelDesignRef1[0]), int(ru_pixelDesignRef2[1] - ru_pixelDesignRef1[1]))
        vec2 = (int(ru_pixelRealRef2[0] - ru_pixelRealRef1[0]), int(ru_pixelRealRef2[1] - ru_pixelRealRef1[1]))

        angle = ImageProcess.angleFrom2Vec(vec1, vec2)
        return angle

    def findGripPosition(self):
        try:
            deviationX = (self.ruInfo.ref1.imagePosition[0] * self.currentModel.ruConversionCoef) - (self.fuInfo.ref3.imagePosition[0] * self.currentModel.fuConversionCoef)
            deviationY = (self.ruInfo.ref1.imagePosition[1] * self.currentModel.ruConversionCoef) - (self.fuInfo.ref3.imagePosition[1] * self.currentModel.fuConversionCoef)

            # fu current
            centerFuImageY = int(self.fuInfo.ref3.image.shape[0] / 2)
            centerFuImageX = int(self.fuInfo.ref3.image.shape[1] / 2)

            pixelDeltaFuX = self.fuInfo.ref3.imagePosition[0] - centerFuImageX
            pixelDeltaFuY = self.fuInfo.ref3.imagePosition[1] - centerFuImageY

            plcDeltaFuX = int(self.plcLengthScale * (pixelDeltaFuX * self.currentModel.fuConversionCoef))
            plcDeltaFuY = int(self.plcLengthScale * (pixelDeltaFuY * self.currentModel.fuConversionCoef))

            plcCurrentFuPosX = self.currentModel.plcFuRef1Pos[0] + plcDeltaFuX
            plcCurrentFuPosY = self.currentModel.plcFuRef1Pos[1] - plcDeltaFuY

            # ru current
            centerRuImageY = int(self.ruInfo.ref1.image.shape[0] / 2)
            centerRuImageX = int(self.ruInfo.ref1.image.shape[1] / 2)

            pixelDeltaRuX = self.ruInfo.ref1.imagePosition[0] - centerRuImageX
            pixelDeltaRuY = self.ruInfo.ref1.imagePosition[1] - centerRuImageY

            plcDeltaRuX = int(self.plcLengthScale * (pixelDeltaRuX * self.currentModel.ruConversionCoef))
            plcDeltaRuY = int(self.plcLengthScale * (pixelDeltaRuY * self.currentModel.ruConversionCoef))

            plcCurrentRuPosX = self.currentModel.plcRuRef1Pos[0] - plcDeltaRuX
            plcCurrentRuPosY = self.currentModel.plcRuRef1Pos[1] + plcDeltaRuY

            # ru cali
            plcCaliRuX, plcCaliRuY, plcCaliRuZ, plcCaliRuU = self.currentModel.plcRuCali
            # fu cali
            plcCaliFuX, plcCaliFuY, plcCaliFuZ, plcCaliFuU = self.currentModel.plcFuCali

            # offset point
            offsetPointX, offsetPointY, offsetPointZ = self.currentModel.offset

            #calculate
            deltaCaliRuX = plcCurrentRuPosX - plcCaliRuX
            deltaCaliRuY = plcCurrentRuPosY - plcCaliRuY

            deltaCaliFuX = plcCurrentFuPosX - plcCaliFuX
            deltaCaliFuY = plcCurrentFuPosY - plcCaliFuY

            print("delta RUX, RUY, FUX, FUY: {},{},{},{}".format(deltaCaliRuX, deltaCaliRuY, deltaCaliFuX, deltaCaliFuY))

            # gripX = self.currentModel.offset[0] + plcCurrentRuPosX + plcCurrentFuPosX
            # gripY = self.currentModel.offset[1] + plcCurrentRuPosY + plcCurrentFuPosY
            gripX = offsetPointX +  deltaCaliRuX + deltaCaliFuX
            gripY = offsetPointY + deltaCaliRuY + deltaCaliFuY

            self.gripPosition = (gripX, gripY, offsetPointZ, self.fuInfo.ref3.plcPos[3])
            return True
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Find Grip Position : {}".format(error))
            messagebox.showwarning("Find Grip Position", "{}".format(error))
            return False


    def findDeviationAngle(self):
        ru_pixelDesignRef1 = self.mm2PixelPoint(self.currentModel.ruRef1Design, self.currentModel.ruConversionCoef)
        ru_pixelDesignRef2 = self.mm2PixelPoint(self.currentModel.ruRef2Design, self.currentModel.ruConversionCoef)

        ru_pixelRealRef1 = self.getDeviationPointCoordinate(self.ruInfo.ref1, ru_pixelDesignRef1)
        ru_pixelRealRef2 = self.getDeviationPointCoordinate(self.ruInfo.ref2, ru_pixelDesignRef2)

        ru_mmRealRef1 = self.pixel2MmPoint(ru_pixelRealRef1, self.currentModel.ruConversionCoef)
        ru_mmRealRef2 = self.pixel2MmPoint(ru_pixelRealRef2, self.currentModel.ruConversionCoef)

        fu_pixelDesignRef1 = self.mm2PixelPoint(self.currentModel.fuRef1Design, self.currentModel.fuConversionCoef)
        fu_pixelDesignRef2 = self.mm2PixelPoint(self.currentModel.fuRef2Design, self.currentModel.fuConversionCoef)
        fu_pixelRealRef1 = self.getDeviationPointCoordinate(self.fuInfo.ref1, fu_pixelDesignRef1)
        fu_pixelRealRef2 = self.getDeviationPointCoordinate(self.fuInfo.ref2, fu_pixelDesignRef2)

        fu_mmRealRef1 = self.pixel2MmPoint(fu_pixelRealRef1, self.currentModel.fuConversionCoef)
        fu_mmRealRef2 = self.pixel2MmPoint(fu_pixelRealRef2, self.currentModel.fuConversionCoef)

        vec1 = (int(100 * (ru_mmRealRef2[0] - ru_mmRealRef1[0])), int(100 * (ru_mmRealRef2[1] - ru_mmRealRef1[1])))
        vec2 = (int(100 * (fu_mmRealRef2[0] - fu_mmRealRef1[0])), int(100 * (fu_mmRealRef2[1] - fu_mmRealRef1[1])))

        baseVec = [1000, 0]
        angle1 = ImageProcess.angleFrom2Vec(vec1, baseVec)
        angle2 = ImageProcess.angleFrom2Vec(vec2, baseVec)

        finalAngle = angle1 - angle2

        angle = ImageProcess.angleFrom2Vec(vec1, vec2)
        print("angle = {}".format(angle))
        print("final = {}".format(finalAngle))
        return finalAngle

    def getDeviationPointCoordinate(self, realRefInfo: RefInfo, pixelDesign):
        print("ref image position: {}".format(realRefInfo.imagePosition))
        print("name Ref: {}".format(realRefInfo.name))
        imageW = realRefInfo.image.shape[1]
        imageH = realRefInfo.image.shape[0]
        centerImageX = int(imageW / 2)
        centerImageY = int(imageH / 2)
        realRefImagePosX, RealRefImagePosY = realRefInfo.imagePosition

        pixelDeltaX = realRefImagePosX - centerImageX
        pixelDeltaY = RealRefImagePosY - centerImageY
        print("delta {}, {}".format(pixelDeltaX, pixelDeltaY))
        deviationPosX = pixelDesign[0] + pixelDeltaX
        deviationPosY = pixelDesign[1]  + pixelDeltaY

        return int(deviationPosX), int(deviationPosY)

    def mm2PixelPoint(self, point, coeff):
        x, y = point

        pixelX = int(x / float(coeff))
        pixelY = int(y / float(coeff))
        return pixelX, pixelY

    def pixel2MmPoint(self, point, coeff):
        x, y = point

        mmX = x * float(coeff)
        mmY = y * float(coeff)
        return mmX, mmY

