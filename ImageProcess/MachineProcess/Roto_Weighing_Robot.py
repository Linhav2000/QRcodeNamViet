from ImageProcess.Algorithm.Algorithm import Algorithm, AlgorithmResult
from Modules.ModelSetting.ModelParameter import ModelParameter
from Connection.Camera import Camera
from ImageProcess.Algorithm.MethodList import *
from Modules.ModelSetting.CAS_Type import CAS_Type
from CommonAssit.CommunicationReceiveAnalyze import CommunicationReceiveInfo
from CommonAssit import CommunicationReceiveAnalyze, Color
from Modules.AxisSystem.AS_Parameter import AS_Parameter
from ImageProcess import ImageProcess
import cv2 as cv
from CommonAssit import TimeControl


class Roto_Weighing_Robot:
    rotoAlgorithmStep0: Algorithm = None
    rotoAlgorithmStep1: Algorithm = None
    currentModel: ModelParameter
    currentCamera: Camera
    current_as: AS_Parameter

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow

    def updateModel(self):
        # self.currentModel = self.mainWindow.runningTab.modelManager.models[self.mainWindow.runningTab.modelManager.currentModelPos]
        self.currentModel = self.mainWindow.runningTab.modelManager.getCurrentModel()
        if self.currentModel is None:
            return
        for algorithm in self.mainWindow.algorithmManager.algorithmList:
            if algorithm.algorithmParameter.name == self.currentModel.rotoAlgorithmStep0:
                self.rotoAlgorithmStep0 = algorithm
        self.rotoAlgorithmStep0 = self.mainWindow.algorithmManager.getAlgorithmWithName(
            self.currentModel.rotoAlgorithmStep0)
        self.rotoAlgorithmStep1 = self.mainWindow.algorithmManager.getAlgorithmWithName(
            self.currentModel.rotoAlgorithmStep1)

        self.currentCamera = self.mainWindow.workingThread.cameraManager.currentCamera
        self.current_as = self.mainWindow.as_manager.getCurrentAS()

    def startWorking(self, checkAlgorithm=True):
        if checkAlgorithm:
            self.updateModel()
            if self.rotoAlgorithmStep0 is None:
                # messagebox.showwarning("Start Roto Weighing robot", "Still not choose the algorithm")
                self.mainWindow.showError("Still not choose the algorithm")
                return False
        self.currentCamera = self.mainWindow.workingThread.cameraManager.currentCamera

        if not self.currentCamera.ready:
            self.currentCamera.connect()
        if not self.mainWindow.workingThread.connectionManager.isReady():
            self.mainWindow.workingThread.connectionManager.connect()

        self.mainWindow.workingThread.light.connect()

        ret = self.currentCamera.ready and self.mainWindow.workingThread.connectionManager.isReady()
        return ret

    def isConnected(self):
        ret = self.currentCamera.ready and self.mainWindow.workingThread.connectionManager.isConnected()
        return ret

    def executeModel(self, communicationReceive):
        ret = False
        movingCoordinateList = []
        text = ""
        ret, commandInfo, text = CommunicationReceiveAnalyze.get_info_running_form(communicationReceive)
        if not ret:
            return ret, movingCoordinateList, text
        modelName = commandInfo.model
        ret, text = self.updateModelInfo(modelName=modelName)

        self.current_as = self.mainWindow.as_manager.getAS_WithName(commandInfo.axisSystemName)
        if self.current_as is None:
            text = "ERROR Cannot get the Axis System. Please check!"
            return False, movingCoordinateList, text

        if not ret:
            self.mainWindow.runningTab.insertLog(text)
            return False, movingCoordinateList, text

        try:
            commandInfo.x = commandInfo.x / self.current_as.robot_mm_moving_Scale
            commandInfo.y = commandInfo.y / self.current_as.robot_mm_moving_Scale
            commandInfo.z = commandInfo.z / self.current_as.robot_mm_moving_Scale
            commandInfo.u = commandInfo.u / self.current_as.robot_mm_moving_Scale
        except Exception as error:
            text = "ERROR: Check the coordinate or the moving to mm scale"
            self.mainWindow.runningTab.insertLog(text)
            return False, movingCoordinateList, text

        ret, mm_movingCoordinateList, text = self.calculateDeviationCoordinates(receiveInfo=commandInfo)

        if ret:
            try:
                for mm_movingCoordinate in mm_movingCoordinateList:
                    movingCoordinateList.append(self.convert_mm_moving_coor(mm_movingCoordinate, self.current_as))
                return ret, movingCoordinateList, text
            except Exception as error:
                text = "ERROR Send Data to robot: {}".format(error)
                return ret, movingCoordinateList, text

        else:
            return ret, movingCoordinateList, text

    def updateModelInfo(self, modelName):
        self.currentModel, text = self.mainWindow.modelSettingTab.modelManager.getModelByName(modelName=modelName)
        if self.currentModel is None:
            return False, text
        self.rotoAlgorithmStep0 = self.mainWindow.algorithmManager.getAlgorithmWithName(
            self.currentModel.rotoAlgorithmStep0)
        if self.rotoAlgorithmStep0 is None:
            text = "ERROR Cannot get the algorithm for step 0. Please check!"
            return False, text
        self.rotoAlgorithmStep1 = self.mainWindow.algorithmManager.getAlgorithmWithName(
            self.currentModel.rotoAlgorithmStep1)
        if self.rotoAlgorithmStep1 is None:
            text = "ERROR Cannot get the algorithm for step 1. Please check!"
            return False, text
        return True, text

    def calculateDeviationCoordinates(self, receiveInfo: CommunicationReceiveInfo, image=None):
        text = ""
        currentPLCPosX = receiveInfo.x
        currentPLCPosY = receiveInfo.y

        deviationCoordinates = (0, 0)
        workingPosition = [receiveInfo.x, receiveInfo.y]
        workingPositionList = []

        # if receiveInfo.header == CommandType.roto_weighing.value:
        #     try:
        #         self.rotoAlgorithmStep0 = self.mainWindow.algorithmManager.getAlgorithmWithName(receiveInfo.algorithmName)
        #         if self.rotoAlgorithmStep0 is None:
        #             text = "Cannot find the Algorithm. Please check Algorithm Name"
        #             return False, deviationCoordinates, text
        #     except Exception as error:
        #         text = "Cannot find the Algorithm. Detail: {}".format(error)
        #         return False, deviationCoordinates, text
        ret = True
        if image is None:
            try:
                self.mainWindow.runningTab.insertLog("Take image")
                TimeControl.sleep(self.currentModel.delayTakepicTime)
                start_take_pic_time = TimeControl.time()
                ret, image = self.currentCamera.takePicture()
                if (ret and TimeControl.time() - start_take_pic_time < 5) or \
                    (not ret and TimeControl.time() - start_take_pic_time > 1000):
                    self.currentCamera.reconnect()
                    TimeControl.sleep(1000)
                    ret, image = self.currentCamera.takePicture()

                print(f"image shape = {image.shape}")
                self.mainWindow.runningTab.insertLog("Take image Done")
            except Exception as error:
                ret = False
                self.mainWindow.runningTab.insertLog(f"Take image Failed: {error}")

        if not ret:
            # messagebox.showwarning("Take picture", "Cannot take picture\nPlease check the connection or cable!")

            self.mainWindow.runningTab.insertLog(
                "ERROR Take picture: Cannot take picture\nPlease check the connection or cable!")
            text = "ERROR Take picture: Cannot take picture"
            self.mainWindow.showError(text=text)
            workingPositionList.append((0, 0))
            return ret, workingPositionList, text
        else:
            if not self.mainWindow.modelSettingTab.modelTestFlag:
                self.mainWindow.runningTab.insertLog("distort image")
                image = ImageProcess.undistort(image)
                self.mainWindow.runningTab.insertLog("rotate image")
                image = ImageProcess.rotateImageWithStringKey(sourceImage=image, rotateStringKey=self.current_as.rotate)
            self.mainWindow.runningTab.insertLog("Copy to image show")
            ret = False
            imageShow = image.copy()
            try:
                self.mainWindow.runningTab.insertLog("execute step 0")
                if receiveInfo.step == 0:
                    ret, verifiedCircleList, workingPositionList, text = self.execute_algorithm_step_0(
                        image=image, imageShow=imageShow,
                        current_plc_position=(currentPLCPosX, currentPLCPosY))
                elif receiveInfo.step == 1:
                    self.mainWindow.runningTab.insertLog("execute step 1")
                    step0_ret, verifiedCircleList, workingPositionList, text = self.execute_algorithm_step_0(
                        image=image, imageShow=imageShow,
                        current_plc_position=(currentPLCPosX, currentPLCPosY))
                    ret, workingPositionList, text = self.execute_algorithm_step_1(image=image, imageShow=imageShow,
                                                                                   verified_circles=verifiedCircleList)
                self.mainWindow.showImage(imageShow)
            except Exception as error:
                # messagebox.showerror("Calculate Deviation Coordinates", "Detail: {}".format(error))
                text = "ERROR Calculate Deviation Coordinates: {}".format(error)
                self.mainWindow.runningTab.insertLog(text)
                self.mainWindow.showError(text)
                self.mainWindow.showImage(image)
                workingPositionList.append((0, 0))
                ret = False
        self.mainWindow.runningTab.insertLog("current Robot position = {}, {}".format(currentPLCPosX, currentPLCPosY))
        self.mainWindow.runningTab.insertLog("Deviation X, Y = {}".format(deviationCoordinates))
        self.mainWindow.runningTab.insertLog("Robot working position = {}".format(workingPosition))
        return ret, workingPositionList, text

    def execute_algorithm_step_0(self, image, imageShow, current_plc_position):
        workingPositionList = []
        currentPLCPosX, currentPLCPosY = current_plc_position
        self.mainWindow.runningTab.insertLog("Execute algorithm step 0")
        ret, resultList, text = self.rotoAlgorithmStep0.executeAlgorithm(image=image, imageName="Roto_weighing")
        imageCenterX = image.shape[1] / 2
        imageCenterY = image.shape[0] / 2
        # currentCoordinateX, currentCoordinateY = (imageCenterX, imageCenterY)
        circleList = []
        verifiedCircleList = []
        self.mainWindow.runningTab.insertLog("finding circle")
        if ret:
            ret = False
            result: AlgorithmResult
            for result in resultList:
                if result.methodName == MethodList.averageHoughCircle.value and result.passed:
                    ret = True
                    circleList = result.circleList

                elif result.methodName == MethodList.matchingTemplate.value:
                    detectArea = result.detectAreaList[0]
                    currentCoordinateX = ((detectArea[0] + detectArea[2]) / 2)
                    currentCoordinateY = ((detectArea[1] + detectArea[3]) / 2)
                    cv.circle(imageShow, center=(currentCoordinateX, currentCoordinateY), radius=10,
                              color=(0, 255, 0), thickness=-1, lineType=cv.LINE_AA)
                    ret = True
        self.mainWindow.runningTab.insertLog("Convert circle to plc axis")
        if ret:

            if not self.currentModel.rw_multiPoint:
                verifiedCircleList = self.verify_circle_list(circleList=circleList,
                                                             imageCenterX=imageCenterX, imageCenterY=imageCenterY)
            else:
                verifiedCircleList = circleList

            for circle in verifiedCircleList:
                currentCoordinateX, currentCoordinateY = circle[0]
                cv.circle(imageShow, center=(currentCoordinateX, currentCoordinateY),
                          radius=10, color=(0, 255, 0), thickness=-1, lineType=cv.LINE_AA)

                deviationCoordinates = self.get_deviation_coordinates(currentCoordinateX=currentCoordinateX,
                                                                      currentCoordinateY=currentCoordinateY,
                                                                      imageCenterX=imageCenterX,
                                                                      imageCenterY=imageCenterY)

                workingPosition = (
                    currentPLCPosX + deviationCoordinates[0], currentPLCPosY + deviationCoordinates[1])

                workingPositionList.append(workingPosition)

        return ret, verifiedCircleList, workingPositionList, text

    def verify_circle_list(self, circleList, imageCenterX, imageCenterY):
        minDist = None
        chosenCircle = None
        for circle in circleList:
            circleCenter = circle[0]
            centerImage = (imageCenterX, imageCenterY)

            currentDist = ImageProcess.calculateDistanceBy2Points(circleCenter, centerImage)

            if minDist is None:
                minDist = currentDist
                chosenCircle = circle
            else:
                if currentDist < minDist:
                    chosenCircle = circle
                    minDist = currentDist
        verifiedCircleList = [chosenCircle]
        return verifiedCircleList

    def get_deviation_coordinates(self, currentCoordinateX, currentCoordinateY, imageCenterX, imageCenterY):
        deviationCoordinates = (0, 0)
        pixelDeltaX = currentCoordinateX - imageCenterX
        pixelDeltaY = currentCoordinateY - imageCenterY

        imageDeltaX = pixelDeltaX * self.current_as.robot_pixel_mm_Scale
        imageDeltaY = pixelDeltaY * self.current_as.robot_pixel_mm_Scale

        if self.current_as.casType == CAS_Type.robot_x_pos_y_pos.value:
            deviationCoordinates = (self.current_as.robotOffset[0] + imageDeltaX,
                                    self.current_as.robotOffset[1] + imageDeltaY)
        elif self.current_as.casType == CAS_Type.robot_x_y_exchanged.value:
            deviationCoordinates = (self.current_as.robotOffset[0] + imageDeltaY,
                                    self.current_as.robotOffset[1] + imageDeltaX)
        elif self.current_as.casType == CAS_Type.robot_x_inv_y_pos.value:
            deviationCoordinates = (self.current_as.robotOffset[0] - imageDeltaX,
                                    self.current_as.robotOffset[1] + imageDeltaY)
        elif self.current_as.casType == CAS_Type.robot_x_y_exchanged_y_inv.value:
            deviationCoordinates = (self.current_as.robotOffset[0] + imageDeltaY,
                                    self.current_as.robotOffset[1] - imageDeltaX)
        return deviationCoordinates

    def execute_algorithm_step_1(self, image, verified_circles, imageShow):
        text = ""
        workingPositionList = []
        if len(verified_circles) > 0:
            self.set_center_circle_for_select_area_step1(verified_circles=verified_circles)

        ret, resultList, text = self.rotoAlgorithmStep1.executeAlgorithm(image=image, imageName="Roto_weighing")
        if ret:
            ret = False
            result: AlgorithmResult
            for result in resultList:
                if result.methodName == MethodList.bgrInRange.value or \
                        result.methodName == MethodList.hsvInRange.value or \
                        result.methodName == MethodList.hlsInRange.value or \
                        result.methodName == MethodList.countNonzero.value:
                    ret = ret or result.passed
                    color = Color.cvGreen() if result.passed else Color.cvRed()
                    cv.rectangle(img=imageShow, pt1=(result.workingArea[0] + result.basePoint[0],
                                                     result.workingArea[1] + result.basePoint[1]),
                                 pt2=(result.workingArea[2] + result.basePoint[0],
                                      result.workingArea[3] + result.basePoint[1]),
                                 color=color if ret else (0, 0, 255),
                                 thickness=self.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)
                    if self.mainWindow.modelSettingTab.modelTestFlag:
                        self.mainWindow.showImage(self.rotoAlgorithmStep1.imageList[result.stepId])
                        TimeControl.sleep(1000)
                elif result.methodName == MethodList.matchingTemplate.value:
                    ret = ret or result.passed
                elif result.methodName == MethodList.findContour.value:
                    ret = ret or result.passed
            if not ret:
                text = "Không thấy tai roto"

        workingPositionList.append((0, 0))
        return ret, workingPositionList, text

    def set_center_circle_for_select_area_step1(self, verified_circles):
        deltaX = 0
        deltaY = 0

        for step in self.rotoAlgorithmStep1.algorithmParameter.steps:
            if step.stepAlgorithmName == MethodList.multi_select_area.value:
                select_areas_list = []
                for area, area_type in step.select_areas_list:
                    if area_type == "circle":
                        select_areas_list.append(((verified_circles[0][0], area[1]), area_type))
                        if deltaX == 0:
                            deltaX = verified_circles[0][0][0] - area[0][0]
                            deltaY = verified_circles[0][0][1] - area[0][1]
                step.select_areas_list = select_areas_list

            if step.stepAlgorithmName == MethodList.countNonzero.value or \
                    step.stepAlgorithmName == MethodList.bgrInRange.value or \
                    step.stepAlgorithmName == MethodList.hsvInRange.value or \
                    step.stepAlgorithmName == MethodList.hlsInRange.value:
                step.workingArea = [step.workingArea[0] + deltaX,
                                    step.workingArea[1] + deltaY,
                                    step.workingArea[2] + deltaX,
                                    step.workingArea[3] + deltaY]

    def convert_mm_moving_coor(self, coordinates, as_parameter=None):
        if as_parameter is None:
            current_as = self.mainWindow.as_manager.getCurrentAS()
        else:
            current_as = as_parameter
        movingCoordinates = []
        for coordinate in coordinates:
            movingCoordinates.append(int(coordinate * current_as.robot_mm_moving_Scale))

        return movingCoordinates
