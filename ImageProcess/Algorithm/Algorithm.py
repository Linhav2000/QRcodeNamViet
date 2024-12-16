import numpy as np
import ImageProcess.ImageProcess
from ImageProcess import ImageProcess
from CommonAssit import PathFileControl, Color
from CommonAssit import TimeControl
import jsonpickle
import tkinter.messagebox as messagebox
import os
from ImageProcess.Algorithm.StepParamter import StepParameter
from ImageProcess.Algorithm.AlgorithmParameter import AlgorithmParameter
from ImageProcess.Algorithm.AlgorithmResult import AlgorithmResult
from ImageProcess.Algorithm.MethodList import MethodList
from ImageProcess.Algorithm.AlgorithmResult import AlgorithmResultKey
from View.Common.LoadingView import LoadingView
from ImageProcess.Algorithm.StepParamter import ThresholdCode
from ImageProcess.Algorithm.StepParamter import RF_Type, ReferenceEdgeCornerType
from ImageProcess.Algorithm.StepParamter import ChangeColorCode
from Connection.Camera import Camera
from Modules.Viet_OCR import *
import copy
import threading


# filepath = "./config/algorithm_path.txt"
# file = TextFile(filepath)
# if file.readFile()[1].__contains__("True"):
#     if file.readFile()[2].__contains__("TF2"):
#         import tf2_object_detection as object_detection
#         object_detection.init_model()
#     else:
#         import Object_detection_image_in_main as object_detection

class Algorithm:
    filePath = ".config/Algorithm/algorithm1"
    sourceImage = ImageProcess.createBlackImage()
    result = []
    imageList = []
    resultList = []
    maxStep = 0
    last_execute_step = None
    viet_ocr_engine = None

    def __init__(self, filePath, mainWindow, maxStep):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow
        self.model_segmentation_yolov8 = None
        self.filePath = filePath
        self.maxStep = maxStep
        self.algorithmParameter = AlgorithmParameter()
        self.get()

    def load_model_yolo(self, path_model):
        from ultralytics import YOLO
        self.model_segmentation_yolov8 = YOLO(path_model)
        self.mainWindow.runningTab.insertLog(f"Load model: {path_model}")

    def save(self):
        try:
            jsonStepData = {}
            self.filePath = "./config/Algorithm/" + self.algorithmParameter.name
            PathFileControl.generatePath(self.filePath)
            dataFilePath = self.filePath + "/data.json"
            dataFile = JsonFile(dataFilePath)
            self.algorithmParameter.jsonSteps = []

            for step in self.algorithmParameter.steps:
                self.algorithmParameter.jsonSteps.append(jsonpickle.encode(step))
            jsonData = jsonpickle.encode(self.algorithmParameter)
            dataFile.writeData(jsonData)
            # print(jsonData)
            return True
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Algorithm: {}".format(error))
            return False

    def get(self):
        dataFilePath = self.filePath + "/data.json"
        dataFile = JsonFile(dataFilePath)
        jsonData = dataFile.readFile()

        if jsonData is None:
            return
        try:
            self.algorithmParameter = jsonpickle.decode(jsonData)
            self.algorithmParameter.steps = []
            for jsonStep in self.algorithmParameter.jsonSteps:
                step: StepParameter = jsonpickle.decode(jsonStep)
                step.makeStandard()
                self.algorithmParameter.steps.append(step)

            for index in range(self.maxStep):
                self.imageList.append(None)
            # print(len(self.algorithmParameter.steps))
        except Exception as error:
            PathFileControl.deleteFolder(self.filePath)
            self.mainWindow.runningTab.insertLog("ERROR Get Algorithm parameter: {}".format(error))
            # messagebox.showerror("Get Algorithm parameter", "{}".format(error))

    def rename(self, newName):
        try:
            self.filePath = "./config/Algorithm/" + self.algorithmParameter.name
            oldPath = "./config/Algorithm/" + self.algorithmParameter.name
            newPath = "./config/Algorithm/" + newName
            PathFileControl.moveFolder(src=oldPath, dst=newPath)
            self.algorithmParameter.name = newName
            if self.save():
                self.mainWindow.algorithmManager.changeCurrentAlgorithm(self.algorithmParameter.name)
                self.mainWindow.algorithmManager.updateList()
                return True
            else:
                return False
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Rename algorithm not successfully. Detail: {}".format(error))
            return False

    def exchangeStepPos(self, pos1, pos2):
        intermediateStep = copy.deepcopy(self.algorithmParameter.steps[pos1])
        intermediateStep.stepId = self.algorithmParameter.steps[pos2].stepId

        self.algorithmParameter.steps[pos2].stepId = self.algorithmParameter.steps[pos1].stepId
        self.algorithmParameter.steps[pos1] = copy.deepcopy(self.algorithmParameter.steps[pos2])

        self.algorithmParameter.steps[pos2] = copy.deepcopy(intermediateStep)

        self.mainWindow.researchingTab.showCurrentAlgorithm()

        self.save()

    def stepUp(self, stepPos):
        if stepPos <= 0:
            messagebox.showwarning("Up step", "Cannot up step in step 0")
        else:
            self.exchangeStepPos(stepPos, stepPos - 1)

    def stepDown(self, stepPos):
        if stepPos >= (self.mainWindow.algorithmManager.maxStep - 1):
            messagebox.showwarning("Down step", "Cannot down last step")
        else:
            self.exchangeStepPos(stepPos, stepPos + 1)

    def duplicateStep(self, stepPos):
        res = False
        for step in reversed(self.algorithmParameter.steps):
            if not step.activeFlag and step.stepId != stepPos:
                self.algorithmParameter.steps.__delitem__(step.stepId)
                if step.stepId > stepPos:
                    duplicateStep = copy.deepcopy(self.algorithmParameter.steps[stepPos])
                    self.algorithmParameter.steps.insert(stepPos + 1, duplicateStep)
                else:
                    duplicateStep = copy.deepcopy(self.algorithmParameter.steps[stepPos - 1])
                    self.algorithmParameter.steps.insert(stepPos, duplicateStep)
                res = True
                break

        if not res:
            messagebox.showwarning("Insert Step", "There no place to duplicate a step")
        else:
            for index in range(len(self.algorithmParameter.steps)):
                self.algorithmParameter.steps[index].stepId = index

        self.mainWindow.researchingTab.showCurrentAlgorithm()

        self.save()

    def insertStepDown(self, stepPos):
        res = False
        for step in reversed(self.algorithmParameter.steps):
            if not step.activeFlag and step.stepId != stepPos:
                self.algorithmParameter.steps.__delitem__(step.stepId)
                if step.stepId > stepPos:
                    self.algorithmParameter.steps.insert(stepPos + 1, StepParameter())
                else:
                    self.algorithmParameter.steps.insert(stepPos, StepParameter())
                res = True
                break

        if not res:
            messagebox.showwarning("Insert Step", "There no place to insert a step")
        else:
            for index in range(len(self.algorithmParameter.steps)):
                self.algorithmParameter.steps[index].stepId = index

        self.mainWindow.researchingTab.showCurrentAlgorithm()

        self.save()

    def executeStep(self, executedStepId, image=None, camera: Camera = None, isRunningFlag=False,
                    isGettingReference=False):
        self.mainWindow.resetBasePoint()
        time = TimeControl.time()
        if self.last_execute_step is None:
            self.resultList: [AlgorithmResult] = []
            self.imageList = []
            for index in range(self.maxStep):
                self.imageList.append(None)
            for index in range(self.maxStep):
                self.resultList.append(None)
        text = ""
        if camera is None:
            _camera = self.mainWindow.workingThread.cameraManager.currentCamera
        else:
            _camera = camera

        if image is None and self.mainWindow.originalImage is None:
            text = "ERROR Algorithm {}. There is no image to process\nPlease take the image first!".format(
                self.algorithmParameter.name)

            self.mainWindow.runningTab.insertLog(text)
            # messagebox.showwarning("ERROR Excute Algorithm", "There is no image to process\nPlease take the image first!")
            return False, self.resultList, text
        originalImage = image.copy() if image is not None else self.mainWindow.originalImage.copy()
        # self.mainWindow.originalImage = originalImage.copy()
        self.mainWindow.runningTab.insertLog("begin execute algorithm")
        if self.last_execute_step is None:
            execute_range = range(0, executedStepId + 1)
        else:
            if self.last_execute_step > executedStepId:
                execute_range = range(executedStepId, executedStepId + 1)
            else:
                execute_range = range(self.last_execute_step, executedStepId + 1)
        index = 0
        try:
            for index in execute_range:
                step_image_show = None
                step_image_result = None
                basePoint = [0, 0]
                step: StepParameter = self.algorithmParameter.steps[index]

                if not step.activeFlag:
                    continue

                self.mainWindow.runningTab.insertLog(
                    "begin step {} name {}".format(step.stepId, step.stepAlgorithmName))

                if step.resourceIndex[0] == -1:
                    sourceImage = originalImage.copy()
                elif step.resourceIndex[0] == -4:
                    refImagePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                                           "/",
                                                           self.algorithmParameter.name,
                                                           "/",
                                                           "imageReference_",
                                                           self.algorithmParameter.refImageName,
                                                           ".png")
                    try:
                        sourceImage = cv.imdecode(np.fromfile(refImagePath, dtype=np.uint8), cv.IMREAD_COLOR)
                    except Exception as error:
                        text = "ERROR Algorithm {}. Step {} Please check the image reference. Detaial {}".format(
                            step.stepAlgorithmName, step.stepId, error)
                        self.mainWindow.runningTab.insertLog(text)
                        return False, self.resultList, text
                elif step.resourceIndex[0] == -3:
                    templatePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                                           "/",
                                                           self.algorithmParameter.name,
                                                           "/",
                                                           "imageTemplate_",
                                                           step.templateName,
                                                           ".png")
                    try:
                        sourceImage = cv.imdecode(np.fromfile(templatePath, dtype=np.uint8), cv.IMREAD_COLOR)
                    except Exception as error:
                        text = "ERROR Algorithm {}. Step {} Please check the image template".format(
                            step.stepAlgorithmName, step.stepId)
                        self.mainWindow.runningTab.insertLog(text)
                        return False, self.resultList, text

                elif step.resourceIndex[0] == -2:
                    # messagebox.showerror("Execute Step", "Please choose source image for step {}".format(index))
                    text = "ERROR Algorithm {}. Step {} Please choose source image".format(step.stepAlgorithmName,
                                                                                           step.stepId)
                    self.mainWindow.runningTab.insertLog(text)
                    sourceImage = None
                    return False, self.resultList, text
                else:
                    sourceImage = self.imageList[step.resourceIndex[0]].copy()
                    try:
                        sourceResult = self.getResultWithId(self.resultList, step.resourceIndex[0])
                        if sourceResult.basePoint is not None:
                            basePoint = sourceResult.basePoint
                        if sourceResult.workingArea is not None:
                            basePoint = (basePoint[0] + sourceResult.workingArea[0],
                                         basePoint[1] + sourceResult.workingArea[1])
                    except:
                        pass

                workingArea = (0, 0, 0, 0)
                if step.workingArea is None:
                    workingArea = (0, 0, sourceImage.shape[1], sourceImage.shape[0])
                else:
                    workingArea = step.workingArea

                # validate working area:
                if workingArea[3] - workingArea[1] > sourceImage.shape[0] \
                        or workingArea[2] - workingArea[0] > sourceImage.shape[1] \
                        or workingArea[3] > sourceImage.shape[0] \
                        or workingArea[2] > sourceImage.shape[1]:
                    # messagebox.showerror("Step {}".format(step.stepId),
                    #                      "Step {} has working area out of image".format(step.stepId))
                    text = "ERROR Algorithm {}. Step {} has working area out of image".format(step.stepAlgorithmName,
                                                                                              step.stepId)

                    self.mainWindow.runningTab.insertLog(text)
                    return False, self.resultList, text
                step_resource_image = sourceImage.copy()
                sourceImage = sourceImage[workingArea[1]:workingArea[3],
                              workingArea[0]:workingArea[2]]
                # Blur
                if step.stepAlgorithmName == MethodList.blur.value:
                    processImage = ImageProcess.processBlur(image=sourceImage, ksize=step.blurSize)
                    self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             workingArea=workingArea, basePoint=basePoint)
                    step_image_show = step_image_result = processImage
                    # self.imageList[index] = processImage.copy()
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(processImage)

                # Median Blur
                elif step.stepAlgorithmName == MethodList.medianBlur.value:
                    processImage = ImageProcess.processMedianBlur(image=sourceImage, ksize=step.blurSize)
                    # self.imageList[index] = processImage.copy()
                    self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             workingArea=workingArea, basePoint=basePoint)
                    step_image_show = step_image_result = processImage
                    #
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(processImage)
                # Gaussian Blur
                elif step.stepAlgorithmName == MethodList.gaussianBlur.value:
                    processImage = ImageProcess.processGaussianBlur(image=sourceImage, ksize=step.blurSize,
                                                                    sigmaX=step.blurSigmaX)
                    # self.imageList[index] = processImage.copy()
                    self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             workingArea=workingArea, basePoint=basePoint)
                    step_image_show = step_image_result = processImage

                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(processImage)
                # Find contours
                elif step.stepAlgorithmName == MethodList.findContour.value:
                    # get binary image for find contours
                    binarySourceIndex, paramName = step.contours_binary_source
                    ret, binarySource, text = self.getSourceImage(imageIndex=binarySourceIndex, step=step,
                                                                  originalImage=originalImage)
                    centerList = []
                    listContours, areaDetectList, contourImage = ImageProcess.processFindContours(source=binarySource,
                                                                                                  minArea=step.minAreaContours,
                                                                                                  maxArea=step.maxAreaContours,
                                                                                                  minWidth=step.minWidthContours,
                                                                                                  maxWidth=step.maxWidthContours,
                                                                                                  minHeight=step.minHeightContours,
                                                                                                  maxHeight=step.maxHeightContours,
                                                                                                  minAspectRatio=step.minAspectRatio,
                                                                                                  maxAspectRatio=step.maxAspectRatio)

                    if len(sourceImage.shape) < 3:
                        sourceImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_GRAY2BGR)
                    drawContourImage = cv.drawContours(sourceImage, listContours, -1, (0, 255, 0), 5)
                    step_image_show = drawContourImage
                    step_image_result = contourImage

                    if len(listContours) > 0:
                        for areaDetect in areaDetectList:
                            center = (
                            int((areaDetect[0] + areaDetect[2]) / 2), int((areaDetect[1] + areaDetect[3]) / 2))
                            centerList.append(center)
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                                 workingArea=workingArea, basePoint=basePoint,
                                                                 drawImage=contourImage,
                                                                 methodName=step.stepAlgorithmName,
                                                                 detectAreaList=areaDetectList,
                                                                 contourList=listContours,
                                                                 pointList=centerList)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=False,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=sourceImage,
                                                                 workingArea=workingArea, basePoint=basePoint)
                # Count contours
                elif step.stepAlgorithmName == MethodList.countContour.value:

                    listContours, areaDetectList, contourImage = ImageProcess.processFindContours(source=sourceImage,
                                                                                                  minArea=step.minAreaContours,
                                                                                                  maxArea=step.maxAreaContours,
                                                                                                  minWidth=step.minWidthContours,
                                                                                                  maxWidth=step.maxWidthContours,
                                                                                                  minHeight=step.minHeightContours,
                                                                                                  maxHeight=step.maxHeightContours,
                                                                                                  minAspectRatio=step.minAspectRatio,
                                                                                                  maxAspectRatio=step.maxAspectRatio)
                    numContour = len(areaDetectList)
                    if len(sourceImage.shape) < 3:
                        drawContourImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_GRAY2BGR)
                    else:
                        drawContourImage = sourceImage.copy()
                    if not isRunningFlag and step.stepId == executedStepId:
                        drawContourImage = cv.drawContours(drawContourImage.copy(), listContours, -1, (0, 255, 0), 5)

                    if numContour == step.contourNumThresh:
                        color = (0, 255, 0)
                        if not isRunningFlag and step.stepId == executedStepId:
                            drawContourImage = cv.putText(drawContourImage, "{}".format(numContour),
                                                          (int(drawContourImage.shape[1] / 2),
                                                           int(drawContourImage.shape[0] / 2)),
                                                          cv.FONT_HERSHEY_SIMPLEX,
                                                          _camera.parameter.textScale, color,
                                                          _camera.parameter.textThickness, lineType=cv.LINE_AA)

                        self.resultList[index] = AlgorithmResult(stepId=index, passed=True, drawImage=drawContourImage,
                                                                 methodName=step.stepAlgorithmName,
                                                                 detectAreaList=areaDetectList,
                                                                 contourList=listContours,
                                                                 workingArea=workingArea, basePoint=basePoint)
                    else:
                        if not isRunningFlag and step.stepId == executedStepId:
                            color = (0, 0, 255)
                            drawContourImage = cv.putText(drawContourImage, "{}".format(numContour),
                                                          (int(drawContourImage.shape[1] / 2),
                                                           int(drawContourImage.shape[0] / 2)),
                                                          cv.FONT_HERSHEY_SIMPLEX,
                                                          _camera.parameter.textScale,  
                                                          color, _camera.parameter.textThickness, lineType=cv.LINE_AA)

                        self.resultList[index] = AlgorithmResult(stepId=index, passed=False, drawImage=drawContourImage,
                                                                 methodName=step.stepAlgorithmName,
                                                                 detectAreaList=areaDetectList,
                                                                 contourList=listContours,
                                                                 workingArea=workingArea, basePoint=basePoint)

                    self.imageList[index] = sourceImage.copy()
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(image=drawContourImage)

                # Fill Contours
                elif step.stepAlgorithmName == MethodList.fillContour.value:
                    listContours, areaDetectList, contourImage = ImageProcess.processFindContours(source=sourceImage,
                                                                                                  minArea=step.minAreaContours,
                                                                                                  maxArea=step.maxAreaContours,
                                                                                                  minWidth=step.minWidthContours,
                                                                                                  maxWidth=step.maxWidthContours,
                                                                                                  minHeight=step.minHeightContours,
                                                                                                  maxHeight=step.maxHeightContours,
                                                                                                  minAspectRatio=step.minAspectRatio,
                                                                                                  maxAspectRatio=step.maxAspectRatio)
                    drawContourImage = np.zeros(shape=sourceImage.shape, dtype=np.uint8)
                    for contour in listContours:
                        drawContourImage = cv.drawContours(drawContourImage, [contour], -1, step.fillColor,
                                                           thickness=cv.FILLED, lineType=cv.LINE_AA)

                    self.imageList[index] = drawContourImage.copy()
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(image=drawContourImage)
                    if len(listContours) > 0:
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=True, drawImage=drawContourImage,
                                                                 methodName=step.stepAlgorithmName,
                                                                 detectAreaList=areaDetectList,
                                                                 contourList=listContours,
                                                                 workingArea=workingArea, basePoint=basePoint)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=False,
                                                                 methodName=step.stepAlgorithmName,
                                                                 workingArea=workingArea, basePoint=basePoint,
                                                                 drawImage=sourceImage)
                # Get image inside contour
                elif step.stepAlgorithmName == MethodList.getImageInsideContour.value:

                    # get binary image for find contours
                    binarySourceIndex, paramName = step.contours_binary_source
                    ret, binarySource, text = self.getSourceImage(imageIndex=binarySourceIndex, step=step,
                                                                  originalImage=originalImage)
                    if not ret:
                        return ret, self.resultList, text

                    # get working area and base point to do bitwise method
                    areaResult = self.getResultWithSource(resultList=self.resultList, source=step.contours_area_source)

                    if areaResult is not None:
                        sourceWorkingArea = areaResult.workingArea
                        sourceBasePoint = areaResult.basePoint
                    else:
                        sourceWorkingArea = workingArea
                        sourceBasePoint = basePoint

                    sourceWorkingArea = (
                    sourceWorkingArea[0] + sourceBasePoint[0], sourceWorkingArea[1] + sourceBasePoint[1],
                    sourceWorkingArea[2] + sourceBasePoint[0], sourceWorkingArea[3] + sourceBasePoint[1])
                    sourceImage = sourceImage[sourceWorkingArea[1]: sourceWorkingArea[3],
                                  sourceWorkingArea[0]:sourceWorkingArea[2]]

                    listContours, areaDetectList, contourImage = ImageProcess.processFindContours(source=binarySource,
                                                                                                  minArea=step.minAreaContours,
                                                                                                  maxArea=step.maxAreaContours,
                                                                                                  minWidth=step.minWidthContours,
                                                                                                  maxWidth=step.maxWidthContours,
                                                                                                  minHeight=step.minHeightContours,
                                                                                                  maxHeight=step.maxHeightContours,
                                                                                                  minAspectRatio=step.minAspectRatio,
                                                                                                  maxAspectRatio=step.maxAspectRatio)

                    mask = np.zeros_like(sourceImage)

                    mask = cv.drawContours(mask, listContours, -1, step.fillColor,
                                           thickness=cv.FILLED, lineType=cv.LINE_AA)

                    imageFromContour = ImageProcess.processBitwise_and(source1=sourceImage,
                                                                       source2=sourceImage,
                                                                       mask=mask)

                    self.imageList[index] = imageFromContour.copy()
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(image=imageFromContour)

                    if len(listContours) > 0:
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=True, drawImage=imageFromContour,
                                                                 methodName=step.stepAlgorithmName,
                                                                 detectAreaList=areaDetectList,
                                                                 contourList=listContours,
                                                                 workingArea=areaResult.workingArea,
                                                                 basePoint=areaResult.basePoint)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=False,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=sourceImage,
                                                                 workingArea=areaResult.workingArea,
                                                                 basePoint=areaResult.basePoint)

                # Delate
                elif step.stepAlgorithmName == MethodList.dilate.value:
                    dilateImage = ImageProcess.processDilate(sourceImage=sourceImage, kernelSizeX=step.kernelSizeX,
                                                             kernelSizeY=step.kernelSizeY, iterations=step.iterations)
                    self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             workingArea=workingArea, basePoint=basePoint)
                    self.imageList[index] = dilateImage
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(image=dilateImage)
                # Erode
                elif step.stepAlgorithmName == MethodList.erode.value:
                    erodeImage = ImageProcess.processErode(sourceImage=sourceImage, kernelSizeX=step.kernelSizeX,
                                                           kernelSizeY=step.kernelSizeY, iterations=step.iterations)
                    self.imageList[index] = erodeImage.copy()
                    self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             workingArea=workingArea, basePoint=basePoint)
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(image=erodeImage)

                # Bit and wise
                elif step.stepAlgorithmName == MethodList.bitwiseAnd.value:
                    ret, sourceImage2, text = self.getSourceImage(imageIndex=step.resource2Index, step=step,
                                                                  originalImage=originalImage)
                    if not ret:
                        return ret, self.resultList, text
                    ret, mask, text = self.getSourceImage(imageIndex=step.maskIndex, step=step,
                                                          originalImage=originalImage)
                    if not ret:
                        return ret, self.resultList, text
                    bitAndWiseImage = ImageProcess.processBitwise_and(source1=sourceImage, source2=sourceImage2,
                                                                      mask=mask)
                    self.imageList[index] = bitAndWiseImage.copy()
                    self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint, passed=True,
                                                             stepId=step.stepId, methodName=step.stepAlgorithmName)
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(bitAndWiseImage)

                # Bit or wise
                elif step.stepAlgorithmName == MethodList.bitwiseOr.value:
                    ret, sourceImage2, text = self.getSourceImage(imageIndex=step.resource2Index, step=step,
                                                                  originalImage=originalImage)
                    if not ret:
                        return ret, self.resultList, text
                    ret, mask, text = self.getSourceImage(imageIndex=step.maskIndex, step=step,
                                                          originalImage=originalImage)
                    if not ret:
                        return ret, self.resultList, text

                    bitOrWiseImage = ImageProcess.processBitwise_or(source1=sourceImage, source2=sourceImage2,
                                                                    mask=None)
                    self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint, passed=True,
                                                             stepId=step.stepId, methodName=step.stepAlgorithmName)
                    self.imageList[index] = bitOrWiseImage.copy()
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(bitOrWiseImage)
                # Bit Not wise
                elif step.stepAlgorithmName == MethodList.bitwiseNot.value:
                    ret, sourceImage2, text = self.getSourceImage(imageIndex=step.resource2Index, step=step,
                                                                  originalImage=originalImage)
                    if not ret:
                        return ret, self.resultList, text
                    ret, mask, text = self.getSourceImage(imageIndex=step.maskIndex, step=step,
                                                          originalImage=originalImage)
                    if not ret:
                        return ret, self.resultList, text

                    bitNotWiseImage = ImageProcess.processBitwise_not(source1=sourceImage, source2=sourceImage2,
                                                                      mask=mask)
                    self.imageList[index] = bitNotWiseImage.copy()
                    self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint, passed=True,
                                                             stepId=step.stepId, methodName=step.stepAlgorithmName)
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(bitNotWiseImage)

                # Bit Xor wise
                elif step.stepAlgorithmName == MethodList.bitwiseXor.value:
                    ret, sourceImage2, text = self.getSourceImage(imageIndex=step.resource2Index, step=step,
                                                                  originalImage=originalImage)
                    if not ret:
                        return ret, self.resultList, text
                    ret, mask, text = self.getSourceImage(imageIndex=step.maskIndex, step=step,
                                                          originalImage=originalImage)
                    if not ret:
                        return ret, self.resultList, text

                    bitXorWiseImage = ImageProcess.processBitwise_xor(source1=sourceImage, source2=sourceImage2,
                                                                      mask=mask)
                    self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint, passed=True,
                                                             stepId=step.stepId, methodName=step.stepAlgorithmName)
                    self.imageList[index] = bitXorWiseImage.copy()
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(bitXorWiseImage)
                # Rotate
                elif step.stepAlgorithmName == MethodList.rotate.value:
                    if step.rotateCode == -1:
                        ret, rotateImage, text = ImageProcess.rotateImage(sourceImage, angle=step.rt_angle,
                                                                          centerPoint=step.rt_center)
                        if not ret:
                            self.mainWindow.runningTab.insertLog(text)
                    else:
                        rotateImage = ImageProcess.processRotateImage(sourceImage, step.rotateCode)

                    self.imageList[index] = rotateImage.copy()
                    self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint, passed=True,
                                                             stepId=step.stepId, methodName=step.stepAlgorithmName)
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(rotateImage)
                # Flip Image
                elif step.stepAlgorithmName == MethodList.flip.value:
                    flipImage = ImageProcess.processFlip(sourceImage, code=step.flipCode)
                    self.imageList[index] = flipImage.copy()
                    self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint, passed=True,
                                                             stepId=step.stepId, methodName=step.stepAlgorithmName)
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(flipImage)

                # Matching Template
                elif step.stepAlgorithmName == MethodList.matchingTemplate.value:
                    templatePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                                           "/",
                                                           self.algorithmParameter.name,
                                                           "/",
                                                           "imageTemplate_",
                                                           step.templateName,
                                                           ".png")
                    template = cv.imdecode(np.fromfile(templatePath, dtype=np.uint8), cv.IMREAD_GRAYSCALE)

                    # validate template image
                    if workingArea[3] - workingArea[1] < template.shape[0] \
                            or workingArea[2] - workingArea[0] < template.shape[1]:
                        # messagebox.showerror("Matching template step {}".format(step.stepId), "Step {} has working area smaller than template".format(step.stepId))
                        text = "ERROR Algorithm {}. Step {} has working area smaller than template".format(
                            step.stepAlgorithmName, step.stepId)
                        self.mainWindow.runningTab.insertLog(text)
                        return False, [], text
                    matchingResultList = ImageProcess.processTemplateMatching(sourceImage, template=template,
                                                                              minMatchingValue=float(
                                                                                  step.minMatchingValue),
                                                                              multiMatchingFlag=step.multiMatchingFlag)
                    imageShow = sourceImage.copy()
                    detectAreaList = []
                    pointList = []
                    valueList = []
                    for result in matchingResultList:
                        if not isRunningFlag and step.stepId == executedStepId:
                            imageShow = cv.rectangle(imageShow,
                                                     (result[0], result[1]),
                                                     (result[2], result[3]),
                                                     (0, 255, 0), 3)
                            imageShow = cv.putText(imageShow, "{}".format(round(result[4], 2)),
                                                   (result[0] + 10, result[1] + 45),
                                                   cv.FONT_HERSHEY_SIMPLEX,
                                                   _camera.parameter.textScale,
                                                   (0, 255, 0),
                                                   _camera.parameter.textThickness,
                                                   lineType=cv.LINE_AA)
                        detectAreaList.append((workingArea[0] + result[0], workingArea[1] + result[1],
                                               workingArea[0] + result[2], workingArea[1] + result[3]))
                        pointList.append((int((result[0] + result[2]) / 2), int((result[1] + result[3]) / 2)))
                        valueList.append(result[4])
                    self.resultList[index] = AlgorithmResult(stepId=index,
                                                             methodName=step.stepAlgorithmName,
                                                             workingArea=workingArea, basePoint=basePoint,
                                                             pointList=pointList,
                                                             detectAreaList=detectAreaList,
                                                             passed=True,
                                                             drawImage=imageShow,
                                                             valueList=valueList)

                    if len(matchingResultList) < 1:
                        if not isRunningFlag and step.stepId == executedStepId:
                            imageShow = cv.rectangle(imageShow,
                                                     (workingArea[0], workingArea[1]),
                                                     (workingArea[2], workingArea[3]),
                                                     (0, 0, 255), 3)

                        self.resultList[index] = AlgorithmResult(methodName=step.stepAlgorithmName, stepId=index,
                                                                 workingArea=workingArea, basePoint=basePoint,
                                                                 passed=False, drawImage=imageShow)
                    else:
                        imageResult = sourceImage[matchingResultList[0][1]: matchingResultList[0][3],
                                      matchingResultList[0][0]: matchingResultList[0][2]]
                        self.imageList[index] = imageResult.copy()
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(imageShow, False)

                # Original reference
                elif step.stepAlgorithmName == MethodList.originalReference.value:
                    refPointArea1 = []
                    refPointArea2 = []
                    refPointArea3 = []
                    for result in self.resultList:
                        if result.stepId == step.orRef1StepIdx:
                            refPointArea1 = result.detectAreaList
                        elif result.stepId == step.orRef2StepIdx:
                            refPointArea2 = result.detectAreaList
                        elif result.stepId == step.orRef3StepIdx:
                            refPointArea3 = result.detectAreaList

                    if len(refPointArea1) < 1:
                        text = "ERROR Algorithm {}. Step {} Cannot find reference position 1".format(
                            step.stepAlgorithmName, step.stepId)
                        self.mainWindow.runningTab.insertLog(text)
                        return False, [], text
                    if len(refPointArea2) < 1:
                        text = "ERROR Algorithm {}. Step {} Cannot find reference position 2".format(
                            step.stepAlgorithmName, step.stepId)
                        self.mainWindow.runningTab.insertLog(text)
                        return False, [], text
                    if len(refPointArea3) < 1:
                        text = "ERROR Algorithm {}. Step {} Cannot find reference position 3".format(
                            step.stepAlgorithmName, step.stepId)
                        self.mainWindow.runningTab.insertLog(text)
                        return False, [], text

                    refPoint1 = (int((refPointArea1[0][0] + refPointArea1[0][2]) / 2),
                                 int((refPointArea1[0][1] + refPointArea1[0][3]) / 2))
                    refPoint2 = (int((refPointArea2[0][0] + refPointArea2[0][2]) / 2),
                                 int((refPointArea2[0][1] + refPointArea2[0][3]) / 2))
                    refPoint3 = (int((refPointArea3[0][0] + refPointArea3[0][2]) / 2),
                                 int((refPointArea3[0][1] + refPointArea3[0][3]) / 2))

                    transformImage = ImageProcess.processAffineTransformImage(sourceImage=sourceImage,
                                                                              realRef=[refPoint1, refPoint2, refPoint3],
                                                                              originalRef=[step.originalRefPoint1,
                                                                                           step.originalRefPoint2,
                                                                                           step.originalRefPoint3])
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(transformImage)
                    self.imageList[step.stepId] = transformImage.copy()

                # Convert Color
                elif step.stepAlgorithmName == MethodList.cvtColor.value:
                    processImage = ImageProcess.processCvtColor(sourceImage=sourceImage, code=step.cvtColorCode)
                    if processImage is not None:
                        if not isRunningFlag and step.stepId == executedStepId:
                            self.mainWindow.showImage(processImage, False)
                        self.imageList[step.stepId] = processImage.copy()
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                                 methodName=step.stepAlgorithmName,
                                                                 workingArea=workingArea, basePoint=basePoint)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=False,
                                                                 methodName=step.stepAlgorithmName,
                                                                 workingArea=workingArea, basePoint=basePoint)
                        text = "ERROR Algorithm {}. Step {} Please check the image and the parameter setting! ".format(
                            step.stepAlgorithmName, step.stepId)
                        # messagebox.showerror("Convert Color Method", "Cannot apply Convert Color Algorithm!\nPlease check the image and the parameter setting!")
                        self.mainWindow.runningTab.insertLog(text)
                        return False, self.resultList, text
                # Black to white
                elif step.stepAlgorithmName == MethodList.black2White.value:
                    black2WhiteImage = sourceImage.copy()
                    black2WhiteImage[sourceImage == 0] = 255

                    self.imageList[index] = black2WhiteImage.copy()
                    self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             workingArea=workingArea, basePoint=basePoint)
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(black2WhiteImage)
                # White to black
                elif step.stepAlgorithmName == MethodList.white2Black.value:
                    white2BlackImage = sourceImage.copy()
                    white2BlackImage[sourceImage == 255] = 0

                    self.imageList[index] = white2BlackImage.copy()
                    self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             workingArea=workingArea, basePoint=basePoint)
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(white2BlackImage)
                # HLS range
                elif step.stepAlgorithmName == MethodList.hlsInRange.value:

                    hlsImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_BGR2HLS)

                    processImage = ImageProcess.processInRange(sourceImage=hlsImage,
                                                               lower=(
                                                               step.hlsLower[0], step.hlsLower[1], step.hlsLower[2]),
                                                               upper=(
                                                               step.hlsUpper[0], step.hlsUpper[1], step.hlsUpper[2]))

                    # self.imageList[index] = processImage.copy()
                    step_image_result = processImage
                    nonzeroAmount = ImageProcess.processCountNonzero(sourceImage=processImage)
                    print("nonzero: {}".format(nonzeroAmount))
                    if not isRunningFlag and step.stepId == executedStepId:
                        mask = ImageProcess.processBitwise_and(source1=hlsImage, source2=hlsImage, mask=processImage)
                        self.mainWindow.showImage(mask, False)
                        self.mainWindow.showBottomMiddleText(
                            "HLS range step {} = {}".format(step.stepId, nonzeroAmount))

                    if not step.minRange <= nonzeroAmount <= step.maxRange:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint,
                                                                 passed=False, value=nonzeroAmount,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=originalImage.copy())
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=True,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=originalImage.copy(), value=nonzeroAmount)
                # HSV range
                elif step.stepAlgorithmName == MethodList.hsvInRange.value:

                    hsvImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_BGR2HSV)

                    processImage = ImageProcess.processInRange(sourceImage=hsvImage,
                                                               lower=(
                                                               step.hsvLower[0], step.hsvLower[1], step.hsvLower[2]),
                                                               upper=(
                                                               step.hsvUpper[0], step.hsvUpper[1], step.hsvUpper[2]))

                    # self.imageList[index] = processImage.copy()
                    nonzeroAmount = ImageProcess.processCountNonzero(sourceImage=processImage)
                    print("nonzero: {}".format(nonzeroAmount))
                    if not isRunningFlag and step.stepId == executedStepId:
                        mask = ImageProcess.processBitwise_and(source1=hsvImage, source2=hsvImage, mask=processImage)
                        step_image_show = mask
                        # self.mainWindow.showImage(mask, False)
                        self.mainWindow.showBottomMiddleText(
                            "HSV range step {} = {}".format(step.stepId, nonzeroAmount))
                    step_image_result = processImage
                    if not step.minRange <= nonzeroAmount <= step.maxRange:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint,
                                                                 passed=False, value=nonzeroAmount,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=originalImage.copy())
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=True,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=originalImage.copy(), value=nonzeroAmount)
                # BGR range
                elif step.stepAlgorithmName == MethodList.bgrInRange.value:

                    processImage = ImageProcess.processInRange(sourceImage=sourceImage,
                                                               lower=(
                                                               step.bgrLower[0], step.bgrLower[1], step.bgrLower[2]),
                                                               upper=(
                                                               step.bgrUpper[0], step.bgrUpper[1], step.bgrUpper[2]))

                    # self.imageList[index] = processImage.copy()
                    nonzeroAmount = ImageProcess.processCountNonzero(sourceImage=processImage)
                    print("nonzero: {}".format(nonzeroAmount))
                    if not isRunningFlag and step.stepId == executedStepId:
                        # self.mainWindow.showImage(mask, False)
                        mask = ImageProcess.processBitwise_and(source1=sourceImage, source2=sourceImage,
                                                               mask=processImage)
                        step_image_show = mask
                        self.mainWindow.showBottomMiddleText(
                            "BGR range step {} = {}".format(step.stepId, nonzeroAmount))

                    step_image_result = processImage
                    if not step.minRange <= nonzeroAmount <= step.maxRange:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=False,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=originalImage.copy(), value=nonzeroAmount)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=True,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=originalImage.copy(), value=nonzeroAmount)
                # BGR + HSV range
                elif step.stepAlgorithmName == MethodList.bgr_hsvRange.value:
                    bgr_processImage = ImageProcess.processInRange(sourceImage=sourceImage,
                                                                   lower=(step.bgrLower[0], step.bgrLower[1],
                                                                          step.bgrLower[2]),
                                                                   upper=(step.bgrUpper[0], step.bgrUpper[1],
                                                                          step.bgrUpper[2]))

                    hsv_sourceImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_BGR2HSV)
                    hsv_processImage = ImageProcess.processInRange(sourceImage=hsv_sourceImage,
                                                                   lower=(step.hsvLower[0], step.hsvLower[1],
                                                                          step.hsvLower[2]),
                                                                   upper=(step.hsvUpper[0], step.hsvUpper[1],
                                                                          step.hsvUpper[2]))

                    processImage = ImageProcess.processBitwise_and(bgr_processImage, hsv_processImage)

                    mask = ImageProcess.processBitwise_and(source1=sourceImage, source2=sourceImage, mask=processImage)
                    # self.imageList[index] = processImage.copy()
                    nonzeroAmount = ImageProcess.processCountNonzero(sourceImage=processImage)
                    print("nonzero: {}".format(nonzeroAmount))
                    if not isRunningFlag and step.stepId == executedStepId:
                        # self.mainWindow.showImage(mask, False)
                        self.mainWindow.showBottomMiddleText(
                            "BGR + HSV range step {} = {}".format(step.stepId, nonzeroAmount))

                    if not step.minRange <= nonzeroAmount <= step.maxRange:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=False,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=originalImage.copy(), value=nonzeroAmount)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=True,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=originalImage.copy(), value=nonzeroAmount)
                    step_image_result = processImage
                    step_image_show = mask
                # BGR + HLS range
                elif step.stepAlgorithmName == MethodList.bgr_hlsRange.value:
                    bgr_processImage = ImageProcess.processInRange(sourceImage=sourceImage,
                                                                   lower=(step.bgrLower[0], step.bgrLower[1],
                                                                          step.bgrLower[2]),
                                                                   upper=(step.bgrUpper[0], step.bgrUpper[1],
                                                                          step.bgrUpper[2]))

                    hls_sourceImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_BGR2HLS)
                    hls_processImage = ImageProcess.processInRange(sourceImage=hls_sourceImage,
                                                                   lower=(step.hlsLower[0], step.hlsLower[1],
                                                                          step.hlsLower[2]),
                                                                   upper=(step.hlsUpper[0], step.hlsUpper[1],
                                                                          step.hlsUpper[2]))

                    processImage = ImageProcess.processBitwise_and(bgr_processImage, hls_processImage)

                    mask = ImageProcess.processBitwise_and(source1=sourceImage, source2=sourceImage, mask=processImage)
                    # self.imageList[index] = processImage.copy()
                    nonzeroAmount = ImageProcess.processCountNonzero(sourceImage=processImage)
                    print("nonzero: {}".format(nonzeroAmount))
                    if not isRunningFlag and step.stepId == executedStepId:
                        # self.mainWindow.showImage(mask, False)
                        self.mainWindow.showBottomMiddleText(
                            "BGR + HLS range step {} = {}".format(step.stepId, nonzeroAmount))
                    step_image_result = processImage
                    step_image_show = mask
                    if not step.minRange <= nonzeroAmount <= step.maxRange:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=False,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=originalImage.copy(), value=nonzeroAmount)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=True,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=originalImage.copy(), value=nonzeroAmount)
                # HSV + HLS range
                elif step.stepAlgorithmName == MethodList.hsv_hlsRange.value:

                    hls_sourceImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_BGR2HLS)
                    hls_processImage = ImageProcess.processInRange(sourceImage=hls_sourceImage,
                                                                   lower=(step.hlsLower[0], step.hlsLower[1],
                                                                          step.hlsLower[2]),
                                                                   upper=(step.hlsUpper[0], step.hlsUpper[1],
                                                                          step.hlsUpper[2]))

                    hsv_sourceImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_BGR2HSV)

                    hsv_processImage = ImageProcess.processInRange(sourceImage=hsv_sourceImage,
                                                                   lower=(step.hsvLower[0], step.hsvLower[1],
                                                                          step.hsvLower[2]),
                                                                   upper=(step.hsvUpper[0], step.hsvUpper[1],
                                                                          step.hsvUpper[2]))

                    processImage = ImageProcess.processBitwise_and(hls_processImage, hsv_processImage)

                    mask = ImageProcess.processBitwise_and(source1=sourceImage, source2=sourceImage, mask=processImage)
                    # self.imageList[index] = processImage.copy()
                    nonzeroAmount = ImageProcess.processCountNonzero(sourceImage=processImage)
                    print("nonzero: {}".format(nonzeroAmount))
                    if not isRunningFlag and step.stepId == executedStepId:
                        # self.mainWindow.showImage(mask, False)
                        self.mainWindow.showBottomMiddleText(
                            "HSV + HLS range step {} = {}".format(step.stepId, nonzeroAmount))
                    step_image_result = processImage
                    step_image_show = mask
                    if not step.minRange <= nonzeroAmount <= step.maxRange:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=False,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=originalImage.copy(), value=nonzeroAmount)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=True,
                                                                 methodName=step.stepAlgorithmName,
                                                                 drawImage=originalImage.copy(), value=nonzeroAmount)
                # Detect color
                elif step.stepAlgorithmName == MethodList.colorDetect.value:
                    lower = (int(step.averageColor[0] - step.bgrToleranceRange[0]),
                             int(step.averageColor[1] - step.bgrToleranceRange[1]),
                             int(step.averageColor[2] - step.bgrToleranceRange[2]))

                    upper = (int(step.averageColor[0] + step.bgrToleranceRange[0]),
                             int(step.averageColor[1] + step.bgrToleranceRange[1]),
                             int(step.averageColor[2] + step.bgrToleranceRange[2]))

                    # sourceImage = sourceImage[workingArea[1]:workingArea[3], workingArea[0]:workingArea[2]]

                    processImage = ImageProcess.processInRange(sourceImage=sourceImage, lower=lower, upper=upper)

                    mask = ImageProcess.processBitwise_and(source1=sourceImage, source2=sourceImage, mask=processImage)
                    # self.imageList[index] = processImage.copy()
                    nonzeroAmount = ImageProcess.processCountNonzero(sourceImage=processImage)
                    print("nonzero: {}".format(nonzeroAmount))
                    if not isRunningFlag and step.stepId == executedStepId:
                        # self.mainWindow.showImage(mask, False)
                        self.mainWindow.showBottomMiddleText(
                            "Detect color step {} = {}".format(step.stepId, nonzeroAmount))
                    step_image_result = processImage
                    step_image_show = mask
                    if nonzeroAmount < step.nonzeroThresh:
                        self.resultList[index] = AlgorithmResult(stepId=index, methodName=step.stepAlgorithmName,
                                                                 workingArea=workingArea, basePoint=basePoint,
                                                                 passed=False, drawImage=originalImage.copy(),
                                                                 value=nonzeroAmount)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, methodName=step.stepAlgorithmName,
                                                                 workingArea=workingArea, basePoint=basePoint,
                                                                 passed=True, drawImage=originalImage.copy(),
                                                                 value=nonzeroAmount)

                # in range color
                elif step.stepAlgorithmName == MethodList.inRange.value:
                    lower = (int(step.averageColor[0] - step.bgrToleranceRange[0]),
                             int(step.averageColor[1] - step.bgrToleranceRange[1]),
                             int(step.averageColor[2] - step.bgrToleranceRange[2]))

                    upper = (int(step.averageColor[0] + step.bgrToleranceRange[0]),
                             int(step.averageColor[1] + step.bgrToleranceRange[1]),
                             int(step.averageColor[2] + step.bgrToleranceRange[2]))

                    # sourceImage = sourceImage[workingArea[1]:workingArea[3],
                    #               workingArea[0]:workingArea[2]]
                    processImage = ImageProcess.processInRange(sourceImage=sourceImage, lower=lower, upper=upper)
                    mask = ImageProcess.processBitwise_and(source1=sourceImage, source2=sourceImage, mask=processImage)
                    self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             workingArea=workingArea, basePoint=basePoint)
                    # self.imageList[step.stepId] = processImage.copy()
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(mask, False)
                    step_image_result = processImage
                    step_image_show = mask
                # Count nonzero
                elif step.stepAlgorithmName == MethodList.countNonzero.value:
                    nonzeroAmount = ImageProcess.processCountNonzero(sourceImage=sourceImage)
                    print("nonzero: {}".format(nonzeroAmount))

                    # workingArea = self.algorithmParameter.steps[step.resourceIndex[0]].workingArea
                    # self.imageList[index] = sourceImage.copy()
                    if not step.minRange <= nonzeroAmount <= step.maxRange:
                        self.resultList[index] = AlgorithmResult(stepId=index, methodName=step.stepAlgorithmName,
                                                                 workingArea=workingArea, basePoint=basePoint,
                                                                 passed=False,
                                                                 drawImage=sourceImage.copy(), value=nonzeroAmount)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, methodName=step.stepAlgorithmName,
                                                                 workingArea=workingArea, basePoint=basePoint,
                                                                 passed=True,
                                                                 drawImage=sourceImage.copy(), value=nonzeroAmount)
                    # if nonzeroAmount < step.nonzeroThresh:
                    #     self.resultList[index] = AlgorithmResult(stepId=index, methodName=step.stepAlgorithmName,
                    #                                       workingArea=workingArea, basePoint=basePoint, passed=False,
                    #                                       drawImage=sourceImage.copy(), value=nonzeroAmount)
                    # else:
                    #     self.resultList[index] = AlgorithmResult(stepId=index, methodName=step.stepAlgorithmName,
                    #                                       workingArea=workingArea, basePoint=basePoint, passed=True,
                    #                                       drawImage=sourceImage.copy(), value=nonzeroAmount)
                    step_image_show = step_image_result = sourceImage

                    if not isRunningFlag and step.stepId == executedStepId:
                        #     self.mainWindow.showImage(sourceImage, False)
                        self.mainWindow.showBottomMiddleText(
                            "Count nonzero step {} = {}".format(step.stepId, nonzeroAmount))

                # Threshold
                elif step.stepAlgorithmName == MethodList.threshold.value:
                    if step.thresholdType2 == ThresholdCode._None.value:
                        ret, processImage = ImageProcess.processThreshold(sourceImage, step.threshold_thresh_val,
                                                                          step.maxThresholdValue, step.thresholdType1)
                    else:
                        ret, processImage = ImageProcess.processThreshold(sourceImage, step.threshold_thresh_val,
                                                                          step.maxThresholdValue,
                                                                          step.thresholdType1 + step.thresholdType2)
                    if ret:
                        # self.imageList[index] = processImage
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                                 methodName=step.stepAlgorithmName,
                                                                 workingArea=workingArea, basePoint=basePoint,
                                                                 drawImage=processImage)
                        # if not isRunningFlag and step.stepId == executedStepId:
                        #     self.mainWindow.showImage(processImage, False)
                        step_image_show = step_image_result = processImage


                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=False,
                                                                 methodName=step.stepAlgorithmName,
                                                                 workingArea=workingArea, basePoint=basePoint)
                        # messagebox.showerror("Theshold Method", "Cannot apply Threshold Algorithm!\nPlease check the image and the parameter setting!")
                        text = "ERROR Algorithm {}. Step {} Please check the image and the parameter setting!".format(
                            step.stepAlgorithmName, step.stepId)
                        self.mainWindow.runningTab.insertLog(text)
                        return False, self.resultList, text
                # Adaptive Thresh holding
                elif step.stepAlgorithmName == MethodList.adaptiveThreshold.value:
                    adaptiveThresholdImage = ImageProcess.processAdaptiveThreshold(sourceImage=sourceImage,
                                                                                   maxValue=step.maxThresholdValue,
                                                                                   thresholdType=step.thresholdType1,
                                                                                   adaptiveMethod=step.adaptiveMode,
                                                                                   blockSize=step.blockSize,
                                                                                   C=step.adaptiveC)

                    # self.imageList[index] = adaptiveThresholdImage.copy()
                    self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             workingArea=workingArea, basePoint=basePoint)
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(adaptiveThresholdImage)
                    step_image_show = step_image_result = adaptiveThresholdImage

                # Canny
                elif step.stepAlgorithmName == MethodList.canny.value:
                    cannyImage = ImageProcess.processCanny(sourceImage, minThresh=step.minThresh,
                                                           maxThresh=step.maxThresholdValue,
                                                           apertureSize=step.canny_kernel_size)

                    self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             workingArea=workingArea, basePoint=basePoint)
                    # self.imageList[index] = cannyImage.copy()
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(cannyImage)
                    step_image_show = step_image_result = cannyImage

                # Hough lines
                elif step.stepAlgorithmName == MethodList.houghLines.value:
                    theta = step.hl_theta * np.pi / 180
                    minTheta = step.hl_min_theta * np.pi / 180
                    maxTheta = step.hl_max_theta * np.pi / 180

                    lineList = ImageProcess.processHoughLine(sourceImage=sourceImage,
                                                             workingArea=workingArea,
                                                             rho=step.hl_rho,
                                                             theta=theta,
                                                             threshold=step.hl_threshold,
                                                             lines=None,
                                                             srn=step.hl_srn,
                                                             stn=step.hl_stn,
                                                             min_theta=minTheta,
                                                             max_theta=maxTheta)
                    houghLinesImage = sourceImage.copy()
                    if len(houghLinesImage.shape) < 3:
                        houghLinesImage = ImageProcess.processCvtColor(houghLinesImage, cv.COLOR_GRAY2BGR)
                    for line in lineList:
                        cv.line(houghLinesImage, line[0], line[1], (0, 255, 0), _camera.parameter.textThickness,
                                lineType=cv.LINE_AA)
                    self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             workingArea=workingArea, basePoint=basePoint)
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(houghLinesImage)
                    step_image_show = step_image_result = houghLinesImage

                # Probabilistic Hough lines
                elif step.stepAlgorithmName == MethodList.houghLinesP.value:
                    theta = step.hl_theta * np.pi / 180

                    lineList = ImageProcess.processHoughLinesP(sourceImage=sourceImage,
                                                               rho=step.hl_rho,
                                                               theta=theta,
                                                               threshold=step.hl_threshold,
                                                               lines=None,
                                                               minLineLength=step.hl_min_length,
                                                               maxLineGap=step.hl_max_gap)
                    houghLinesPImage = sourceImage.copy()
                    if len(houghLinesPImage.shape) < 3:
                        houghLinesPImage = ImageProcess.processCvtColor(houghLinesPImage, cv.COLOR_GRAY2BGR)
                    for line in lineList:
                        cv.line(houghLinesPImage, line[0], line[1], (0, 255, 0), _camera.parameter.textThickness,
                                lineType=cv.LINE_AA)
                    self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             workingArea=workingArea, basePoint=basePoint)
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(houghLinesPImage)
                    step_image_show = step_image_result = houghLinesPImage

                # Hough circle
                elif step.stepAlgorithmName == MethodList.houghCircle.value:
                    houghCircleImage, circles = ImageProcess.processHoughCircle(sourceImage,
                                                                                workingArea=workingArea,
                                                                                minDist=step.houghCircleMinDist,
                                                                                param1=step.houghCircleParm1,
                                                                                param2=step.houghCircleParm2,
                                                                                minRadius=step.houghCircleMinRadius,
                                                                                maxRadius=step.houghCircleMaxRadius)

                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(houghCircleImage)
                    step_image_show = step_image_result = houghCircleImage

                    if len(circles) > 0:
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                                 methodName=step.stepAlgorithmName,
                                                                 workingArea=workingArea, basePoint=basePoint,
                                                                 drawImage=houghCircleImage, circleList=circles)
                        print("Circle List: {}".format(circles))
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=False,
                                                                 methodName=step.stepAlgorithmName,
                                                                 workingArea=workingArea, basePoint=basePoint,
                                                                 drawImage=houghCircleImage,
                                                                 circleList=circles)

                # Average hough circle
                elif step.stepAlgorithmName == MethodList.averageHoughCircle.value:
                    circleList, averageImage, houghCircleImage = ImageProcess.processAverageHoughCircle(sourceImage,
                                                                                                        workingArea=workingArea,
                                                                                                        minDist=step.houghCircleMinDist,
                                                                                                        param1=step.houghCircleParm1,
                                                                                                        param2=step.houghCircleParm2,
                                                                                                        minRadius=step.houghCircleMinRadius,
                                                                                                        maxRadius=step.houghCircleMaxRadius,
                                                                                                        betweenDist=step.houghCircleBetweenDist,
                                                                                                        trustNumber=step.houghCircleTrustNumber)
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(averageImage)
                    step_image_show = step_image_result = averageImage
                    if circleList is None:
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=False,
                                                                 methodName=step.stepAlgorithmName,
                                                                 workingArea=workingArea, basePoint=basePoint,
                                                                 drawImage=averageImage, circleList=circleList)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, passed=True,
                                                                 methodName=step.stepAlgorithmName,
                                                                 workingArea=workingArea, basePoint=basePoint,
                                                                 drawImage=averageImage,
                                                                 circleList=circleList)

                # # detect bolt using yolo v4 with pytorch
                # elif step.stepAlgorithmName == MethodList.boltHeaderDetectionWithPytorchYolo4.value:
                #     boltHeaderImage, boxes = BoltDetectionProcess.doProcess(image=sourceImage, thresh=0.99, nmsThesh=0.4, use_cuda=False, _model=None)
                #     if not isRunningFlag and step.stepId == executedStepId:
                #         self.mainWindow.showImage(boltHeaderImage)
                #     if len(boxes) > 0:
                #         self.resultList[index] = AlgorithmResult(stepId=index, passed=True, methodName=step.stepAlgorithmName,
                #                                           workingArea=workingArea, drawImage=boltHeaderImage,
                #                                           detectAreaList=boxes)
                #     else:
                #         self.resultList[index] = AlgorithmResult(stepId=index, passed=False, methodName=step.stepAlgorithmName,
                #                                           workingArea=workingArea, drawImage=boltHeaderImage,
                #                                           detectAreaList=boxes)

                # Get system offset
                elif step.stepAlgorithmName == MethodList.getSystemOffset.value:
                    (coefficient, beginCenter, endCenter), offsetCenter = ImageProcess.getSystemOffset(
                        sourceImage=sourceImage)
                # Focus checking
                elif step.stepAlgorithmName == MethodList.focusChecking.value:
                    variance_of_laplacian = ImageProcess.getVarianceOfLaplacian(sourceImage)
                    if variance_of_laplacian > step.threshFocus:
                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 methodName=step.stepAlgorithmName,
                                                                 value=variance_of_laplacian, stepId=step.stepId,
                                                                 passed=True)
                    else:
                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 methodName=step.stepAlgorithmName,
                                                                 value=variance_of_laplacian, stepId=step.stepId,
                                                                 passed=False)
                    step_image_result = step_image_show = sourceImage

                # Subtraction MOG2
                elif step.stepAlgorithmName == MethodList.subtractionMog2.value:
                    try:
                        if step.bs_process_image_index == -1:
                            processImage = originalImage.copy()
                        elif step.bs_process_image_index == -4:
                            refImagePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                                                   "/",
                                                                   self.algorithmParameter.name,
                                                                   "/",
                                                                   "imageReference_",
                                                                   self.algorithmParameter.refImageName,
                                                                   ".png")
                            try:
                                processImage = cv.imdecode(np.fromfile(refImagePath, dtype=np.uint8), cv.IMREAD_COLOR)
                            except Exception as error:
                                text = "ERROR Algorithm {}. Step {} Please check the image reference. Detail {}".format(
                                    step.stepAlgorithmName, step.stepId, error)
                                self.mainWindow.runningTab.insertLog(text)
                                return False, self.resultList, text
                        elif step.bs_process_image_index == -3:
                            templatePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                                                   "/",
                                                                   self.algorithmParameter.name,
                                                                   "/",
                                                                   "imageTemplate_",
                                                                   step.templateName,
                                                                   ".png")
                            try:
                                processImage = cv.imdecode(np.fromfile(templatePath, dtype=np.uint8), cv.IMREAD_COLOR)
                            except Exception as error:
                                text = "ERROR Algorithm {}. Step {} Please check the image template".format(
                                    step.stepAlgorithmName, step.stepId)
                                self.mainWindow.runningTab.insertLog(text)
                                return False, self.resultList, text
                        elif step.bs_process_image_index == -2:
                            processImage = None
                        else:
                            processImage = self.imageList[step.bs_process_image_index].copy()

                        # if step.bs_processWorkingArea is None:
                        #     bs_processWorkingArea = (0, 0, processImage.shape[1], processImage.shape[0])
                        # else:
                        #     bs_processWorkingArea = step.bs_processWorkingArea
                        #
                        # # validate working area:
                        # if bs_processWorkingArea[3] - bs_processWorkingArea[1] > processImage.shape[0] \
                        #         or bs_processWorkingArea[2] - bs_processWorkingArea[0] > processImage.shape[1] \
                        #         or bs_processWorkingArea[3] > processImage.shape[0] \
                        #         or bs_processWorkingArea[2] > processImage.shape[1]:
                        #     # messagebox.showerror("Step {}".format(step.stepId),
                        #     #                      "Step {} has working area out of image".format(step.stepId))
                        #     text = "ERROR Algorithm {}. Step {} has working area out of image".format(
                        #         step.stepAlgorithmName, step.stepId)
                        #
                        #     self.mainWindow.runningTab.insertLog(text)
                        #     return False, self.resultList, text

                        processImage = processImage[workingArea[1]:workingArea[3],
                                       workingArea[0]:workingArea[2]]

                        backSub = cv.createBackgroundSubtractorMOG2(history=step.bs_history_frame_num,
                                                                    varThreshold=step.bs_dist2Threshold,
                                                                    detectShadows=step.bs_detect_shadow)
                        mog2Result = backSub.apply(sourceImage)
                        mog2Result = backSub.apply(processImage)
                        # # backSub.apply(sourceImage)
                        # ret,(knnResult, backSub), text = ImageProcess.processBS_KNN(sourceImage=sourceImage,
                        #                                                             history=step.bs_history_frame_num,
                        #                                                             dist2Threshold=step.bs_dist2Threshold,
                        #                                                             detectShadows=step.bs_detect_shadow)
                        # if ret:
                        #     ret,(knnResult, backSub), text = ImageProcess.processBS_KNN(sourceImage=processImage,
                        #                                                             existBackSub=backSub)
                        # if ret:
                        # self.imageList[index] = mog2Result.copy()
                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 methodName=step.stepAlgorithmName, stepId=step.stepId,
                                                                 passed=True)
                        # if not isRunningFlag and step.stepId == executedStepId:
                        #     self.mainWindow.showImage(mog2Result)
                        step_image_result = step_image_show = mog2Result

                    except Exception as error:
                        text = "ERROR Algorithm {}. Step {} Please Check the parameter! Detail: {}".format(
                            step.stepAlgorithmName, step.stepId, error)
                        self.mainWindow.runningTab.insertLog(text)
                        return False, self.resultList, text
                # subtraction KNN
                elif step.stepAlgorithmName == MethodList.subtractionKNN.value:
                    try:
                        ret, processImage, text = self.getSourceImage(imageIndex=step.bs_process_image_index, step=step,
                                                                      originalImage=originalImage)
                        if not ret:
                            return ret, self.resultList, text
                        backSub = cv.createBackgroundSubtractorKNN(history=step.bs_history_frame_num,
                                                                   dist2Threshold=step.bs_dist2Threshold,
                                                                   detectShadows=step.bs_detect_shadow)
                        knn_Result = backSub.apply(sourceImage)
                        knn_Result = backSub.apply(processImage)
                        # # backSub.apply(sourceImage)
                        # ret,(knnResult, backSub), text = ImageProcess.processBS_KNN(sourceImage=sourceImage,
                        #                                                             history=step.bs_history_frame_num,
                        #                                                             dist2Threshold=step.bs_dist2Threshold,
                        #                                                             detectShadows=step.bs_detect_shadow)
                        # if ret:
                        #     ret,(knnResult, backSub), text = ImageProcess.processBS_KNN(sourceImage=processImage,
                        #                                                             existBackSub=backSub)
                        # if ret:
                        # self.imageList[index] = knn_Result.copy()
                        # if not isRunningFlag and step.stepId == executedStepId:
                        #     self.mainWindow.showImage(knn_Result)
                        step_image_result = step_image_show = knn_Result

                    except Exception as error:
                        text = "ERROR Algorithm {}. Step {} Please Check the parameter! Detail: {}".format(
                            step.stepAlgorithmName, step.stepId, error)
                        self.mainWindow.runningTab.insertLog(text)
                        return False, self.resultList, text
                # translation image
                elif step.stepAlgorithmName == MethodList.translation.value:

                    try:
                        ret, translationImage, text = ImageProcess.processTransMoveImage(sourceImage=sourceImage,
                                                                                         move_x=step.trans_move_x,
                                                                                         move_y=step.trans_move_y)
                        if ret:
                            # self.imageList[index] = translationImage.copy()
                            # if not isRunningFlag and step.stepId == executedStepId:
                            #     self.mainWindow.showImage(translationImage)
                            step_image_result = step_image_show = translationImage

                        else:
                            self.mainWindow.runningTab.insertLog(text)
                            return False, self.resultList, text
                    except Exception as error:
                        text = "ERROR Algorithm {}. Step {} Please Check the parameter! Detail: {}".format(
                            step.stepAlgorithmName, step.stepId, error)
                        self.mainWindow.runningTab.insertLog(text)
                        return False, self.resultList, text
                # reference translation
                elif step.stepAlgorithmName == MethodList.referenceTranslation.value:
                    baseIndex, baseParm = step.rt_baseSource
                    destIndex, destParm = step.rt_destSource

                    baseResult: AlgorithmResult = self.getResultWithId(stepId=baseIndex,
                                                                       resultList=self.resultList)
                    basePoint = baseResult.getValue(baseParm)

                    destResult: AlgorithmResult = self.getResultWithId(stepId=destIndex,
                                                                       resultList=self.resultList)
                    destPoint = destResult.getValue(destParm)
                    moveX = 0
                    moveY = 0
                    if step.rt_type == RF_Type.top.value or step.rt_type == RF_Type.bottom.value:
                        moveY = basePoint[1] - destPoint[1]
                    elif step.rt_type == RF_Type.right.value or step.rt_type == RF_Type.left.value:
                        moveX = basePoint[0] - destPoint[0]
                    else:
                        moveX = basePoint[0] - destPoint[0]
                        moveY = basePoint[1] - destPoint[1]

                    ret, rt_image, text = ImageProcess.processTransMoveImage(sourceImage=sourceImage, move_x=moveX,
                                                                             move_y=moveY)
                    if not ret:
                        text = "ERROR Algorithm {}. Step {}. ".format(
                            step.stepAlgorithmName, step.stepId, text)
                        self.mainWindow.runningTab.insertLog(text)
                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 passed=False,
                                                                 stepId=step.stepId, methodName=step.stepAlgorithmName)

                        return False, self.resultList, text
                    # self.imageList[index] = rt_image.copy()
                    self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint, passed=True,
                                                             stepId=step.stepId, methodName=step.stepAlgorithmName)
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(rt_image)
                    step_image_result = step_image_show = rt_image

                # Draw circle
                elif step.stepAlgorithmName == MethodList.drawCircle.value:
                    stepId, paramName = step.dc_circleInput
                    try:
                        circleImage = sourceImage
                        if stepId >= 0:
                            sourceInput: AlgorithmResult = self.getResultWithId(stepId=stepId,
                                                                                resultList=self.resultList)
                            point = sourceInput.getValue(paramName)
                            if paramName == AlgorithmResultKey.point.value:
                                circleImage = cv.circle(sourceImage, center=point,
                                                        radius=step.dc_radius, color=(255, 255, 255),
                                                        thickness=step.dc_thickness, lineType=cv.LINE_AA)
                            elif paramName == AlgorithmResultKey.circle.value:
                                circleImage = cv.circle(sourceImage, center=point[0],
                                                        radius=point[1], color=(255, 255, 255),
                                                        thickness=step.dc_thickness, lineType=cv.LINE_AA)
                        else:
                            circleImage = cv.circle(sourceImage, center=step.dc_center,
                                                    radius=step.dc_radius, color=(255, 255, 255),
                                                    thickness=step.dc_thickness, lineType=cv.LINE_AA)
                        # self.imageList[index] = circleImage.copy()
                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 passed=True,
                                                                 stepId=step.stepId, methodName=step.stepAlgorithmName)
                        # if not isRunningFlag and step.stepId == executedStepId:
                        #     self.mainWindow.showImage(circleImage)
                        step_image_result = step_image_show = circleImage
                    except Exception as error:
                        text = "ERROR Algorithm {}. Step {} Check the parameter Detail: ".format(
                            step.stepAlgorithmName, step.stepId, error)
                        self.mainWindow.runningTab.insertLog(text)
                        return False, self.resultList, text
                # Get extreme
                elif step.stepAlgorithmName == MethodList.getExtreme.value:
                    stepId, paramName = step.ge_sourceContour
                    sourceInput: AlgorithmResult = self.getResultWithId(stepId=stepId, resultList=self.resultList)
                    contourList = sourceInput.getValue(paramName)
                    extTop, extRight, extBot, extLeft = ImageProcess.processFindExtremeOfContourList(contourList)
                    drawImage = sourceImage.copy()
                    # self.imageList[index] = sourceImage.copy()
                    if step.ge_extremeType == RF_Type.left.value:
                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 passed=True,
                                                                 point=extLeft, stepId=step.stepId,
                                                                 methodName=step.stepAlgorithmName)
                        if not isRunningFlag and step.stepId == executedStepId:
                            cv.circle(drawImage, extLeft, _camera.parameter.textThickness, (0, 255, 0), -1,
                                      lineType=cv.LINE_AA)
                            # self.mainWindow.showImage(drawImage)
                    elif step.ge_extremeType == RF_Type.top.value:
                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 passed=True,
                                                                 point=extTop, stepId=step.stepId,
                                                                 methodName=step.stepAlgorithmName)
                        if not isRunningFlag and step.stepId == executedStepId:
                            cv.circle(drawImage, extTop, _camera.parameter.textThickness, (0, 255, 0), -1,
                                      lineType=cv.LINE_AA)
                            # self.mainWindow.showImage(drawImage)
                    elif step.ge_extremeType == RF_Type.right.value:
                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 passed=True,
                                                                 point=extRight, stepId=step.stepId,
                                                                 methodName=step.stepAlgorithmName)
                        if not isRunningFlag and step.stepId == executedStepId:
                            cv.circle(drawImage, extRight, _camera.parameter.textThickness, (0, 255, 0), -1,
                                      lineType=cv.LINE_AA)
                            # self.mainWindow.showImage(drawImage)
                    elif step.ge_extremeType == RF_Type.bottom.value:
                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 passed=True,
                                                                 point=extBot, stepId=step.stepId,
                                                                 methodName=step.stepAlgorithmName)
                        if not isRunningFlag and step.stepId == executedStepId:
                            cv.circle(drawImage, extBot, _camera.parameter.textThickness, (0, 255, 0), -1,
                                      lineType=cv.LINE_AA)
                            # self.mainWindow.showImage(drawImage)
                    elif step.ge_extremeType == RF_Type.all.value:
                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 passed=True,
                                                                 extreme=(extTop, extRight, extBot, extLeft),
                                                                 stepId=step.stepId,
                                                                 methodName=step.stepAlgorithmName)
                        if not isRunningFlag and step.stepId == executedStepId:
                            cv.circle(drawImage, extLeft, _camera.parameter.textThickness, (0, 255, 0), -1,
                                      lineType=cv.LINE_AA)
                            cv.circle(drawImage, extTop, _camera.parameter.textThickness, (0, 255, 0), -1,
                                      lineType=cv.LINE_AA)
                            cv.circle(drawImage, extRight, _camera.parameter.textThickness, (0, 255, 0), -1,
                                      lineType=cv.LINE_AA)
                            cv.circle(drawImage, extBot, _camera.parameter.textThickness, (0, 255, 0), -1,
                                      lineType=cv.LINE_AA)
                            # self.mainWindow.showImage(drawImage)
                    step_image_result = sourceImage
                    step_image_show = drawImage
                    # Paint
                elif step.stepAlgorithmName == MethodList.paint.value:
                    ret, paintImage, text = ImageProcess.paint(sourceImage=sourceImage,
                                                               paintArea=step.paintArea,
                                                               color=step.paintColor)

                    if ret:
                        # self.imageList[index] = paintImage.copy()
                        # if not isRunningFlag and executedStepId == step.stepId:
                        #     self.mainWindow.showImage(paintImage)
                        step_image_show = step_image_result = paintImage

                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 passed=True,
                                                                 methodName=step.stepAlgorithmName)
                    else:
                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 passed=False,
                                                                 methodName=step.stepAlgorithmName)
                        self.mainWindow.runningTab.insertLog(text)
                # Min area rectangle
                elif step.stepAlgorithmName == MethodList.getMinAreaRect.value:
                    centerList = []
                    rotationList = []
                    stepId, paramName = step.mar_source_contours
                    sourceInput: AlgorithmResult = self.getResultWithId(stepId=stepId, resultList=self.resultList)
                    contourList = sourceInput.getValue(paramName)
                    boxList = []
                    for contour in contourList:
                        ret, minRect, text = ImageProcess.getMinAreaRect(contour=contour)
                        if ret:
                            boxList.append(minRect)
                            box, angle, center = minRect
                            reference = ([0, 0], [1, 0])  # horizontal edge

                            edge1 = ImageProcess.calculateDistanceBy2Points(box[0], box[1])
                            edge2 = ImageProcess.calculateDistanceBy2Points(box[0], box[3])
                            w = edge1
                            h = edge2
                            usedLine = (box[0], box[1])
                            if edge2 < edge1:
                                w = edge2
                                h = edge1
                                usedLine = (box[0], box[3])

                            angle = ImageProcess.findAngleByLine(reference, usedLine)
                            centerList.append(center)
                            rotationList.append((center, angle))
                            if not isRunningFlag and step.stepId == executedStepId:
                                pointX = (center[0] + 50, center[1])
                                pointY = (center[0], center[1] - 50)

                                ret, pointX, text = ImageProcess.rotatePoint(origin=center, point=pointX, angle=angle)
                                ret, pointY, text = ImageProcess.rotatePoint(origin=center, point=pointY, angle=angle)
                                cv.arrowedLine(sourceImage, center, pointX, (255, 255, 0), 2, cv.LINE_AA)
                                cv.arrowedLine(sourceImage, center, pointY, (255, 255, 0), 2, cv.LINE_AA)

                                for i in range(4):
                                    cv.line(sourceImage, box[i], box[(i + 1) % 4], (0, 255, 0), 2, cv.LINE_AA)

                                cv.putText(sourceImage, "{}".format(angle), center, cv.FONT_HERSHEY_SIMPLEX,
                                           _camera.parameter.textScale, (0, 255, 255), _camera.parameter.textThickness,
                                           lineType=cv.LINE_AA)

                        else:
                            self.mainWindow.runningTab.insertLog(text)
                            return False, self.resultList, text
                    # self.imageList[index] = sourceImage.copy()
                    self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                             stepId=step.stepId,
                                                             boxList=boxList, passed=True, contourList=contourList,
                                                             pointList=centerList, rotationList=rotationList)
                    step_image_show = step_image_result = sourceImage
                    if not isRunningFlag and step.stepId == executedStepId:
                        # self.mainWindow.showImage(sourceImage)

                        try:
                            self.mainWindow.showBottomMiddleText(f"(w, h, angle) = ({w}, {h}, {angle})")
                        except:
                            pass

                elif step.stepAlgorithmName == MethodList.dataMatrixReaderWithArea.value:
                    stepId, paramName = step.get_min_area_box
                    sourceInput: AlgorithmResult = self.getResultWithId(stepId=stepId, resultList=self.resultList)
                    list_result_data = []
                    box_list = sourceInput.getValue(paramName)
                    image_last = originalImage
                    for dmcode in box_list:
                        pos = dmcode[0]
                        angle = dmcode[1]
                        pts = np.array(pos, dtype="float32")
                        rect = cv.boundingRect(pts)
                        x, y, w, h = rect
                        cv.rectangle(image_last, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=5)
                        cropped = image_last[y:y + h, x:x + w].copy()
                        pts = pts - pts.min(axis=0)  # Offset points so they are in the cropped image frame
                        dst = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype="float32")
                        M = cv.getPerspectiveTransform(pts, dst)
                        warped = cv.warpPerspective(cropped, M, (w, h))

                        ret, dataMatrixCodes, text = ImageProcess.readDataMatrixCode(sourceImage=warped)
                        for dataMatrixCode in dataMatrixCodes:
                            barcodeData = dataMatrixCode.data.decode("utf-8")
                            barcodeInfo = barcodeData.split(" ")
                            text = ""
                            for info in barcodeInfo:
                                if info != "":
                                    text = text + info + ","
                            list_result_data.append((pos, text))
                            self.mainWindow.runningTab.insertLog("Data matrix info: {}".format(text))
                            self.mainWindow.showBottomMiddleText("Data matrix info: {}".format(text))
                    print(list_result_data)
                    step_image_show = step_image_result = image_last
                # Barcode Reader
                elif step.stepAlgorithmName == MethodList.barcodeReader.value:
                    # return False, self.resultList, text

                    ret, barcodes, text = ImageProcess.readBarcode(sourceImage=sourceImage)
                    drawImage = sourceImage.copy()
                    barcodeInfoList = []
                    if ret:
                        for barcode in barcodes:
                            x, y, w, h = barcode.rect
                            cv.rectangle(drawImage, (x, y), (x + w, y + h), (0, 0, 255),
                                         _camera.parameter.textThickness,
                                         lineType=cv.LINE_AA)
                            barcodeData = barcode.data.decode("utf-8")
                            barcodeType = barcode.type
                            barcodeInfo = barcodeData.split(" ")
                            text = ""
                            for info in barcodeInfo:
                                if info != "":
                                    text = text + info + ","
                            self.mainWindow.runningTab.insertLog("Barcode info: {}\nType: {}".format(text, barcodeType))
                            self.mainWindow.showBottomMiddleText("Barcode info: {}".format(text))
                            barcodeInfoList.append((barcodeInfo, barcode.rect))
                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 stepId=step.stepId,
                                                                 methodName=step.stepAlgorithmName, passed=True,
                                                                 barcodeList=barcodeInfoList)
                        # if not isRunningFlag and step.stepId == executedStepId:
                        #     self.mainWindow.showImage(drawImage)
                        # self.imageList[index] = drawImage.copy()
                        step_image_show = step_image_result = drawImage

                    else:
                        self.mainWindow.runningTab.insertLog(text)
                        return False, self.resultList, text
                # Data matrix reader
                elif step.stepAlgorithmName == MethodList.dataMatrixReader.value:
                    # return False, self.resultList, text
                    ret, dataMatrixCodes, text = ImageProcess.readDataMatrixCode(sourceImage=sourceImage)
                    drawImage = sourceImage.copy()
                    barcodeInfoList = []
                    if ret:
                        if len(drawImage.shape) < 3:
                            drawImage = ImageProcess.processCvtColor(drawImage, cv.COLOR_GRAY2BGR)
                        centerY = int(drawImage.shape[0] / 2)
                        for dataMatrixCode in dataMatrixCodes:
                            x, y, w, h = dataMatrixCode.rect

                            y = y - 2 * (y - centerY)

                            cv.rectangle(drawImage, (x, y), (x + w, y + abs(h)), (0, 0, 255),
                                         _camera.parameter.textThickness,
                                         lineType=cv.LINE_AA)
                            barcodeData = dataMatrixCode.data.decode("utf-8")
                            barcodeInfo = barcodeData.split(" ")
                            text = ""
                            for info in barcodeInfo:
                                if info != "":
                                    text = text + info + ","
                            self.mainWindow.runningTab.insertLog("Data matrix info: {}".format(text))
                            self.mainWindow.showBottomMiddleText("Data matrix info: {}".format(text))
                            barcodeInfoList.append((barcodeInfo, (x, y, w, h)))
                        self.resultList[index] = AlgorithmResult(workingArea=workingArea, basePoint=basePoint,
                                                                 methodName=step.stepAlgorithmName,
                                                                 stepId=step.stepId, passed=True,
                                                                 barcodeList=barcodeInfoList)
                        # if not isRunningFlag and step.stepId == executedStepId:
                        #     self.mainWindow.showImage(drawImage)
                        # self.imageList[index] = drawImage.copy()
                        step_image_show = step_image_result = drawImage

                    else:
                        self.mainWindow.runningTab.insertLog(text)
                        return False, self.resultList, text
                # Find chess board corners
                elif step.stepAlgorithmName == MethodList.findChessBoardCorners.value:
                    if len(sourceImage.shape) > 2:
                        grayImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_BGR2GRAY)
                    else:
                        grayImage = sourceImage.copy()
                    ret, corners, text = ImageProcess.findChessBoardCorner(sourceImage=grayImage,
                                                                           boardSize=(step.cbc_sizeX, step.cbc_sizeY))
                    cornersImage = sourceImage.copy()
                    if ret:
                        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                        corners2 = cv.cornerSubPix(grayImage, corners, (11, 11), (-1, -1), criteria)

                        # Draw and display the corners
                        cornersImage = cv.drawChessboardCorners(cornersImage, (step.cbc_sizeX, step.cbc_sizeY),
                                                                corners2, ret)
                        # if not isRunningFlag and step.stepId == executedStepId:
                        #     self.mainWindow.showImage(cornersImage)
                        step_image_show = step_image_result = cornersImage

                    else:
                        self.mainWindow.runningTab.insertLog(text)
                        return ret, self.resultList, text

                    print(corners)
                # Resize
                elif step.stepAlgorithmName == MethodList.resize.value:
                    try:
                        if step.rs_ratio:
                            resizeImage = cv.resize(sourceImage, dsize=(0, 0), fx=step.rs_fX, fy=step.rs_fY)
                        else:
                            resizeImage = cv.resize(sourceImage, dsize=(step.rs_sizeX, step.rs_sizeY))
                        # if not isRunningFlag and step.stepId == executedStepId:
                        #     self.mainWindow.showImage(resizeImage)
                        # self.imageList[index] = resizeImage.copy()
                        step_image_show = step_image_result = resizeImage

                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=True,
                                                                 methodName=step.stepAlgorithmName)
                    except Exception as error:
                        text = f"ERROR Algorithm {self.algorithmParameter.name}. Step {step.stepId} Check the parameter Detail: {error}"
                        self.mainWindow.runningTab.insertLog(text)
                        return False, self.resultList, text
                # Connection Contours
                elif step.stepAlgorithmName == MethodList.connectionContour.value:
                    stepId, paramName = step.resourceIndex
                    sourceInput: AlgorithmResult = self.getResultWithId(stepId=stepId, resultList=self.resultList)
                    contourList = sourceInput.getValue(paramName)

                    connectionImage = ImageProcess.processConnectContours(contourList, sourceImage,
                                                                          step.cc_size, step.cc_distance,
                                                                          step.cc_location)
                    step_image_show = step_image_result = connectionImage
                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea, basePoint=basePoint,
                                                             passed=True,
                                                             methodName=step.stepAlgorithmName)

                # Split Channel

                elif step.stepAlgorithmName == MethodList.splitChannel.value:
                    ret, channelImage, text = ImageProcess.processSplitChannel(sourceImage, step.sc_channel_id)

                    if not ret:
                        self.mainWindow.runningTab.insertLog(text)
                        return ret, self.resultList, text

                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(channelImage)
                    # self.imageList[index] = channelImage.copy()
                    step_image_show = step_image_result = channelImage
                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea, basePoint=basePoint,
                                                             passed=True,
                                                             methodName=step.stepAlgorithmName)
                elif step.stepAlgorithmName == MethodList.ocr_tesseract.value:
                    ret, text = ImageProcess.process_ocr_tesseract(sourceImage, step.ocr_tes_lange)
                    if not ret:
                        self.mainWindow.runningTab.insertLog(text)
                    else:
                        self.mainWindow.runningTab.insertLog(f"Tesseract step {step.stepId}: {text}")
                        self.mainWindow.showBottomMiddleText(f"Tesseract step {step.stepId}: {text}")
                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea, basePoint=basePoint,
                                                             passed=True,
                                                             methodName=step.stepAlgorithmName, text=text)
                # change color
                elif step.stepAlgorithmName == MethodList.changeColor.value:
                    maskId, paramName = step.change_color_mask
                    ret, maskInput, text = self.getSourceImage(imageIndex=maskId, step=step,
                                                               originalImage=originalImage)
                    averageColor = (0, 0, 0)

                    change_color_image = sourceImage.copy()
                    if step.change_color_code == ChangeColorCode.black2average.value:
                        averageColor = cv.mean(sourceImage, mask=maskInput)
                        change_color_image[sourceImage == 0] = averageColor[0]
                    elif step.change_color_code == ChangeColorCode.white2average.value:
                        averageColor = cv.mean(sourceImage, mask=maskInput)
                        change_color_image[sourceImage == 255] = averageColor[0]

                    # self.imageList[index] = change_color_image
                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea, basePoint=basePoint,
                                                             passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             drawImage=originalImage.copy(),
                                                             value=averageColor)
                    # if not isRunningFlag and executedStepId == index:
                    #     self.mainWindow.showImage(change_color_image)
                    step_image_show = step_image_result = change_color_image

                # threshold average
                elif step.stepAlgorithmName == MethodList.threshold_average.value:
                    averageColor = (0, 0, 0)
                    if len(sourceImage.shape) > 2:
                        sourceImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_BGR2GRAY)
                    averageColor = cv.mean(sourceImage, mask=None)

                    if step.ta_brightness_reflection > 0:
                        ret, thresh_image = ImageProcess.processThreshold(sourceImage, int(
                            averageColor[0] + step.ta_brightness_reflection), maxval=255, type=cv.THRESH_BINARY)
                    else:
                        ret, thresh_image = ImageProcess.processThreshold(sourceImage, int(
                            averageColor[0] + step.ta_brightness_reflection), maxval=255, type=cv.THRESH_BINARY_INV)

                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea, basePoint=basePoint,
                                                             passed=True,
                                                             methodName=step.stepAlgorithmName,
                                                             drawImage=originalImage.copy(),
                                                             value=averageColor)

                    step_image_show = step_image_result = thresh_image
                    # self.imageList[index] = thresh_image.copy()
                    # if not isRunningFlag and executedStepId == index:
                    #     self.mainWindow.showImage(thresh_image)

                # # DDK scratch Deep learning
                # elif step.stepAlgorithmName == MethodList.ddk_scratch_dl.value:
                #     rects, class_names, valid_scores = object_detection.processImage(sourceImage, step.dl_thresh,
                #                                                        resize_shape=step.dl_resize_shape)
                #
                #     self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea, basePoint=basePoint,
                #                                              passed=True if len(rects) == 0 else False,
                #                                              methodName=step.stepAlgorithmName,
                #                                              detectAreaList=rects)
                #     self.imageList[index] = sourceImage.copy()
                #     if not isRunningFlag and executedStepId == index:
                #         for rect, class_name in zip(rects, class_names):
                #             cv.rectangle(sourceImage, pt1=(rect[0], rect[1]), pt2=(rect[2], rect[3]),
                #                          color=(0, 0, 255),
                #                          thickness=5,
                #                          lineType=cv.LINE_AA)
                #             cv.putText(sourceImage, text=class_name, org=(rect[0], rect[1]),
                #                        fontFace=cv.FONT_HERSHEY_COMPLEX,
                #                        fontScale=_camera.parameter.textScale,
                #                        color=(255, 255, 0),
                #                        thickness=_camera.parameter.textThickness,
                #                        lineType=cv.LINE_AA)
                #         self.mainWindow.showImage(sourceImage)

                # distance point to point
                elif step.stepAlgorithmName == MethodList.distance_point_to_point.value:
                    point_1_id, paramName_point_1 = step.p2p_point1
                    point_2_id, paramName_point_2 = step.p2p_point2

                    sourceInput_point1: AlgorithmResult = self.getResultWithId(stepId=point_1_id,
                                                                               resultList=self.resultList)
                    point1 = sourceInput_point1.getValue(paramName_point_1)

                    sourceInput_point2: AlgorithmResult = self.getResultWithId(stepId=point_2_id,
                                                                               resultList=self.resultList)
                    point2 = sourceInput_point2.getValue(paramName_point_2)

                    # print(f"point1 = {point1}, basePoint={sourceInput_point1.basePoint}, workingarea = {sourceInput_point1.workingArea}")
                    # print(f"point2 = {point2}, basePoint={sourceInput_point2.basePoint}, workingarea = {sourceInput_point2.workingArea}")

                    real_point1 = (point1[0] + sourceInput_point1.basePoint[0] + sourceInput_point1.workingArea[0],
                                   point1[1] + sourceInput_point1.basePoint[1] + sourceInput_point1.workingArea[1])
                    real_point2 = (point2[0] + sourceInput_point2.basePoint[0] + sourceInput_point2.workingArea[0],
                                   point2[1] + sourceInput_point2.basePoint[1] + sourceInput_point2.workingArea[1])

                    # calculate distance
                    current_as = self.mainWindow.as_manager.getCurrentAS()
                    distance = ImageProcess.calculateDistanceBy2Points(real_point1, real_point2)
                    mm_distance = distance * current_as.robot_pixel_mm_Scale

                    textShow = f"Distance P2P = {mm_distance} micromet"

                    imageWidth = sourceImage.shape[1]
                    size = int(imageWidth / 300)
                    if step.p2p_range[0] <= mm_distance <= step.p2p_range[1]:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint,
                                                                 distance=mm_distance, passed=True,
                                                                 pointList=(real_point1, real_point2),
                                                                 methodName=step.stepAlgorithmName)
                        color = (0, 255, 0)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=False,
                                                                 distance=mm_distance,
                                                                 pointList=(real_point1, real_point2),
                                                                 methodName=step.stepAlgorithmName)
                        color = (0, 0, 255)

                    if not isRunningFlag and executedStepId == index:
                        # draw line
                        cv.circle(sourceImage, center=real_point1, radius=_camera.parameter.textThickness * 5,
                                  color=(0, 255, 0), thickness=-1, lineType=cv.LINE_AA)
                        cv.circle(sourceImage, center=real_point2, radius=_camera.parameter.textThickness * 5,
                                  color=(0, 255, 0), thickness=-1, lineType=cv.LINE_AA)
                        cv.line(sourceImage, real_point1, real_point2, color=color,
                                thickness=_camera.parameter.textThickness, lineType=cv.LINE_AA)

                        cv.putText(sourceImage, text=textShow, org=(size, sourceImage.shape[0] - 2 * size),
                                   fontFace=cv.FONT_HERSHEY_COMPLEX,
                                   fontScale=_camera.parameter.textScale,
                                   color=color,
                                   thickness=_camera.parameter.textThickness,
                                   lineType=cv.LINE_AA)
                        # self.mainWindow.showImage(sourceImage)
                        step_image_show = sourceImage

                # distance point to line
                elif step.stepAlgorithmName == MethodList.distance_point_to_line.value:
                    point_id, paramName_point = step.p2l_point
                    line_point_1_id, paramName_line_point_1 = step.p2l_point1_line
                    line_point_2_id, paramName_line_point_2 = step.p2l_point2_line

                    sourceInput_point: AlgorithmResult = self.getResultWithId(stepId=point_id,
                                                                              resultList=self.resultList)
                    point = sourceInput_point.getValue(paramName_point)

                    sourceInput_line_point1: AlgorithmResult = self.getResultWithId(stepId=line_point_1_id,
                                                                                    resultList=self.resultList)
                    line_point1 = sourceInput_line_point1.getValue(paramName_line_point_1)

                    sourceInput_line_point2: AlgorithmResult = self.getResultWithId(stepId=line_point_2_id,
                                                                                    resultList=self.resultList)
                    line_point2 = sourceInput_line_point2.getValue(paramName_line_point_2)

                    print(
                        f"point = {point}, basePoint={sourceInput_point.basePoint}, workingarea = {sourceInput_point.workingArea}")
                    print(
                        f"line point1 = {line_point1}, basePoint={sourceInput_line_point1.basePoint}, workingarea = {sourceInput_line_point1.workingArea}")
                    print(
                        f"line point2 = {line_point2}, basePoint={sourceInput_line_point2.basePoint}, workingarea = {sourceInput_line_point2.workingArea}")

                    real_point = (point[0] + sourceInput_point.basePoint[0] + sourceInput_point.workingArea[0],
                                  point[1] + sourceInput_point.basePoint[1] + sourceInput_point.workingArea[1])
                    real_line_point1 = (
                    line_point1[0] + sourceInput_line_point1.basePoint[0] + sourceInput_line_point1.workingArea[0],
                    line_point1[1] + sourceInput_line_point1.basePoint[1] + sourceInput_line_point1.workingArea[1])
                    real_line_point2 = (
                    line_point2[0] + sourceInput_line_point2.basePoint[0] + sourceInput_line_point2.workingArea[0],
                    line_point2[1] + sourceInput_line_point2.basePoint[1] + sourceInput_line_point2.workingArea[1])

                    # calculate distance
                    current_as = self.mainWindow.as_manager.getCurrentAS()
                    # ret, distance = ImageProcess.distance_point_to_line(real_point, (real_line_point1, real_line_point2))

                    ret, project_point = ImageProcess.project_from_point_to_line(real_point,
                                                                                 (real_line_point1, real_line_point2))

                    distance = ImageProcess.calculateDistanceBy2Points(real_point, project_point)
                    mm_distance = distance * current_as.robot_pixel_mm_Scale

                    textShow = f"Distance P2L = {mm_distance} micromet"

                    imageWidth = sourceImage.shape[1]
                    size = int(imageWidth / 300)
                    if step.p2l_range[0] <= mm_distance <= step.p2l_range[1]:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint,
                                                                 distance=mm_distance, passed=True,
                                                                 pointList=(real_point, project_point),
                                                                 line=(real_line_point1, real_line_point2),
                                                                 methodName=step.stepAlgorithmName)
                        color = (0, 255, 0)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint,
                                                                 distance=mm_distance, passed=False,
                                                                 pointList=(real_point, project_point),
                                                                 line=(real_line_point1, real_line_point2),
                                                                 methodName=step.stepAlgorithmName)
                        color = (0, 0, 255)

                    if not isRunningFlag and executedStepId == index:
                        # draw line
                        cv.circle(sourceImage, center=real_point, radius=_camera.parameter.textThickness * 5,
                                  color=(255, 255, 0), thickness=-1, lineType=cv.LINE_AA)
                        cv.circle(sourceImage, center=real_line_point1, radius=_camera.parameter.textThickness * 5,
                                  color=(255, 255, 0), thickness=-1, lineType=cv.LINE_AA)
                        cv.circle(sourceImage, center=real_line_point2, radius=_camera.parameter.textThickness * 5,
                                  color=(255, 255, 0), thickness=-1, lineType=cv.LINE_AA)
                        cv.line(sourceImage, real_line_point1, real_line_point2, color=(255, 255, 0),
                                thickness=_camera.parameter.textThickness, lineType=cv.LINE_AA)

                        cv.line(sourceImage, real_point, project_point, color=color,
                                thickness=_camera.parameter.textThickness, lineType=cv.LINE_AA)

                        cv.putText(sourceImage, text=textShow, org=(size, sourceImage.shape[0] - 2 * size),
                                   fontFace=cv.FONT_HERSHEY_COMPLEX,
                                   fontScale=_camera.parameter.textScale,
                                   color=color,
                                   thickness=_camera.parameter.textThickness,
                                   lineType=cv.LINE_AA)
                        step_image_show = sourceImage
                        # self.mainWindow.showImage(sourceImage)
                # Angle from 2 lines
                elif step.stepAlgorithmName == MethodList.angle_from_2_lines.value:
                    point1_line1_id, paramName_point1_line1 = step.af2l_point1_line1
                    point2_line1_id, paramName_point2_line1 = step.af2l_point2_line1
                    point1_line2_id, paramName_point1_line2 = step.af2l_point1_line2
                    point2_line2_id, paramName_point2_line2 = step.af2l_point2_line2

                    sourInput_point1_line1: AlgorithmResult = self.getResultWithId(stepId=point1_line1_id,
                                                                                   resultList=self.resultList)
                    if sourInput_point1_line1 is None:
                        point1_line1 = (0, 0)
                        point2_line1 = (0, sourceImage.shape[0])
                    else:
                        point1_line1 = sourInput_point1_line1.getValue(paramName_point1_line1)
                        point1_line1 = (
                        point1_line1[0] + sourInput_point1_line1.basePoint[0] + sourInput_point1_line1.workingArea[0],
                        point1_line1[1] + sourInput_point1_line1.basePoint[1] + sourInput_point1_line1.workingArea[1])

                    sourInput_point2_line1: AlgorithmResult = self.getResultWithId(stepId=point2_line1_id,
                                                                                   resultList=self.resultList)
                    if sourInput_point2_line1 is None:
                        point1_line1 = (0, 0)
                        point2_line1 = (0, sourceImage.shape[0])
                    else:
                        point2_line1 = sourInput_point2_line1.getValue(paramName_point2_line1)
                        point2_line1 = (
                        point2_line1[0] + sourInput_point2_line1.basePoint[0] + sourInput_point2_line1.workingArea[0],
                        point2_line1[1] + sourInput_point2_line1.basePoint[1] + sourInput_point2_line1.workingArea[1])

                    sourInput_point1_line2: AlgorithmResult = self.getResultWithId(stepId=point1_line2_id,
                                                                                   resultList=self.resultList)
                    if sourInput_point1_line2 is None:
                        point1_line2 = (0, 0)
                        point2_line2 = (sourceImage.shape[1], 0)
                    else:
                        point1_line2 = sourInput_point1_line2.getValue(paramName_point1_line2)
                        point1_line2 = (
                        point1_line2[0] + sourInput_point1_line2.basePoint[0] + sourInput_point1_line2.workingArea[0],
                        point1_line2[1] + sourInput_point1_line2.basePoint[1] + sourInput_point1_line2.workingArea[1])

                    sourInput_point2_line2: AlgorithmResult = self.getResultWithId(stepId=point2_line2_id,
                                                                                   resultList=self.resultList)
                    if sourInput_point2_line2 is None:
                        point1_line2 = (0, 0)
                        point2_line2 = (sourceImage.shape[1], 0)
                    else:
                        point2_line2 = sourInput_point2_line2.getValue(paramName_point2_line2)
                        point2_line2 = (
                        point2_line2[0] + sourInput_point2_line2.basePoint[0] + sourInput_point2_line2.workingArea[0],
                        point2_line2[1] + sourInput_point2_line2.basePoint[1] + sourInput_point2_line2.workingArea[1])

                    angle = ImageProcess.findAngleByLine((point1_line1, point2_line1), (point1_line2, point2_line2))

                    if step.af2l_valid_range[0] <= angle <= step.af2l_valid_range[1]:
                        color = (0, 255, 0)
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint,
                                                                 angle=angle, passed=True,
                                                                 lineList=[(point1_line1, point2_line1),
                                                                           (point1_line2, point2_line2)],
                                                                 methodName=step.stepAlgorithmName)
                    else:
                        color = (0, 0, 255)
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint,
                                                                 angle=angle, passed=False,
                                                                 lineList=[(point1_line1, point2_line1),
                                                                           (point1_line2, point2_line2)],
                                                                 methodName=step.stepAlgorithmName)

                    # self.imageList[index] = sourceImage.copy()
                    step_image_result = sourceImage.copy()

                    self.mainWindow.runningTab.insertLog(f"Find Angle by line step {step.stepId}: {angle}")
                    self.mainWindow.showBottomMiddleText(f"Find Angle by line step {step.stepId}: {angle}")
                    if not isRunningFlag and step.stepId == executedStepId:

                        if angle != 0 and angle != 360:
                            intersection_point = ImageProcess.get_intersect_from_2_lines(
                                line1=(point1_line1, point2_line1),
                                line2=(point1_line2, point2_line2))
                            intersection_point = (int(intersection_point[0]), int(intersection_point[1]))
                            cv.line(sourceImage, point1_line1, intersection_point, color=color,
                                    thickness=_camera.parameter.textThickness, lineType=cv.LINE_AA)
                            cv.line(sourceImage, point1_line2, intersection_point, color=color,
                                    thickness=_camera.parameter.textThickness, lineType=cv.LINE_AA)
                        else:
                            cv.line(sourceImage, point1_line1, point2_line1, color=color,
                                    thickness=_camera.parameter.textThickness, lineType=cv.LINE_AA)
                            cv.line(sourceImage, point1_line2, point2_line2, color=color,
                                    thickness=_camera.parameter.textThickness, lineType=cv.LINE_AA)
                        self.mainWindow.showImage(sourceImage)
                # Ignore areas
                elif step.stepAlgorithmName == MethodList.ignore_areas.value:
                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea, basePoint=basePoint,
                                                             passed=True, ignore_area_list=step.ignore_areas_list,
                                                             methodName=step.stepAlgorithmName)

                # Multi select area
                elif step.stepAlgorithmName == MethodList.multi_select_area.value:
                    mask = np.zeros(sourceImage.shape, np.uint8)
                    # imageShow = self.mainWindow.originalImage.copy()
                    list_masks = []
                    for area_id, (area, area_type) in enumerate(step.select_areas_list):
                        if area_type == "rectangle":
                            list_masks.append(cv.rectangle(mask.copy(), pt1=(area[0], area[1]), pt2=(area[2], area[3]),
                                                           color=(255, 255, 255),
                                                           thickness=-1,
                                                           lineType=cv.LINE_AA))

                        elif area_type == "circle":
                            list_masks.append(cv.circle(mask.copy(), center=area[0],
                                                        radius=area[1],
                                                        color=(255, 255, 255),
                                                        thickness=-1,
                                                        lineType=cv.LINE_AA))
                    final_mask = None
                    if len(list_masks) > 0:
                        final_mask = list_masks[0]
                        if not isRunningFlag and step.stepId == executedStepId:
                            self.mainWindow.showImage(list_masks[0])
                            TimeControl.sleep(1000)
                        for idx in range(len(list_masks) - 1):
                            if not isRunningFlag and step.stepId == executedStepId:
                                self.mainWindow.showImage(list_masks[idx + 1])
                                TimeControl.sleep(1000)
                            final_mask = ImageProcess.processBitwise_xor(final_mask, list_masks[idx + 1])
                    if final_mask is not None:
                        select_area_image = ImageProcess.processBitwise_and(sourceImage, sourceImage, final_mask)
                        # self.imageList[index] = select_area_image.copy()
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint,
                                                                 passed=True, methodName=step.stepAlgorithmName)
                        # if not isRunningFlag and step.stepId == executedStepId:
                        #     self.mainWindow.showImage(select_area_image)
                        step_image_show = step_image_result = select_area_image

                    else:
                        # self.imageList[index] = sourceImage.copy()
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint,
                                                                 passed=True, methodName=step.stepAlgorithmName)
                        self.mainWindow.runningTab.insertLog("There is no select area")
                        step_image_show = step_image_result = sourceImage

                # rotate image with angle
                elif step.stepAlgorithmName == MethodList.rotate_with_angle.value:
                    rotate_angle_image = ImageProcess.rotateImageWithAngle(sourceImage=sourceImage,
                                                                           angle=step.riwa_angle,
                                                                           reshape=step.riwa_reshape)
                    # self.imageList[index] = rotate_angle_image.copy()
                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea, basePoint=basePoint,
                                                             passed=True, methodName=step.stepAlgorithmName)
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(rotate_angle_image)
                    step_image_show = step_image_result = rotate_angle_image

                # Change brightness
                elif step.stepAlgorithmName == MethodList.brightness_change.value:
                    change_brightness_image = ImageProcess.change_brightness(sourceImage=sourceImage,
                                                                             type=step.change_brightness_type,
                                                                             value=step.change_brightness_value)
                    # self.imageList[index] = change_brightness_image.copy()
                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea, basePoint=basePoint,
                                                             passed=True, methodName=step.stepAlgorithmName)
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(change_brightness_image)
                    step_image_show = step_image_result = change_brightness_image

                # Histogram Equalization
                elif step.stepAlgorithmName == MethodList.histogram_equalization.value:
                    if len(sourceImage.shape) > 2:
                        sourceImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_BGR2GRAY)
                    equalizedImage = None

                    if step.he_type == "Normal Equalization":
                        equalizedImage = cv.equalizeHist(sourceImage)
                    elif step.he_type == "Adaptive Equalization":
                        clahe = cv.createCLAHE(clipLimit=step.he_clipLimit,
                                               tileGridSize=(step.he_tile_grid_size, step.he_tile_grid_size))
                        equalizedImage = clahe.apply(sourceImage)
                    # self.imageList[index] = equalizedImage.copy()
                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea, basePoint=basePoint,
                                                             passed=True, methodName=step.stepAlgorithmName)
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(equalizedImage)
                    step_image_show = step_image_result = equalizedImage


                # Gama correction
                elif step.stepAlgorithmName == MethodList.gama_correction.value:
                    gama_correction_image = ImageProcess.adjust_gamma(sourceImage, gamma=step.gama_correction_value)
                    # self.imageList[index] = gama_correction_image.copy()
                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea, basePoint=basePoint,
                                                             passed=True, methodName=step.stepAlgorithmName)
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(gama_correction_image)
                    step_image_show = step_image_result = gama_correction_image


                # Reference Edge corner
                elif step.stepAlgorithmName == MethodList.reference_edge_corner.value:
                    ret, thresh_image = ImageProcess.processThreshold(sourceImage, thresh=step.rec_thresh, maxval=255,
                                                                      type=step.rec_thresh_type)
                    if ret:
                        listContours, areaDetectList, contourImage = ImageProcess.processFindContours(thresh_image,
                                                                                                      minArea=step.rec_area)
                        ref_extTop, ref_extRight, ref_extBot, ref_extLeft = step.rec_origin_extreme
                        translateImage = None
                        showImage = contourImage
                        if len(listContours) > 0:
                            contour = listContours[0]
                            if isGettingReference:
                                step.rec_origin_extreme = ImageProcess.processFindExtremeOfContour(contour)
                                showImage = ImageProcess.processCvtColor(showImage, cv.COLOR_GRAY2BGR)
                                for center in step.rec_origin_extreme:
                                    cv.circle(showImage, center=center, radius=5, color=Color.bgrAqua(), thickness=-1,
                                              lineType=cv.LINE_AA)
                                self.mainWindow.showImage(showImage)
                            else:
                                extTop, extRight, extBot, extLeft = ImageProcess.processFindExtremeOfContour(contour)
                                movingParameter = [0, 0, 0, 0]
                                if step.rec_type == ReferenceEdgeCornerType.top.value:
                                    movingParameter[0] = extTop[1] - ref_extTop[1]
                                elif step.rec_type == ReferenceEdgeCornerType.right.value:
                                    movingParameter[1] = extRight[0] - ref_extRight[0]
                                elif step.rec_type == ReferenceEdgeCornerType.bottom.value:
                                    movingParameter[2] = extBot[1] - ref_extBot[1]
                                elif step.rec_type == ReferenceEdgeCornerType.left.value:
                                    movingParameter[3] = extLeft[0] - ref_extLeft[0]
                                elif step.rec_type == ReferenceEdgeCornerType.left_top.value:
                                    movingParameter[0] = extTop[1] - ref_extTop[1]
                                    movingParameter[3] = extLeft[0] - ref_extLeft[0]
                                elif step.rec_type == ReferenceEdgeCornerType.top_right.value:
                                    movingParameter[0] = extTop[1] - ref_extTop[1]
                                    movingParameter[1] = extRight[0] - ref_extRight[0]
                                elif step.rec_type == ReferenceEdgeCornerType.right_bottom.value:
                                    movingParameter[2] = extBot[1] - ref_extBot[1]
                                    movingParameter[1] = extRight[0] - ref_extRight[0]
                                elif step.rec_type == ReferenceEdgeCornerType.bottom_left.value:
                                    movingParameter[2] = extBot[1] - ref_extBot[1]
                                    movingParameter[3] = extLeft[0] - ref_extLeft[0]
                                move_x = movingParameter[1] if movingParameter[1] != 0 else movingParameter[3]
                                move_y = movingParameter[0] if movingParameter[0] != 0 else movingParameter[2]
                                ret, translateImage, text = ImageProcess.processTransMoveImage(
                                    sourceImage=step_resource_image,
                                    move_x=move_x, move_y=move_y)
                                step_image_show = step_image_result = translateImage
                                # self.imageList[index] = translateImage
                                # if not isRunningFlag and step.stepId == executedStepId:
                                #     self.mainWindow.showImage(translateImage)
                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=(0, 0, 0, 0),
                                                             basePoint=basePoint,
                                                             passed=ret, methodName=step.stepAlgorithmName)
                # Flood Fill
                elif step.stepAlgorithmName == MethodList.floodFill.value:
                    mask = np.zeros((sourceImage.shape[0] + 2, sourceImage.shape[1] + 2), np.uint8)
                    cv.floodFill(sourceImage, mask, seedPoint=step.flood_fill_seed_point, newVal=step.flood_fill_color,
                                 loDiff=None if step.flood_fill_lowdiff == 0 else step.flood_fill_lowdiff,
                                 upDiff=None if step.flood_fill_updiff == 0 else step.flood_fill_updiff)
                    # self.imageList[index] = sourceImage.copy()
                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea, basePoint=basePoint,
                                                             passed=True, methodName=step.stepAlgorithmName)
                    step_image_show = step_image_result = sourceImage
                    # if not isRunningFlag and step.stepId == executedStepId:
                    #     self.mainWindow.showImage(sourceImage)
                # Viet OCR
                elif step.stepAlgorithmName == MethodList.viet_ocr.value:
                    if self.viet_ocr_engine is None or self.viet_ocr_engine.detector is None:
                        try:
                            self.viet_ocr_engine = Viet_OCR(model=step.vo_model, device=step.vo_device,
                                                            weight_file=step.vo_weight_file_path,
                                                            vocab_file_path=step.vo_vocab_path_file)
                        except Exception as error:
                            self.mainWindow.runningTab.insertLog(f"ERROR Viet OCR. Detail {error}")

                    if self.viet_ocr_engine is not None:
                        text = self.viet_ocr_engine.read_from_image(Image.fromarray(sourceImage))
                        self.mainWindow.runningTab.insertLog(f"VietOCR step {step.stepId}: {text}")
                        self.mainWindow.showBottomMiddleText(f"VieOCR step {step.stepId}: {text}")
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=True,
                                                                 methodName=step.stepAlgorithmName, text=text)
                # Contour linear regression
                elif step.stepAlgorithmName == MethodList.contour_linear_regression.value:
                    source_contours = self.get_source_with_source(self.resultList, step.clr_source_contour)
                    are_source = self.get_source_with_source(self.resultList, step.clr_area_source)

                    list_coef = ImageProcess.fit_line_contour_with_linear_regression(source_contours)
                    line_list = []
                    for i, coef in enumerate(list_coef):
                        if coef is None:
                            text = "ERROR cannot fit line with contours given, please check"
                            return False, self.resultList, text
                        x_min = source_contours[i][:, :, 0].min()
                        x_max = source_contours[i][:, :, 0].max()
                        y_min = int(coef[0] + coef[1] * x_min)
                        y_max = int(coef[0] + coef[1] * x_max)
                        cv.line(sourceImage, (x_min, y_min), (x_max, y_max), (0, 255, 255), 6, cv.LINE_AA)
                        line_list.append(((x_min, y_min), (x_max, y_max)))
                    if len(line_list) < 1:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=False, lineList=line_list,
                                                                 methodName=step.stepAlgorithmName, text=text)
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=True, lineList=line_list,
                                                                 methodName=step.stepAlgorithmName, text=text)

                    step_image_show = step_image_result = sourceImage
                # Contour Approximation
                elif step.stepAlgorithmName == MethodList.contourApproximation.value:
                    source_contours = self.get_source_with_source(self.resultList, step.c_apprx_source_contour)
                    ret, list_approximation, text = ImageProcess.process_contours_approximation(contours=source_contours,
                                                                                                epsilon_percent=step.c_apprx_epsilon_percent,
                                                                                                closed=step.c_apprx_closed)

                    if ret:
                        drawImage = ImageProcess.convert_to_bgr_image(sourceImage)
                        cv.drawContours(image=drawImage, contours=list_approximation, contourIdx=-1,
                                        color=(0, 255, 0), thickness=_camera.parameter.textThickness, lineType=cv.LINE_AA)
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=True,
                                                                 contourList=list_approximation,
                                                                 methodName=step.stepAlgorithmName)
                        step_image_show = drawImage
                    else:
                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint, passed=False,
                                                                 contourList=list_approximation,
                                                                 methodName=step.stepAlgorithmName)

                elif step.stepAlgorithmName == MethodList.fittingLine.value:
                    source_contours = self.get_source_with_source(self.resultList, step.cfl_source_contour)
                    drawImage = ImageProcess.convert_to_bgr_image(sourceImage)
                    line_list = []
                    for contour in source_contours:
                        # [vx, vy, x0, y0] => (x, y) = (x0, y0) + t*(vx, vy)
                        vector_line = ImageProcess.process_contours_fit_line(contour, step.cfl_distance_type,
                                                                             step.cfl_param, step.cfl_reps,
                                                                             step.cfl_aeps)
                        max_x = contour[:, :, 0].max()
                        min_x = contour[:, :, 0].min()
                        # compute t0 = (y-y0)/vy = (x - x0)/vx
                        t_min = (min_x - vector_line[2]) / vector_line[0]
                        t_max = (max_x - vector_line[2]) / vector_line[0]

                        # compute the start and end point
                        p_min = (vector_line[2:4] + (t_min * vector_line[0:2])).astype(np.int32)
                        p_max = (vector_line[2:4] + (t_max * vector_line[0:2])).astype(np.int32)
                        line_list.append((p_min, p_max))
                        # draw the line. For my version of opencv, it wants tuples so we
                        # flatten the arrays and convert
                        # args: cv2.line(image, p0, p1, color, thickness)
                        drawImage = cv.line(drawImage, (p_min[0][0], p_min[1][0]), (p_max[0][0], p_max[1][0]), (0, 255, 0),
                                            thickness=_camera.parameter.textThickness, lineType=cv.LINE_AA)

                    step_image_show = drawImage
                    step_image_result = sourceImage
                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                             basePoint=basePoint, passed=True,
                                                             lineList=line_list,
                                                             methodName=step.stepAlgorithmName)


                # Draw result
                elif step.stepAlgorithmName == MethodList.drawResult.value:
                    if not isRunningFlag:
                        color = (0, 255, 0)
                        imageWidth = sourceImage.shape[1]
                        imageHeight = sourceImage.shape[0]
                        size = int(imageWidth / 250)
                        if len(sourceImage.shape) < 3:
                            sourceImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_GRAY2BGR)

                        for result in self.resultList:
                            if result is None:
                                continue
                            if result.methodName == MethodList.focusChecking.value:
                                if result.passed:
                                    color = (0, 255, 0)
                                else:
                                    color = (0, 0, 255)
                                    sourceImage = cv.putText(sourceImage,
                                                             text="Result = {}".format(result.value),
                                                             org=(size, imageHeight - 2 * size),
                                                             fontFace=cv.FONT_HERSHEY_SIMPLEX,
                                                             fontScale=_camera.parameter.textScale,
                                                             color=color,
                                                             thickness=_camera.parameter.textThickness,
                                                             lineType=cv.LINE_AA)

                            if result.passed:
                                color = (0, 255, 0)
                                sourceImage = cv.rectangle(sourceImage,
                                                           (result.workingArea[0] + result.basePoint[0],
                                                            result.workingArea[1] + result.basePoint[1]),
                                                           (result.workingArea[2] + result.basePoint[0],
                                                            result.workingArea[3] + result.basePoint[1]),
                                                           color, 3)

                                if result.methodName == MethodList.houghCircle.value or result.methodName == MethodList.averageHoughCircle.value:
                                    if len(result.circleList) > 0:
                                        for circle in result.circleList:
                                            if circle is not None:
                                                cv.circle(sourceImage, (circle[0][0], circle[0][1]), circle[1],
                                                          (0, 255, 0), 5)
                                                cv.circle(sourceImage, (circle[0][0], circle[0][1]), 10, (0, 255, 0),
                                                          -1)

                                if result.methodName == MethodList.findContour.value:
                                    for area in result.detectAreaList:
                                        cv.rectangle(sourceImage,
                                                     (area[0] + result.basePoint[0], area[1] + result.basePoint[1]),
                                                     (area[2] + result.basePoint[0], area[3] + result.basePoint[1]),
                                                     (0, 255, 0), 5)
                                        # center = (int((area[0] + area[2]) / 2) + result.basePoint[0],
                                        #           int((area[1] + area[3]) / 2) + result.basePoint[1])
                                        # cv.circle(sourceImage, center, 10, (0, 255, 0), -1)

                                if result.methodName == MethodList.threshold.value:
                                    self.mainWindow.showImage(result.drawImage)
                            else:
                                color = (0, 0, 255)
                                sourceImage = cv.rectangle(sourceImage,
                                                           (result.workingArea[0] + result.basePoint[0],
                                                            result.workingArea[1] + result.basePoint[1]),
                                                           (result.workingArea[2] + result.basePoint[0],
                                                            result.workingArea[3] + result.basePoint[1]),
                                                           color, 3)

                                sourceImage = cv.putText(sourceImage,
                                                         "{}".format(result.stepId),
                                                         (result.workingArea[0] + result.basePoint[0],
                                                          result.workingArea[1] + result.basePoint[1]),
                                                         cv.FONT_HERSHEY_SIMPLEX,
                                                         _camera.parameter.textScale,
                                                         color, _camera.parameter.textThickness, lineType=cv.LINE_AA)
                        self.mainWindow.showImage(sourceImage)

                elif step.stepAlgorithmName == MethodList.segment_yolov8.value:
                    if self.model_segmentation_yolov8 is None:
                        self.load_model_yolo(path_model=step.path_weight_yolov8)
                    ret, list_results = ImageProcess.process_segmentation_yolov8(
                        model_yolo=self.model_segmentation_yolov8,
                        image=sourceImage, conf=step.confidence_yolov8)
                    list_center_point = []
                    if ret:
                        for res in list_results:
                            class_id = res[0]
                            name_class = res[1]
                            confidence = res[2]
                            bbox = res[3]
                            mask = res[4]
                            x_min, y_min, x_max, y_max = bbox
                            # show box
                            cv.rectangle(sourceImage, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                            # viền polygon mask
                            # pts = np.array(mask, dtype=np.int32)
                            # pts = pts.reshape((-1, 1, 2))
                            # cv.polylines(img_show, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
                            # show  min rectangle
                            points = np.array(mask, dtype=np.float32)
                            rect = cv.minAreaRect(points)
                            box = cv.boxPoints(rect)
                            box = np.int0(box)
                            cv.drawContours(sourceImage, [box], 0, (255, 0, 0), 5)
                            center = np.mean(box, axis=0).astype(int)
                            cv.circle(sourceImage, center=center, color=(0, 0, 255), radius=3, thickness=5)
                            list_center_point.append(center.tolist())
                            #
                            text = ""
                            # show name class
                            text += f"{name_class} "
                            # show_conf
                            text += f"{confidence:.2f} "
                            cv.putText(sourceImage, text, (x_min, y_min - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                                               (0, 255, 0), 2)

                    step_image_show = sourceImage
                    step_image_result = sourceImage

                    self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                             basePoint=basePoint, passed=True,
                                                             list_center_min_rec=list_center_point,
                                                             methodName=step.stepAlgorithmName)
                    print("list_center_point:", list_center_point)
                    self.mainWindow.showImage(sourceImage)

                # Multi select area 2 - circle
                elif step.stepAlgorithmName == MethodList.auto_multi_circle.value:
                    try:
                        image = sourceImage.copy()
                        # convert to bgr
                        image = ImageProcess.convert_to_bgr_image(image)
                        amc_circle = self.get_source_with_source(self.resultList, step.amc_circle_list)[0]

                        mask = np.zeros(image.shape[:2], dtype=np.uint8)
                        mask1 = np.zeros(image.shape[:2], dtype=np.uint8)
                        cv.circle(mask, amc_circle[0], int(amc_circle[1] + step.amc_circle_radius_1), 255, -1)
                        cv.circle(mask1, amc_circle[0], int(amc_circle[1] + step.amc_circle_radius_2), 255, -1)
                        image1 = cv.bitwise_xor(mask, mask1)
                        image2 = cv.merge((image1, image1, image1))
                        sourceImage = cv.bitwise_and(image, image2)

                        self.resultList[index] = AlgorithmResult(stepId=index, workingArea=workingArea,
                                                                 basePoint=basePoint,
                                                                 passed=True, methodName=step.stepAlgorithmName)
                        step_image_show = step_image_result = sourceImage
                    except Exception as err:
                        self.mainWindow.runningTab.insertLog("Auto mutli circle: {}".format(err))

                self.mainWindow.runningTab.insertLog("end step {} name {}".format(step.stepId, step.stepAlgorithmName))

                # show image process and save image process off each process
                if step_image_result is not None:
                    try:
                        self.imageList[index] = step_image_result.copy()
                    except Exception as error:
                        self.mainWindow.runningTab.insertLog(
                            f"Cannot add image process of step {index} name {step.stepAlgorithmName}, detail: {error}")
                if step_image_show is not None:
                    if not isRunningFlag and step.stepId == executedStepId:
                        self.mainWindow.showImage(step_image_show)

        except Exception as error:
            # if not isRunningFlag:
            #     messagebox.showerror("Execute Step {}".format(index), "Detail: {}".format(error))
            # self.mainWindow.runningTab.insertLog("ERROR execute Step {}: {}".format(index, error))
            text = "ERROR Algorithm {} Step {}. Detail: {}".format(step.stepAlgorithmName, index, error)
            self.mainWindow.runningTab.insertLog(text)

        self.mainWindow.runningTab.insertLog("end execute algorithm")
        self.mainWindow.runningTab.insertLog("Vision process time: {} ms".format(TimeControl.time() - time))
        self.last_execute_step = executedStepId
        result_list = [algorithm_result for algorithm_result in self.resultList if algorithm_result is not None]
        return True, result_list, text

    def getSourceImage(self, imageIndex, step, originalImage):
        text = ""
        # neu chi so o day la original image
        if imageIndex == -1:
            processImage = originalImage.copy()
        # neu chi so the hien day la reference image
        elif imageIndex == -4:
            refImagePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                                   "/",
                                                   self.algorithmParameter.name,
                                                   "/",
                                                   "imageReference_",
                                                   self.algorithmParameter.refImageName,
                                                   ".png")
            try:
                processImage = cv.imdecode(np.fromfile(refImagePath, dtype=np.uint8), cv.IMREAD_COLOR)
            except Exception as error:
                text = "ERROR Algorithm {}. Step {} Please check the image reference. Detail {}".format(
                    step.stepAlgorithmName, step.stepId, error)
                self.mainWindow.runningTab.insertLog(text)
                return False, None, text
        # trong truong hop chon anh mau
        elif imageIndex == -3:
            templatePath = "{}{}{}{}{}{}{}".format(self.mainWindow.algorithmManager.filePath,
                                                   "/",
                                                   self.algorithmParameter.name,
                                                   "/",
                                                   "imageTemplate_",
                                                   step.templateName,
                                                   ".png")
            try:
                processImage = cv.imdecode(np.fromfile(templatePath, dtype=np.uint8), cv.IMREAD_COLOR)
            except Exception as error:
                text = "ERROR Algorithm {}. Step {} Please check the image template. Detail: {}".format(
                    step.stepAlgorithmName, step.stepId, error)
                self.mainWindow.runningTab.insertLog(text)
                return False, None, text
        # truong hop de None
        elif imageIndex == -2:
            processImage = None
        # Truong hop chon anh cua cac buoc truoc
        else:
            processImage = self.imageList[imageIndex].copy()
        return True, processImage, text

    def get_source_with_source(self, resultList: [AlgorithmResult], source):
        stepId, parmName = source
        result: AlgorithmResult = self.getResultWithId(resultList=resultList, stepId=stepId)
        return result.getValue(parmName)

    def getResultWithSource(self, resultList: [AlgorithmResult], source):
        stepId, parmName = source
        return self.getResultWithId(resultList=resultList, stepId=stepId)

    def getResultWithId(self, resultList: [AlgorithmResult], stepId):
        ret = None
        for result in resultList:
            if result is not None and result.stepId == stepId:
                ret = result
                break
        return ret

    def executeAlgorithm(self, image=None, camera: Camera = None, imageName=""):
        if image is None:
            return False, [], "Input image is None"
        self.last_execute_step = None
        try:
            # originalImage = image.copy() if image is not None else self.mainWindow.originalImage.copy()
            self.mainWindow.originalImage = image.copy()

            ret, resultList, text = self.executeStep(len(self.algorithmParameter.steps) - 1, camera=camera, image=image,
                                                     isRunningFlag=True)
            if self.algorithmParameter.saveImageFlag:
                saveThread = threading.Thread(target=self.saveAlgorithmImageThread, args=(image, imageName))
                saveThread.start()
            # self.checkExpiredImagePath()
            # if self.algorithmParameter.saveImageFlag:
            #     dataPath = "./data"
            #     imagePath = "./data/image"
            #     datePath = "./data/image/" + TimeControl.y_m_dFormat()
            #     imageFileName = datePath + "/" + TimeControl.y_m_d_H_M_S_format() + "-" + imageName + ".jpg"
            #
            #     PathFileControl.generatePath(dataPath)
            #     PathFileControl.generatePath(imagePath)
            #     PathFileControl.generatePath(datePath)
            #     cv.imwrite(imageFileName, image)
            return ret, resultList, text
        except Exception as error:
            text = "ERROR execute Algorithm: {}".format(error)
            self.mainWindow.runningTab.insertLog(text)
            return False, [], text

    def saveAlgorithmImageThread(self, image, imageName):
        try:
            dataPath = "./data"
            imagePath = "./data/image"
            datePath = "./data/image/" + TimeControl.y_m_dFormat()
            imageFileName = datePath + "/" + TimeControl.y_m_d_H_M_S_format() + "-" + imageName + ".jpg"

            PathFileControl.generatePath(dataPath)
            PathFileControl.generatePath(imagePath)
            PathFileControl.generatePath(datePath)
            cv.imencode(".jpg", image)[1].tofile(imageFileName)
        except Exception as error:
            print(error)

    def checkExpiredImagePath(self):
        imagePath = "./data/image"

        listPath = [f.path for f in os.scandir(imagePath) if f.is_dir()]
        listPath.sort()
        print("image path num = {}".format(len(listPath)))
        if len(listPath) > 2:
            for i in range(len(listPath)):
                if i > 1:
                    try:
                        loadingView = LoadingView(self.mainWindow.mainFrame, self.mainWindow, "Deleting...")
                        PathFileControl.deleteFolder(listPath[i])
                        loadingView.done()
                    except Exception as error:
                        self.mainWindow.runningTab.insertLog("ERROR Delete image foloder: {}".format(error))


class AlgorithmManager:
    filePath = "./config/Algorithm"
    algorithmList = []
    # currentIndex = -1
    currentName = ""
    maxStep = 99

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow
        PathFileControl.generatePath(self.filePath)
        self.get()

    def save(self):
        return

    def get(self):
        self.algorithmList = []
        try:
            filePath = self.filePath + "/index.txt"
            file = TextFile(filePath)
            file.readFile()
            self.currentName = file.dataList[0]
        except:
            pass
        listPath = [f.path for f in os.scandir(self.filePath) if f.is_dir()]

        for algorithmDir in listPath:
            try:
                self.algorithmList.append(Algorithm(algorithmDir, self.mainWindow, self.maxStep))
            except:
                pass

    def algorithmNameExisted(self, algorithmName):
        for algorithm in self.algorithmList:
            if algorithm.algorithmParameter.name == algorithmName:
                return True

        return False

    def addNewAlgorithm(self, algorithmName):
        algorithm = None
        try:
            algorithm = Algorithm(self.filePath + "/{}".format(algorithmName), self.mainWindow, self.maxStep)
            algorithm.algorithmParameter.name = algorithmName
            algorithm.algorithmParameter.steps = []
            for step in range(self.mainWindow.algorithmManager.maxStep):
                stepParameter = StepParameter()
                stepParameter.stepAlgorithmName = MethodList.matchingTemplate.value
                stepParameter.stepId = step
                stepParameter.resourceIndex = (step - 1, AlgorithmResultKey.drawImage.value)
                algorithm.algorithmParameter.steps.append(stepParameter)
            self.algorithmList.append(algorithm)
            if algorithm.save():
                self.changeCurrentAlgorithm(algorithmName)
                self.updateList()

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Add New Algorithm: {}".format(error))
            messagebox.showerror("Add New Algorithm", "{}".format(error))

        return algorithm

    def updateList(self):
        self.get()
        machineName = self.mainWindow.startingWindow.machineName
        if machineName.isRearMissingInspectionMachine():
            self.mainWindow.modelSettingTab.rearCheckMissingFrame.updateAlgorithmList()
        elif machineName.isLocationDetect():
            self.mainWindow.modelSettingTab.locationDetectSettingFrame.updateAlgorithmList()
        elif machineName.is_demo_color_detect():
            self.mainWindow.modelSettingTab.demo_color_detect_setting_frame.updateAlgorithmList()
        elif machineName.is_demo_location_detect():
            self.mainWindow.modelSettingTab.demo_location_detect_setting_frame.updateAlgorithmList()
        elif machineName.is_roto_weighing_robot():
            self.mainWindow.modelSettingTab.roto_weighing_robot_model_setting_frame.updateAlgorithmList()
        elif machineName.is_e_map_checking():
            self.mainWindow.modelSettingTab.e_map_model_setting.updateAlgorithmList()
        elif machineName.is_reading_weighing():
            self.mainWindow.modelSettingTab.read_weighing_model_setting.updateAlgorithmList()
        elif machineName.is_fpc_inspection():
            self.mainWindow.modelSettingTab.fpc_inspection_frame.updateAlgorithmList()
        elif machineName.is_ddk_inspection():
            self.mainWindow.modelSettingTab.ddk_inspection_frame.updateAlgorithmList()
        elif machineName.is_counting_in_conveyor():
            self.mainWindow.modelSettingTab.counting_in_conveyor_setting.updateAlgorithmList()
        elif machineName.is_syc_phone_check():
            self.mainWindow.modelSettingTab.syc_model_setting_frame.updateAlgorithmList()

        self.mainWindow.as_setting_tab.updateAlgorithmList()

    def duplicateAlgorithm(self):
        try:
            currentAlgorithm = self.getCurrentAlgorithm()
            newAlgorithmName = currentAlgorithm.algorithmParameter.name + "_Copy"
            index = 1
            while self.algorithmNameExisted(newAlgorithmName):
                newAlgorithmName = currentAlgorithm.algorithmParameter.name + "_Copy" + "_{}".format(index)
                index += 1

            old_path_file = self.filePath + "/{}".format(currentAlgorithm.algorithmParameter.name)
            new_path_file = self.filePath + "/{}".format(newAlgorithmName)
            PathFileControl.copyTree(old_path_file, new_path_file)

            newAlgorithm = Algorithm(self.filePath + "/{}".format(newAlgorithmName), self.mainWindow, self.maxStep)
            newAlgorithm.algorithmParameter.name = newAlgorithmName
            if newAlgorithm.save():
                self.changeCurrentAlgorithm(newAlgorithmName)
                self.updateList()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Duplicate Algorithm: {}".format(error))
            messagebox.showerror("Duplicate Algorithm", "{}".format(error))

    def deleteCurrentAlgorithm(self):
        path = self.filePath + "/" + self.getCurrentAlgorithm().algorithmParameter.name
        try:
            if PathFileControl.deleteFolder(path):
                messagebox.showinfo("Delete Algorithm", "Delete Algorithm successfully!")
            else:
                messagebox.showerror("Delete Algorithm", "Delete Algorithm failed!")

            self.updateList()
            self.mainWindow.researchingTab.updateAlgorithmForNewList()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Delete current algorithm: {}".format(error))
            messagebox.showerror("Delete current algorithm", "Detail: {}".format(error))

    def deleteAlgorithmWithName(self, algorithmName):
        path = self.filePath + "/" + algorithmName
        try:
            if PathFileControl.deleteFolder(path):
                messagebox.showinfo("Delete Algorithm", "Delete Algorithm successfully!")
            else:
                messagebox.showerror("Delete Algorithm", "Delete Algorithm failed!")

            self.get()
            self.mainWindow.researchingTab.updateAlgorithmForChangeModel()
            self.mainWindow.modelSettingTab.syc_model_setting_frame.updateAlgorithmList()
            self.mainWindow.modelSettingTab.rearCheckMissingFrame.updateAlgorithmList()
            self.mainWindow.modelSettingTab.locationDetectSettingFrame.updateAlgorithmList()
            self.mainWindow.modelSettingTab.demo_color_detect_setting_frame.updateAlgorithmList()
            self.mainWindow.modelSettingTab.demo_location_detect_setting_frame.updateAlgorithmList()
            self.mainWindow.modelSettingTab.roto_weighing_robot_model_setting_frame.updateAlgorithmList()
            self.mainWindow.modelSettingTab.e_map_model_setting.updateAlgorithmList()
            self.mainWindow.modelSettingTab.counting_in_conveyor_setting.updateAlgorithmList()
            self.mainWindow.modelSettingTab.read_weighing_model_setting.updateAlgorithmList()


        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Delete current algorithm: {}".format(error))
            messagebox.showerror("Delete current algorithm", "Detail: {}".format(error))

    def changeCurrentAlgorithm(self, currentName):
        self.currentName = currentName
        # self.currentIndex = currentIndex
        filePath = self.filePath + "/index.txt"
        file = TextFile(filePath)
        file.dataList = ["{}".format(self.currentName)]
        # print("current Algorithm save: {}".format(file.dataList))
        file.saveFile()

    def getCurrentAlgorithm(self):
        for algorithm in self.algorithmList:
            if algorithm.algorithmParameter.name == self.currentName:
                return algorithm

        if len(self.algorithmList) > 0:
            return self.algorithmList[0]

    def getAlgorithmWithName(self, algorithmName):
        for algorithm in self.algorithmList:
            if algorithm.algorithmParameter.name == algorithmName:
                return algorithm

        return None

    def reset_last_execute_step(self):
        for algorithm in self.algorithmList:
            algorithm.last_execute_step = None
