from ImageProcess import ImageProcess
from CommonAssit.FileManager import CsvFile
import tkinter.messagebox as messagebox
import cv2 as cv
import numpy as np
from Modules.ModelSetting.ModelParameter import ModelParameter
from View.ModelSetting.ModelSettingTab import NumOfRefPoint
import CommonAssit.TimeControl as TimeControl
import CommonAssit.PathFileControl as PathFileControl
from View.ModelSetting.ActivePointAdvanceSettingView import PointActivatedState
import CommonAssit.CommonAssit as CommonAssit
from CommonAssit import CommunicationReceiveAnalyze
from ImageProcess.Algorithm.Algorithm import Algorithm

import os
import enum

class RefInfo:
    plcPosition = ()
    imagePosition = ()
    image: np
    realRefPosition = ()

class PositionState(enum.Enum):
    NG = "NG"
    OK = "OK"
    NH = "NH"

class AdjustingScrewPosition:

    realRefPoints = []
    realPixelScrewCoordinates = []
    realMillimeterScrewCoordinates = []
    realMachineScrewCoordinates = []

    originalPositions = []
    designPositions = []
    designRefPoints = []
    pixelDesignPoints = []
    realPLCPoints = []
    realActivePLCPoint = []
    activeOriginalPositions = []

    currentModel: ModelParameter
    maxNumberOfPos = 0
    modelName = ""
    serialNo = "0000-0000-0000"
    holeCenterAlgorithm: Algorithm

    ref1:RefInfo

    # For showing process
    transferringImageIndex = 0
    designPosImage: np
    processImage: np


    newProcessFlag = False
    numOfNgToque = 0
    numOfOk = 0
    numOfNgHeight = 0
    numOfTotal = 0

    startingTime = 0
    refTime = 0

    xCoefficient = 1
    yCoefficient = 1

    mirrorXValue = 100 # mm
    plcLengthScale = 1000

    def __init__(self, camera, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow
        self.camera = camera
        self.ref1 = RefInfo()
        self.ref2 = RefInfo()
        self.ref3 = RefInfo()

        self.processImage = ImageProcess.createBlackImage()

    def getDesignPositions(self):
        self.pixelDesignPoints.clear()
        self.originalPositions.clear()
        self.designPositions.clear()
        self.realPLCPoints.clear()
        self.realActivePLCPoint.clear()
        self.activeOriginalPositions.clear()
        self.currentModel = self.mainWindow.runningTab.modelManager.getCurrentModel()
        if self.currentModel is None:
            return
        # self.currentModel = self.mainWindow.runningTab.modelManager.models[self.mainWindow.runningTab.modelManager.currentModelPos]
        self.modelName = self.currentModel.name

        designPointsFile = CsvFile(self.currentModel.designFilePath)
        designPointsFile.readFile()

        for point in designPointsFile.dataList:
            x = point[0]
            y = point[1]
            try:
                _x = float(x)
                _y = float(y)

                self.originalPositions.append((_x, _y))

                pixelX = int(_x / float(self.currentModel.conversionCoef))
                pixelY = int(_y / float(self.currentModel.conversionCoef))

                self.pixelDesignPoints.append((pixelX, pixelY))

                _x = int(_x * self.plcLengthScale)
                _y = int(_y * self.plcLengthScale)
                self.designPositions.append((_x, _y))
            except:
                pass

        self.maxNumberOfPos = len(self.designPositions)
        if (int(self.currentModel.activeTo) + 1) > self.maxNumberOfPos:
            messagebox.showerror("Design Position", "the setting active position to is greater than max number of design position!")

        for algorithm in self.mainWindow.algorithmManager.algorithmList:
            if algorithm.algorithmParameter.name == self.currentModel.centerHoleAlgorithm:
                self.holeCenterAlgorithm = algorithm

    def convertToMirrorAxis(self, point):
        mirrorXPoint = None
        x, y = point
        mirrorX = self.mirrorXValue - x

        mirrorXPoint = (mirrorX, y)

        return mirrorXPoint

    def takeReferenceImage(self, ref: RefInfo, plcRev):
        plcRevInfo = CommunicationReceiveAnalyze.getRuConnectorInfo(plcRev)
        plcPos = (plcRevInfo.x, plcRevInfo.y)
        try:
            ret, image = self.camera.takePicture()
            if ret:
                ref.image = image
                ref.plcPosition = plcPos
                print("PLC position: {}".format(plcPos))
                ret, circle, _ = self.getRefPosition(ref.image)
                ref.imagePosition = circle[0]
                return ret
        except:
            pass
        return False

    def getRefPosition(self, _image):
        if len(_image) < 1:
            return False, ((0, 0), 0), None
        shape = _image.shape
        image = _image.copy()

        ret, resultList, text = self.holeCenterAlgorithm.executeAlgorithm(image)
        result = resultList[0]
        circles = result.circleList
        processImage = result.drawImage
        circle = circles[0]

        if len(circles) <= 0:
            return False, ((0, 0), 0), processImage
        else:
            return True, circle, processImage
        
        if self.currentModel.screwRecognizeAlgorithm == "Hough circles":
            processImage, circles = ImageProcess.processHoughCircle(image,
                                                                    minDist=self.currentModel.minDist,
                                                                    param1=self.currentModel.parm1,
                                                                    param2=self.currentModel.parm2,
                                                                    minRadius=self.currentModel.boltRadius - 31,
                                                                    maxRadius=self.currentModel.boltRadius + 33)
            emurateCircleX = 0
            emurateCircleY = 0
            emurateCircleR = 0
            for circle in circles:
                emurateCircleX += circle[0]
                emurateCircleY += circle[1]
                emurateCircleR += circle[2]
            circle = None
            if len(circles) > 0:
                circle = (int(emurateCircleX / len(circles)), int(emurateCircleY / len(circles)), int(emurateCircleR / len(circles)))
                cv.circle(image, (circle[0], circle[1]), circle[2], (0, 255, 0), 5)
                cv.circle(image, (circle[0], circle[1]), 10, (0, 255, 0), -1)
            self.mainWindow.showImage(image)

            if len(circles) <= 0:
                return False, ((0, 0), 0), processImage
            else:
                return True, ((int(circle[0]), int(circle[1])), int(circle[2])), processImage
        elif self.currentModel.screwRecognizeAlgorithm == "Contours":
            if len(shape) > 2:
                image = cv.cvtColor(_image, cv.COLOR_BGR2GRAY)
            _, thresh = cv.threshold(image, int(self.currentModel.threshValue), 255, cv.THRESH_BINARY)

            kernel = np.ones((3, 3), np.uint8)
            dilateImage = cv.dilate(thresh, kernel, iterations=3)

            erodeImage = cv.erode(dilateImage, kernel, iterations=3)

            blurImage = cv.medianBlur(erodeImage, 3)
            ret, thresh2 = cv.threshold(blurImage, int(self.currentModel.threshValue), 255, cv.THRESH_BINARY)
            contours, _ = cv.findContours(thresh2, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

            showImage = cv.cvtColor(thresh2, cv.COLOR_GRAY2BGR)
            retImage = showImage.copy()
            global center
            center = (0,0)
            isRefDetected = False
            Refw = 0
            for contour in contours:

                area = cv.contourArea(contour)
                x, y, w, h = cv.boundingRect(contour)
                print("ref area: {}".format(area))
                print("x, y, w, h: {}".format((x, y, w, h)))

                self.mainWindow.runningTab.insertLog("ref area: {}".format(area))
                self.mainWindow.runningTab.insertLog("x, y, w, h: {}".format((x, y, w, h)))
                # if 45000 < area < 75000:
                #     cv.circle(showImage, center, int(w / 2), (0, 255, 0), 3)
                #     cv.circle(showImage, center, 3, (255, 0, 0), -1)
                #     isRefDetected = True
                #     break
                #
                if 180 < w < 300 and 180 < h < 300:
                    center = (int(x + w / 2), int(y + h / 2))
                    # cv.circle(showImage, center, int(w / 2), (0, 255, 0), 3)
                    # cv.circle(showImage, center, 3, (255, 0, 0), -1)
                    isRefDetected = True
                    Refw = w
                    # break
            cv.circle(showImage, center, int(Refw / 2), (0, 255, 0), 5)
            cv.circle(showImage, center, 10, (255, 0, 0), -1)
            circle = (center, int(Refw / 2))
            self.mainWindow.showImage(showImage)
            return isRefDetected, circle, retImage

    def takeRefImage1(self, plcRev):
        # model = self.mainWindow.runningTab.modelManager.models[self.mainWindow.runningTab.modelManager.currentModelPos]
        ret = self.takeReferenceImage(self.ref1, plcRev)
        print("image pos 1: {}".format(self.ref1.imagePosition))

        mirrorRefPoint1 = self.convertToMirrorAxis(self.currentModel.refPoint1)
        mirrorRefPoint2 = self.convertToMirrorAxis(self.currentModel.refPoint2)

        deltaX = int(self.plcLengthScale * float(mirrorRefPoint2[0])) - int(self.plcLengthScale * float(mirrorRefPoint1[0]))
        deltaY = int(self.plcLengthScale * float(mirrorRefPoint2[1])) - int(self.plcLengthScale * float(mirrorRefPoint1[1]))
        plcPos2 = (int(float(self.currentModel.plcRef1Pos[0]) + deltaX), int(float(self.currentModel.plcRef1Pos[1]) + deltaY), int(float(self.currentModel.plcRef1Pos[2])))
        return ret, plcPos2

    def takeRefImage2(self, plcRev):
        # model = self.mainWindow.runningTab.modelManager.models[self.mainWindow.runningTab.modelManager.currentModelPos]
        ret = self.takeReferenceImage(self.ref2, plcRev)
        print("image pos 2: {}".format(self.ref2.imagePosition))

        mirrorRefPoint1 = self.convertToMirrorAxis(self.currentModel.refPoint1)
        mirrorRefPoint3 = self.convertToMirrorAxis(self.currentModel.refPoint3)

        deltaX = int(self.plcLengthScale * float(mirrorRefPoint3[0])) - int(self.plcLengthScale * float(mirrorRefPoint1[0]))
        deltaY = int(self.plcLengthScale * float(mirrorRefPoint3[1])) - int(self.plcLengthScale * float(mirrorRefPoint1[1]))
        plcPos3 = (int(float(self.currentModel.plcRef1Pos[0]) + deltaX), int(float(self.currentModel.plcRef1Pos[1]) + deltaY), int(float(self.currentModel.plcRef1Pos[2])))
        return ret, plcPos3

    def takeRefImage3(self, plcRev):
        ret = self.takeReferenceImage(self.ref3, plcRev)
        if ret:
            try:
                # model = self.mainWindow.runningTab.modelManager.models[self.mainWindow.runningTab.modelManager.currentModelPos]
                self.calculateRealRefPos(self.currentModel)
                ret, matrix = self.getAffineMatrix(self.currentModel)
                if ret:
                    self.transformDesign2Real(matrix, self.currentModel)
                print(matrix)
            except Exception as error:
                self.mainWindow.runningTab.insertLog("ERROR Take Reference point 3: {}".format(error))
                messagebox.showerror("Take Reference point 3", "{}".format(error))
                return False
        return ret


    def getAffineMatrix(self, model):
        try:
            pixelDesignRefPoint1 = (int(float(model.refPoint1[0])/float(model.conversionCoef)), int(float(model.refPoint1[1])/float(model.conversionCoef)))
            pixelDesignRefPoint2 = (int(float(model.refPoint2[0])/float(model.conversionCoef)), int(float(model.refPoint2[1])/float(model.conversionCoef)))
            pixelDesignRefPoint3 = (int(float(model.refPoint3[0])/float(model.conversionCoef)), int(float(model.refPoint3[1])/float(model.conversionCoef)))
            designRefPoints = np.float32([pixelDesignRefPoint1, pixelDesignRefPoint2, pixelDesignRefPoint3])
            realRefPoints = np.float32([self.ref1.realRefPosition, self.ref2.realRefPosition, self.ref3.realRefPosition])

            matrix = cv.getAffineTransform(designRefPoints, realRefPoints)
            return True, matrix
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Affine Matrix: {}".format(error))
            messagebox.showerror("Affine Matrix", "{}".format(error))
            return False, []

    def transformDesign2Real(self, matrix, model):
        self.realPLCPoints.clear()
        self.realActivePLCPoint.clear()
        self.activeOriginalPositions.clear()
        if self.mainWindow.modelSettingTab.modelTestFlag:
            for i in range(5):
                pixelRefPoint1 = self.convertMmPoint2Pixel(model.refPoint1, model)
                pixelRefPoint2 = self.convertMmPoint2Pixel(model.refPoint2, model)
                pixelRefPoint3 = self.convertMmPoint2Pixel(model.refPoint3, model)
                realPoint1 = self.transformPoint(pixelRefPoint1, matrix, model)
                realPoint2 = self.transformPoint(pixelRefPoint2, matrix, model)
                realPoint3 = self.transformPoint(pixelRefPoint3, matrix, model)
                self.realPLCPoints.append(realPoint1)
                self.realPLCPoints.append(realPoint2)
                self.realPLCPoints.append(realPoint3)
        else:
            for designPoint in self.pixelDesignPoints:
                realPoint = self.transformPoint(designPoint, matrix, model)
                self.realPLCPoints.append((realPoint[0], realPoint[1], int(model.offset[2])))
            for index in range(len(self.realPLCPoints)):
                for point in self.currentModel.activePointsSetting:
                    if index == int(point[0]) and point[1] == PointActivatedState.activated.value:
                        self.realActivePLCPoint.append(self.realPLCPoints[index])
                        self.activeOriginalPositions.append(self.originalPositions[index])

    def convertMmPoint2Pixel(self, point, model):
        x, y = point

        pixelX = int(x / float(model.conversionCoef))
        pixelY = int(y / float(model.conversionCoef))
        return pixelX, pixelY

    def transformPoint(self, point, matrix, model):
        x1 = point[0] * matrix[0][0] + point[1] * matrix[0][1] + matrix[0][2]
        y1 = point[0] * matrix[1][0] + point[1] * matrix[1][1] + matrix[1][2]
        # x1 = int(self.plcLengthScale * x1 * float(model.conversionCoef)) + int(float(model.offset[0]))
        # for mirror axis
        x1 = int(self.plcLengthScale * (self.mirrorXValue - (x1 * float(model.conversionCoef)))) + int(float(model.offset[0]))
        y1 = int(self.plcLengthScale * y1 * float(model.conversionCoef)) + int(float(model.offset[1]))
        return x1, y1

    def calculateRealRefPos(self, model):
        try:
            imageW = self.ref1.image.shape[1]
            imageH = self.ref1.image.shape[0]
            imageCenter = int(imageW/2), int(imageH/2)

            self.ref1.realRefPosition = self.takeRealPos(model, imageCenter, self.ref1, model.refPoint1)
            self.ref2.realRefPosition = self.takeRealPos(model, imageCenter, self.ref2, model.refPoint2)
            if model.numOfRefPoint == NumOfRefPoint._2RefPoint.value:
                ref1 = (int(self.ref1.realRefPosition[0]), int(self.ref1.realRefPosition[1]))
                ref2 = (int(self.ref2.realRefPosition[0]), int(self.ref2.realRefPosition[1]))

                ret, ref3 = ImageProcess.equilateralTriangleFrom2Points(ref1, ref2)
                if ret:
                    self.ref3.realRefPosition = (int(ref3[0]), int(ref3[1]))

            elif model.numOfRefPoint == NumOfRefPoint._3RefPoint.value:
                self.ref3.realRefPosition = self.takeRealPos(model, imageCenter, self.ref3, model.refPoint3)

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Real Reference Calculation: {}".format(error))
            messagebox.showerror("Real Reference Calculation", "{}".format(error))

    def takeRealPos(self, model, imageCenter, realRef, designRef):
        try:
            centerImageX, centerImageY  = imageCenter
            realRefImagePosX, RealRefImagePosY = realRef.imagePosition

            pixelDeltaX = realRefImagePosX - centerImageX
            pixelDeltaY = RealRefImagePosY - centerImageY

            caliPosX = int(designRef[0] / float(model.conversionCoef) + pixelDeltaX)
            caliPosY = int(designRef[1] / float(model.conversionCoef)+ pixelDeltaY)

            return caliPosX, caliPosY
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Real Reference Calculation: {}".format(error))
            messagebox.showerror("Real Reference Calculation", "{}".format(error))
            return 0, 0


    def drawDesignPositionIntoBigPicture(self):
        imageWidth = 672
        imageHeight = 624

        xList = []
        yList = []
        if len(self.originalPositions) <= 0:
            return ImageProcess.createBlackImage()

        for position in self.originalPositions:
            xList.append(position[0])
            yList.append(position[1])

        maxX = int(max(xList) + 50)
        maxY = int(max(yList) + 10)
        maxXShowZone = imageWidth - 110

        self.yCoefficient = imageHeight / maxY
        self.xCoefficient = maxXShowZone / maxX

        ret = ImageProcess.createBlackImage((imageHeight, imageWidth))
        if len(ret.shape) < 3:
            ret = cv.cvtColor(ret, cv.COLOR_GRAY2RGB)
        index = 0
        for position in self.originalPositions:
            # centerX = int(2 * position[0] * self.currentModel.conversionCoef)
            # centerY = int(2 * position[1] * self.currentModel.conversionCoef)
            centerX = int(position[0] * self.xCoefficient)
            centerY = int(position[1] * self.yCoefficient)
            cv.circle(ret, (centerX, centerY), 3, (255, 2555, 255), -1)
            if index < len(self.originalPositions) - 3:
                cv.circle(ret, (centerX, centerY), 3, (255, 2555, 255), -1)
            else:
                cv.circle(ret, (centerX, centerY), 5, (255, 0, 255), -1)

            if index % 2 == 0:
                textColor = (0, 255, 0)
            else:
                textColor = (0, 255, 255)
            cv.putText(ret, "{}".format(index), (centerX - 2, centerY - 6), cv.FONT_HERSHEY_SIMPLEX,
                       self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, textColor,
                       self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                       lineType=cv.LINE_AA)
            index += 1
            pass
        self.designPosImage = ret.copy()
        # self.processImage = ret.copy()
        return ret

    def drawGuideColor(self):
        if len(self.processImage.shape) < 3:
            self.processImage = cv.cvtColor(self.processImage, cv.COLOR_GRAY2RGB)
        imageWidth = self.processImage.shape[1]
        textColor = (255, 255, 255)
        xColorPos = 150
        xTextPos = xColorPos - 20
        yColor = 15
        yText = 20
        yDelta = 30

        cv.circle(self.processImage, (imageWidth - xColorPos, yColor + yDelta), 8, (0, 255, 0), -1)
        cv.circle(self.processImage, (imageWidth - xColorPos, yColor + 2 * yDelta), 8, (0, 0, 255), -1)
        cv.circle(self.processImage, (imageWidth - xColorPos, yColor + 3 * yDelta), 8, (0, 255, 255), -1)


        cv.putText(self.processImage,
                   "SN: {}".format(self.serialNo),
                   (imageWidth - xColorPos - 30, yText),
                   cv.FONT_HERSHEY_SIMPLEX, self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                   textColor,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)

        cv.putText(self.processImage, "OK:", (imageWidth - xTextPos, yText + yDelta), cv.FONT_HERSHEY_SIMPLEX,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, textColor,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)
        cv.putText(self.processImage, "NG Torque:", (imageWidth - xTextPos, yText + 2 * yDelta), cv.FONT_HERSHEY_SIMPLEX,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, textColor,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)
        cv.putText(self.processImage, "NG Height:", (imageWidth - xTextPos, yText + 3 * yDelta), cv.FONT_HERSHEY_SIMPLEX,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, textColor,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)
        cv.putText(self.processImage, "Total:", (imageWidth - xTextPos, yText + 4 * yDelta), cv.FONT_HERSHEY_SIMPLEX,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, textColor,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)
        cv.putText(self.processImage, "Takt time:", (imageWidth - xTextPos, yText + 5 * yDelta), cv.FONT_HERSHEY_SIMPLEX,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, textColor,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)
        self.drawCountResult()

    def drawCountResult(self):
        if len(self.processImage.shape) < 3:
            self.processImage = cv.cvtColor(self.processImage, cv.COLOR_GRAY2RGB)
        imageWidth = self.processImage.shape[1]

        textColor = (255, 255, 255)
        xTextPos = 40
        yTextPos = 50
        yDelta = 30


        cv.putText(self.processImage, "{}".format(int(self.numOfOk)), (imageWidth - xTextPos, yTextPos),
                   cv.FONT_HERSHEY_SIMPLEX,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, textColor,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)
        cv.putText(self.processImage, "{}".format(int(self.numOfNgToque)), (imageWidth - xTextPos, yTextPos + yDelta),
                   cv.FONT_HERSHEY_SIMPLEX,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, textColor,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)
        cv.putText(self.processImage, "{}".format(int(self.numOfNgHeight)), (imageWidth - xTextPos, yTextPos + 2 * yDelta),
                   cv.FONT_HERSHEY_SIMPLEX,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, textColor,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)
        cv.putText(self.processImage, "{}".format(int(self.numOfTotal)), (imageWidth - xTextPos, yTextPos + 3 * yDelta),
                   cv.FONT_HERSHEY_SIMPLEX,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, textColor,
                   self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)

    def clearResult(self):
        if len(self.processImage.shape) < 3:
            self.processImage = cv.cvtColor(self.processImage, cv.COLOR_GRAY2RGB)
        imageWidth = self.processImage.shape[1]
        imageHeight = self.processImage.shape[0]

        self.processImage[30: imageHeight, imageWidth - 40: imageWidth - 2] = (0, 0, 0)

    def saveData(self):
        try:
            dataFolder = "./data"
            dataAdjustScrewPos = dataFolder + "/Adjust Screw Position"
            dateFolder = dataAdjustScrewPos + "/" + TimeControl.y_m_dFormat()
            barcodeFolder = dateFolder + "/" + str(self.serialNo)

            PathFileControl.generatePath(dateFolder)
            PathFileControl.generatePath(dataAdjustScrewPos)
            PathFileControl.generatePath(dateFolder)

            if os.path.exists(barcodeFolder):
                num = 1
                while True:
                    barcodeFolder = dateFolder + "/" + str(self.serialNo) + "_" + str(num)
                    if os.path.exists(barcodeFolder):
                        num += 1
                        continue
                    else:
                        break
            PathFileControl.generatePath(barcodeFolder)

            # save image
            ref1FilePath = barcodeFolder + "/Ref1.jpg"
            ref2FilePath = barcodeFolder + "/Ref2.jpg"
            ref3FilePath = barcodeFolder + "/Ref3.jpg"
            try:
                # cv.imwrite(ref1FilePath, self.ref1.image)
                # cv.imwrite(ref2FilePath, self.ref2.image)
                # cv.imwrite(ref3FilePath, self.ref3.image)
                cv.imencode(".jpg", self.ref1.image)[1].tofile(ref1FilePath)
                cv.imencode(".jpg", self.ref2.image)[1].tofile(ref2FilePath)
                cv.imencode(".jpg", self.ref3.image)[1].tofile(ref3FilePath)

            except Exception as error:
                self.mainWindow.runningTab.insertLog("ERROR Save Ref Image: {}".format(error))
                messagebox.showerror("Save Ref Image", "{}".format(error))


            # save point, design point, plc Point
            pointsFilePath = barcodeFolder + "/PointsPosition.csv"
            pointsFile = CsvFile(pointsFilePath)
            try:
                pointsFile.dataList.append(["OK", "NG TORQUE","NG HEIGHT", "TOTAL"])

                pointsFile.dataList.append(["{}".format(self.numOfOk), "{}".format(self.numOfNgToque), "{}".format(self.numOfNgHeight), "{}".format(self.numOfTotal)])
                pointsFile.dataList.append([""])
                pointsFile.dataList.append(["Design Position X", "Design Position Y", " ", "PLC Position X", "PLC Position Y"])
                for pointIndex in range(len(self.pixelDesignPoints)):
                    pointsFile.dataList.append([self.originalPositions[pointIndex][0],
                                                self.originalPositions[pointIndex][1],
                                                " ",
                                                self.realPLCPoints[pointIndex][0],
                                                self.realPLCPoints[pointIndex][1]])

                pointsFile.saveFile()
            except Exception as error:
                self.mainWindow.runningTab.insertLog("ERROR Save Positions: {}".format(error))
                messagebox.showerror("Save Positions", "{}".format(error))
        except:
            pass
    def showTransferringPosImage(self):
        self.mainWindow.showImage(self.transImage[self.transferringImageIndex], True)

        if self.transferringImageIndex < 3:
            self.transferringImageIndex += 1
        else:
            self.transferringImageIndex = 0

    def processCurrentPos(self, plcValue):
        try:
            currentPos = int(plcValue[0:3])
            # currentPos = int(self.currentModel.activeFrom) + currentPos

            state = plcValue[4:6]
            self.showCurrentPositionState(currentPos, state, (0,0))
        except:
            pass

    def showCurrentPositionState(self, index, state, coordinate):
        if self.newProcessFlag:
            self.newProcessFlag = False
            self.processImage = self.drawDesignPositionIntoBigPicture()
            self.drawGuideColor()
            self.numOfOk = 0
            self.numOfNgToque = 0
            self.numOfNgHeight = 0
            self.numOfTotal = 0

        try:
            if len(self.processImage.shape) < 3:
                self.processImage = cv.cvtColor(self.processImage, cv.COLOR_GRAY2RGB)
            position = self.activeOriginalPositions[index]
            # position = self.originalPositions[index]

            centerX = int(position[0] * self.xCoefficient)
            centerY = int(position[1] * self.yCoefficient)

            if state == PositionState.OK.value:
                self.numOfOk += 1
                greenColor = (0, 255, 0)
                cv.circle(self.processImage, (centerX, centerY), 4, greenColor, -1)
            elif state == PositionState.NG.value:
                self.numOfNgToque += 1
                redColor = (0, 0, 255)
                cv.circle(self.processImage, (centerX, centerY), 4, redColor, -1)
            elif state == PositionState.NH.value:
                self.numOfNgHeight += 1
                yellowColor = (0, 255, 255)
                cv.circle(self.processImage, (centerX, centerY), 4, yellowColor, -1)
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Show current position state: {}".format(error))
            self.mainWindow.runningTab.insertLog("{}".format(error))

        try:
            self.numOfTotal = self.numOfOk + self.numOfNgToque + self.numOfNgHeight
            self.clearResult()
            self.drawCountResult()
            # self.mainWindow.showImage(self.processImage)
            # if index == int(self.currentModel.activeTo):
            imageWidth = self.processImage.shape[1]
            xTextPos = 150 - 20
            yTextPos = 20 + 5 * 30

            # tackTime = int((TimeControl.time() - self.startingTime)/(int(self.currentModel.activeTo) - int(self.currentModel.activeFrom) + 1) / 1000)
            tackTime = int((TimeControl.time() - self.startingTime) / 1000)
            cv.putText(self.processImage, "Takt Time: {}s".format(tackTime),(imageWidth - xTextPos, yTextPos), cv.FONT_HERSHEY_SIMPLEX,
                       self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, (255, 255, 255),
                       self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)
            cv.putText(self.processImage, "Ref Time: {}s".format(int(self.refTime/1000)), (imageWidth - xTextPos, yTextPos + 30),
                       cv.FONT_HERSHEY_SIMPLEX,
                       self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale, (255, 255, 255),
                       self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)
            self.mainWindow.showImage(self.processImage, True)

            currentResult = self.mainWindow.runningTab.resultTab.currentResultFrame.result
            currentResult.serialNo = self.serialNo
            currentResult.ok = self.numOfOk
            currentResult.ngTorque = self.numOfNgToque
            currentResult.ngHeight = self.numOfNgHeight
            currentResult.total = self.numOfTotal
            currentResult.visionTime = int(self.refTime/1000)
            currentResult.progressTime = tackTime

            self.mainWindow.runningTab.showCurrentResult()
            # if index == int(self.currentModel.activeTo):
            if index == len(self.realActivePLCPoint) - 1:
                self.saveData()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Show current position state: {}".format(error))
            self.mainWindow.runningTab.insertLog("show current position: {}".format(error))
