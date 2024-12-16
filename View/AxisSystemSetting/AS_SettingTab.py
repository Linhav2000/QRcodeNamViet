from tkinter import messagebox
from View.AxisSystemSetting.NewAxisSystemWindow import NewAxisSystemWindow
from Modules.ModelSetting.DisplayParamFrame import DisplayParamFrame
from View.ModelSetting.RoboWeighingRobot.CASTypeSelectWindow import CASTypeSelectWindow
from Modules.AxisSystem.AS_Parameter import AS_Parameter
from View.Common.CommonStepFrame import *
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from ImageProcess import ImageProcess
from Modules.ModelSetting.CAS_Type import CAS_Type
from Modules.Camera.CameraParameter import CameraRotate
from Modules.ModelSetting.Algorithm_Choose import Algorithm_Choose
from ImageProcess.Algorithm.Algorithm import Algorithm
from ImageProcess.Algorithm.AlgorithmResult import AlgorithmResult, AlgorithmResultKey
from ImageProcess.Algorithm.MethodList import MethodList
from View.AxisSystemSetting.Coordinate_Input import Coordinate_Input
import cv2 as cv
import copy

class AS_Type(enum.Enum):
    on_robot_hand = "On Robot Hand"
    fixed_camera = "Fixed Camera"

class AS_SettingTab(VisionFrame):
    btnASAddNew: AddButton
    btnAS_Delete: DeleteButton
    btnAS_Save: SaveButton
    btnDuplicate: CopyButton

    as_nameLabel: VisionLabel
    nameEntry: VisionEntry
    asComboBox: ttk.Combobox
    asNameList = []

    current_parameter_frame = None
    parameterFrame_OnHandType: VisionLabelFrame = None
    mm_moving_Scale: InputParamFrame
    delayTime: InputParamFrame
    exceptDelta: InputParamFrame
    robot_coordinates_type: DisplayParamFrame
    btnSelectRobotCASType: VisionButton
    pixel_mm_Scale: InputParamFrame
    btnGetScale: VisionButton
    offsetLabel: VisionLabel
    offsetXEntry: VisionEntry
    offsetYEntry: VisionEntry
    btnGetOffset: VisionButton
    asLabel:VisionLabel
    as_nameLabel:VisionLabel
    as_type_label:VisionLabel
    parameterFrame_OnHandType:VisionLabelFrame
    preProcess_algorithm: Algorithm_Choose

    as_type_label: VisionLabel
    as_type_comb: ttk.Combobox
    current_as_type = ""

    parameterFrame_FixedCamType: VisionLabelFrame = None
    image_point1: Coordinate_Input
    btnGetImagePoint: VisionButton
    btnGetRobotPoint: VisionButton
    image_point2: Coordinate_Input
    image_point3: Coordinate_Input
    robot_point1: Coordinate_Input
    robot_point2: Coordinate_Input
    robot_point3: Coordinate_Input

    getOffsetFlag = False
    caliOffsetFlag = False

    offsetCenter = (0, 0)
    beginCenter = (0, 0)
    endCenter = (0, 0)

    cameraPos = [0, 0]
    workingPos = [0, 0]

    minArea = 0
    maxArea = 0

    yDistance = 35
    xDistance = 150

    def __init__(self, root, mainWindow):
        VisionFrame.__init__(self, root)
        self.mainWindow = mainWindow
        self.setupView()
        self.notifyRegister()
    def setupView(self):
        # self.setupParameterFrame()
        self.setup_as_name_change()
        self.setupBtnTakePic()
        self.setupBtnSelectImage()
        self.setup_as_type()
        self.setup_as_combo()
        self.setupBtnAddNew()
        self.setupDuplicateButton()
        self.setupBtnDelete()
        self.setupBtnSave()

        current_as: AS_Parameter = self.mainWindow.as_manager.getCurrentAS()
        self.current_as_type = current_as.as_type if current_as is not None else AS_Type.on_robot_hand.value

        self.show_parameter_frame()
        self.showCurrentASParam()
    def notifyRegister(self):
        self.mainWindow.notificationCenter.add_observer(with_block=self.changeLanguage, for_name="ChangeLanguage")
    def changeLanguage(self, sender, notification_name, info):
        self.asLabel.config(text= self.mainWindow.languageManager.localized("axis system"))
        self.as_nameLabel.config(text= self.mainWindow.languageManager.localized("as name"))
        self.as_type_label.config(text=self.mainWindow.languageManager.localized("as type"))
        self.parameterFrame_OnHandType.config(text=self.mainWindow.languageManager.localized("parameter"))
    def setup_as_combo(self):
        self.asLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("axis system"))
        self.asLabel.place(relx=0.02, rely=0.02)

        self.asNameList = self.mainWindow.as_manager.getNameList()
        self.asComboBox = ttk.Combobox(self, value=self.asNameList, state='readonly', cursor="hand2")
        self.asComboBox.bind("<<ComboboxSelected>>", self.asSelectChange)
        self.asComboBox.place(relx=0.25, rely=0.02)
        try:
            self.asComboBox.current(self.mainWindow.as_manager.getCurrentPos())
        except:
            pass


    def asSelectChange(self, event):
        if self.isChanged():
            askSave = messagebox.askyesno("Change Axis System Setting",
                                          "There are some changes. Do you wanna save this setting?")
            if askSave:
                if self.mainWindow.as_manager.currentName != self.nameEntry.get() and\
                        self.mainWindow.as_manager.as_name_existed(self.nameEntry.get()):
                    askChange = messagebox.askyesno("Axis System Name", "The AS name \"{}\" is existed, Do you want to change another name?\nyes = stay and change\nno = move without saving".format(self.nameEntry.get()))
                    if askChange:
                        self.asComboBox.current(self.mainWindow.as_manager.getCurrentPos())
                        return
                else:
                    self.save()
        self.mainWindow.as_manager.changeCurrentAS(self.asNameList[self.asComboBox.current()])
        self.show_parameter_frame()
        self.showCurrentASParam()

    def setupBtnTakePic(self):
        btnTakePic = TakePicButton(self, self.mainWindow.workingThread.capturePicture)
        btnTakePic.place(relx=0.68, rely=0.02, relwidth=0.2, relheight = 0.05)

    def setupBtnSelectImage(self):
        btnSelectImage = ImageButton(self, imagePath="./resource/open_image.png",command=self.mainWindow.workingThread.openImage)
        btnSelectImage.place(relx=0.68, rely=0.08, relwidth=0.2, relheight = 0.05)

    def setup_as_name_change(self):
        # Name entry
        self.as_nameLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("as name"))
        self.as_nameLabel.place(relx=0.02, rely=0.069)

        self.nameEntry = VisionEntry(self)
        self.nameEntry.place(relx=0.25, rely=0.069, width=180, height=20)

    def setup_as_type(self):
        self.as_type_label = VisionLabel(self, text=self.mainWindow.languageManager.localized("as type"))
        self.as_type_label.place(relx=0.02, rely=0.11)

        as_type_list = [as_type.value for as_type in AS_Type]
        self.as_type_comb = ttk.Combobox(self, value=as_type_list, state='readonly', cursor="hand2")
        self.as_type_comb.bind("<<ComboboxSelected>>", self.as_type_select_change)
        self.as_type_comb.place(relx=0.25, rely=0.11)

    def as_type_select_change(self, event):
        ask_change = messagebox.askokcancel("Change Axis System Type", "If you change the Axis System Type, all current data will be saved!")
        if not ask_change:
            return
        self.current_as_type = self.as_type_comb.get()
        self.show_parameter_frame()
        self.showCurrentASParam()

    def show_parameter_frame(self):
        if self.current_parameter_frame is not None:
            self.current_parameter_frame.place_forget()

        if self.current_as_type == AS_Type.on_robot_hand.value:
            self.show_on_hand_parameter_frame()
            self.current_parameter_frame = self.parameterFrame_OnHandType
        elif self.current_as_type == AS_Type.fixed_camera.value:
            self.show_fixed_camera_parameter_frame()
            self.current_parameter_frame = self.parameterFrame_FixedCamType

    def show_on_hand_parameter_frame(self):
        if self.parameterFrame_OnHandType is not None:
            self.parameterFrame_OnHandType.place(relx=0.01, rely=0.18, relwidth=0.98, relheight=0.72)
        else:
            listRotate = []
            for rotate in CameraRotate:
                listRotate.append(rotate.value)

            self.parameterFrame_OnHandType = VisionLabelFrame(self, text=self.mainWindow.languageManager.localized("parameter"))
            self.parameterFrame_OnHandType.place(relx=0.01, rely=0.18, relwidth=0.98, relheight=0.72)

            self.robot_coordinates_type = DisplayParamFrame(self.parameterFrame_OnHandType, "Robot coordinates type :",
                                                            yPos=5 + 0 * self.yDistance,
                                                            height=self.yDistance)

            # self.robot_coordinates_type = DisplayParamFrame(DisplayParamFrame,text=self.mainWindow.languageManager.localized("coordinates type"))
            # self.robot_coordinates_type.place(yPos=5+0*self.yDistance,height=self.yDistance)
            self.btnSelectRobotCASType = VisionButton(self.parameterFrame_OnHandType, text="Select",
                                                      command=self.clickBtnSelectCASType)
            self.btnSelectRobotCASType.place(x=320, y=5 + 0 * self.yDistance, width=100, height=25)

            self.mm_moving_Scale = InputParamFrame(self.parameterFrame_OnHandType, "mm to moving Scale :",
                                                   yPos=5 + 1 * self.yDistance,
                                                   height=self.yDistance, width=100)

            self.delayTime = InputParamFrame(self.parameterFrame_OnHandType, "Delay time (ms) :",
                                             yPos=5 + 2 * self.yDistance, height=self.yDistance,
                                             width=100)

            self.exceptDelta = InputParamFrame(self.parameterFrame_OnHandType, "Except Delta (pixel) :",
                                               yPos=5 + 3 * self.yDistance,
                                               height=self.yDistance, width=100)

            self.rotate = ComboForFlexibleValue(self.parameterFrame_OnHandType, "Rotate : ",
                                                yPos=5 + 4 * self.yDistance,
                                                height=self.yDistance, valueList=listRotate)

            self.pixel_mm_Scale = InputParamFrame(self.parameterFrame_OnHandType, "Pixel to mm scale :",
                                                  yPos=5 + 5 * self.yDistance,
                                                  height=self.yDistance, width=100)

            self.btnGetScale = VisionButton(self.parameterFrame_OnHandType, text="Get scale",
                                            command=self.clickBtnGetScale)
            self.btnGetScale.place(x=320, y=5 + 5 * self.yDistance, width=100, height=25)

            self.offsetLabel = VisionLabel(self.parameterFrame_OnHandType, text="Offset value : ")
            self.offsetLabel.place(x=5, y=5 + 6 * self.yDistance, height=self.yDistance)

            self.offsetXEntry = VisionEntry(self.parameterFrame_OnHandType)
            self.offsetXEntry.place(x=150, y=5 + 6 * self.yDistance, width=70, height=25)

            self.offsetYEntry = VisionEntry(self.parameterFrame_OnHandType)
            self.offsetYEntry.place(x=230, y=5 + 6 * self.yDistance, width=70, height=25)

            self.btnGetOffset = VisionButton(self.parameterFrame_OnHandType, text="Get Offset",
                                             command=self.clickBtnGetOffset)
            self.btnGetOffset.place(x=320, y=5 + 6 * self.yDistance, width=100, height=25)

            algorithmList = [algorithm.algorithmParameter.name for algorithm in self.mainWindow.algorithmManager.algorithmList]

            self.preProcess_algorithm = Algorithm_Choose(self.parameterFrame_OnHandType, "Pre-Process algorithm: ",
                                                         yPos=5 + 7 * self.yDistance, height=self.yDistance,
                                                         valueList=algorithmList, mainWindow=self.mainWindow)
    def show_fixed_camera_parameter_frame(self):
        if self.parameterFrame_FixedCamType is not None:
            self.parameterFrame_FixedCamType.place(relx=0.01, rely=0.18, relwidth=0.98, relheight=0.72)
        else:
            self.parameterFrame_FixedCamType = VisionLabelFrame(self, text="Parameters")
            self.parameterFrame_FixedCamType.place(relx=0.01, rely=0.18, relwidth=0.98, relheight=0.72)
            self.image_point1 = Coordinate_Input(self.parameterFrame_FixedCamType, "Image point 1",
                                                 yPos=5 + 1 * self.yDistance, height=self.yDistance, rel_width=0.75)

            self.image_point2 = Coordinate_Input(self.parameterFrame_FixedCamType, "Image point 2",
                                                 yPos=5 + 2 * self.yDistance, height=self.yDistance, rel_width=0.75)
            self.image_point3 = Coordinate_Input(self.parameterFrame_FixedCamType, "Image point 3",
                                                 yPos=5 + 3 * self.yDistance, height=self.yDistance, rel_width=0.75)
            self.robot_point1 = Coordinate_Input(self.parameterFrame_FixedCamType, "Robot point 1",
                                                 yPos=5 + 4 * self.yDistance, height=self.yDistance, rel_width=0.75)
            self.robot_point2 = Coordinate_Input(self.parameterFrame_FixedCamType, "Robot point 2",
                                                 yPos=5 + 5 * self.yDistance, height=self.yDistance, rel_width=0.75)
            self.robot_point3 = Coordinate_Input(self.parameterFrame_FixedCamType, "Robot point 3",
                                                 yPos=5 + 6 * self.yDistance, height=self.yDistance, rel_width=0.75)
            algorithmList = [algorithm.algorithmParameter.name for algorithm in self.mainWindow.algorithmManager.algorithmList]
            self.getImagePointAlgorithm = Algorithm_Choose(self.parameterFrame_FixedCamType,
                                                           lblText="Get Points Algorithm",
                                                           yPos=5 + 7 * self.yDistance, height=self.yDistance,
                                                           valueList=algorithmList, mainWindow=self.mainWindow)

            self.btnGetImagePoint = VisionButton(self.parameterFrame_FixedCamType, text= "Get Image Points", command=self.getImagePoints)
            self.btnGetImagePoint.place(relx=0.1, y=5 + 8 * self.yDistance + 2, height=self.yDistance, heigh=self.yDistance - 2)
            self.btnGetRobotPoint = VisionButton(self.parameterFrame_FixedCamType, text= "Get Robot Points", command=self.getRobotPoints)
            self.btnGetRobotPoint.place(relx=0.4, y=5 + 8 * self.yDistance + 2 , height=self.yDistance, heigh=self.yDistance - 2)
            self.btnTestAffine = VisionButton(self.parameterFrame_FixedCamType, text="Test Affine", command=self.testAffine)
            self.btnTestAffine.place(relx=0.7, y=5 + 8 * self.yDistance + 2, height=self.yDistance, heigh=self.yDistance - 2)

    def testAffine(self):
        currentAlgorithm: Algorithm = self.mainWindow.algorithmManager.getCurrentAlgorithm()
        currentImage = self.mainWindow.originalImage.copy()

        ret, result_list, text = currentAlgorithm.executeAlgorithm(image=currentImage)
        result: AlgorithmResult
        point = None
        for result in result_list:
            if result.methodName == MethodList.findContour.value:
                point = result.getValue(AlgorithmResultKey.point.value)
                if point is not None:
                    point = (point[0] + result.workingArea[0] + result.basePoint[0],
                             point[1] + result.workingArea[1] + result.basePoint[1])
        robot_point = None
        if point is not None:
            current_as_param: AS_Parameter = self.mainWindow.as_manager.getCurrentAS()
            robot_point = ImageProcess.transformPointWithMatrix(point=point, matrix=current_as_param.transform_matrix)
        if robot_point is not None:
            image = cv.imdecode(np.fromfile(r"D:\Duc\Document\Project\TSB\FPCB_Inspection\picture\robot_points.png", dtype=np.uint8), cv.IMREAD_COLOR)
            cv.circle(image, center=(int(robot_point[0]), int(robot_point[1])), radius=20, color=(0, 255, 0), thickness=-1, lineType=cv.LINE_AA)
            self.mainWindow.showImage(image)

    def getImagePoints(self):
        getImagePointsAlgorithm: Algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName(self.getImagePointAlgorithm.getValue())
        currentImage = self.mainWindow.originalImage.copy()

        ret, result_list, text = getImagePointsAlgorithm.executeAlgorithm(image=currentImage)
        result: AlgorithmResult
        points = []
        if ret:
            for result in result_list:
                if result.methodName == MethodList.findContour.value:
                    point = result.getValue(AlgorithmResultKey.point.value)
                    if point is not None:
                        point = (point[0] + result.workingArea[0] + result.basePoint[0],
                                 point[1] + result.workingArea[1] + result.basePoint[1])
                    points.append(point)

        self.image_point1.setValue(points[0])
        self.image_point2.setValue(points[1])
        self.image_point3.setValue(points[2])

    def getRobotPoints(self):
        currentAlgorithm: Algorithm = self.mainWindow.algorithmManager.getCurrentAlgorithm()
        currentImage = self.mainWindow.originalImage.copy()

        ret, result_list, text = currentAlgorithm.executeAlgorithm(image=currentImage)
        result: AlgorithmResult
        points = []
        if ret:
            for result in result_list:
                if result.methodName == MethodList.findContour.value:
                    point = result.getValue(AlgorithmResultKey.point.value)
                    if point is not None:
                        point = (point[0] + result.workingArea[0] + result.basePoint[0],
                                 point[1] + result.workingArea[1] + result.basePoint[1])
                    points.append(point)

        self.robot_point1.setValue(points[0])
        self.robot_point2.setValue(points[1])
        self.robot_point3.setValue(points[2])

    def clickBtnGetScale(self):
        self.save(notification=False)
        if self.mainWindow.workingThread.roto_weighing_robot.startWorking(checkAlgorithm=False):
            machineName = self.mainWindow.startingWindow.machineName
            if machineName.is_roto_weighing_robot():
                if self.mainWindow.workingThread.roto_weighing_robot.isConnected():
                    self.caliOffsetFlag = True
                else:
                    self.mainWindow.showError("Not ready to get scale\nRobot is not connected!")
                    # messagebox.showerror("Get scale",
                    #                      "Not ready to take scale\nRobot is not connected!")
            else:
                self.caliOffset()
        else:
            self.mainWindow.showError(
                "Not ready to take Scale\nPlease check camera, communication or algorithm!")
    def caliOffset(self, robotPos=None):
        if robotPos is None:
            robotPosX = 0
            robotPosY = 0
        else:
            robotPosX = robotPos[0]
            robotPosY = robotPos[1]
        self.cameraPos = (robotPosX, robotPosY)

        moveFlag = False
        delta = (0, 0)

        try:
            ret, image = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
            self.mainWindow.showImage(image, True)
            if ret:
                # image = ImageProcess.undistort(image)
                image = ImageProcess.rotateImageWithStringKey(sourceImage=image,rotateStringKey=self.rotate.getValue())
                if robotPos is None:
                    (coefficient, self.beginCenter, self.endCenter), self.offsetCenter, (self.minArea, self.maxArea) = self.getSystemOffset(sourceImage=image)
                else:
                    (coefficient, self.beginCenter, self.endCenter), self.offsetCenter, (self.minArea, self.maxArea) = self.getSystemOffset(sourceImage=image,
                                                                                                                                                    _minArea=self.minArea,
                                                                                                                                                    _maxArea=self.maxArea)

                stringPrint = "coefficient = {}, beginCenter = {}, endCenter = {}, offsetCenter = {}".format(coefficient,
                                                                                                   self.beginCenter,
                                                                                                   self.endCenter,
                                                                                                   self.offsetCenter)
                self.mainWindow.runningTab.insertLog(stringPrint)
                self.mainWindow.showBottomMiddleText(stringPrint)

                if robotPos is None:
                    self.pixel_mm_Scale.setValue(coefficient)
                else:
                    coefficient = self.pixel_mm_Scale.getFloatValue()

                centerImageY = int(image.shape[0] / 2)
                centerImageX = int(image.shape[1] / 2)
                if ret:
                    (currentCoordinateX, currentCoordinateY) = self.offsetCenter
                    pixelDeltaX = currentCoordinateX - centerImageX
                    pixelDeltaY = currentCoordinateY - centerImageY
                    exceptDelta = self.exceptDelta.getIntValue()
                    if pixelDeltaX > exceptDelta or pixelDeltaY > exceptDelta or pixelDeltaX < -exceptDelta or pixelDeltaY < -exceptDelta:
                        deltaX = pixelDeltaX * coefficient
                        deltaY = pixelDeltaY * coefficient

                        casType = self.robot_coordinates_type.getValue()
                        # if casType == CAS_Type.robot_x_pos_y_pos.value:
                        #     self.cameraPos = (robotPosX + deltaX, robotPosY + deltaY)
                        # elif casType == CAS_Type.robot_x_y_exchanged.value:
                        #     self.cameraPos = (robotPosX + deltaY, robotPosY + deltaX)
                        # elif casType == CAS_Type.robot_x_inv_y_pos.value:
                        #     self.cameraPos = (robotPosX - deltaX, robotPosY + deltaY)
                        # elif casType == CAS_Type.robot_x_y_exchanged_y_inv.value:
                        #     self.cameraPos = (robotPosX + deltaY, robotPosY - deltaX)
                        if casType == CAS_Type.robot_x_pos_y_pos.value:
                            delta = (deltaX, deltaY)
                        elif casType == CAS_Type.robot_x_y_exchanged.value:
                            delta = ( deltaY, deltaX)
                        elif casType == CAS_Type.robot_x_inv_y_pos.value:
                            delta = (-deltaX, deltaY)
                        elif casType == CAS_Type.robot_x_y_exchanged_y_inv.value:
                            delta = (deltaY, -deltaX)
                        moveFlag = True

            else:
                self.mainWindow.showError("Cannot take the picture!")
                # messagebox.showwarning("Get Measurement Scale", "Cannot take the picture!")
                self.mainWindow.runningTab.insertLog("ERROR Get Measurement Scale: Cannot take the picture")
                moveFlag = False

        except Exception as error:
            moveFlag = False
            # messagebox.showwarning("Get Measurement Scale", "{}".format(error))
            self.mainWindow.runningTab.insertLog("ERROR Get Measurement Scale: {}".format(error))
            self.mainWindow.showError("ERROR Get Measurement Scale: {}".format(error))

        return moveFlag, delta

    def clickBtnGetOffset(self):
        self.save(notification=False)
        if self.mainWindow.workingThread.roto_weighing_robot.startWorking(checkAlgorithm=False):

            if self.mainWindow.workingThread.roto_weighing_robot.isConnected():
                self.getOffsetFlag = True
            else:
                self.mainWindow.showError("Not ready to take offset\nRobot is not connected!")
        else:
            self.mainWindow.showError("Not ready to take offset\nPlease check camera, communication or algorithm!")
            # messagebox.showerror("Get scale", "Not ready to take scale\nPlease check camera, communication or algorithm!")

    def getSystemOffset(self, sourceImage, _minArea=None, _maxArea=None):
        coefficient = 1
        offsetCenter = (0, 0)
        beginCenter = (0, 0)
        endCenter = (0, 0)

        _image = sourceImage.copy()
        # convert to gray image if needed
        # if len(_image.shape) > 2:
        #     _image = ImageProcess.processCvtColor(_image, cv.COLOR_BGR2GRAY)
        pre_process_algorithm: Algorithm = None
        try:
            pre_process_algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName(self.preProcess_algorithm.getValue())
        except Exception as error:
            self.mainWindow.runningTab.insertLog(f"ERROR, get pre-process algorithm {error}")
        if pre_process_algorithm is None:
            return
        ret, result_list, text = pre_process_algorithm.executeAlgorithm(_image)
        result: AlgorithmResult
        erodeImage = None
        for result in result_list:
            if result.methodName == MethodList.erode.value:
                erodeImage = pre_process_algorithm.imageList[result.stepId]
                self.mainWindow.showImage(erodeImage)

        if _maxArea is None:
            # get all circles
            _, totalContoursArea, contourImage = ImageProcess.processFindContours(erodeImage, minArea=100,
                                                                     maxArea=int(
                                                                         erodeImage.shape[0] * erodeImage.shape[1] / 2),
                                                                     maxWidth=erodeImage.shape[1] / 2,
                                                                     maxHeight=erodeImage.shape[0] / 2)
            # define the cofficient point scope
            totalContoursNum = len(totalContoursArea)

            zeroCounted = ImageProcess.processCountNonzero(erodeImage)
            maxArea = int(zeroCounted / totalContoursNum)
            minArea = int(maxArea / 5)

            # determine offset point
            ret, bigContours, contourImage = ImageProcess.processFindContours(erodeImage, minArea=maxArea,
                                                                 maxArea=int(
                                                                     erodeImage.shape[0] * erodeImage.shape[1] / 2),
                                                                 maxWidth=erodeImage.shape[1] / 3 * 2,
                                                                 maxHeight=erodeImage.shape[0] / 3 * 2)

            offsetContour = bigContours[0]
            offsetCenter = (
            int((offsetContour[0] + offsetContour[2]) / 2), int((offsetContour[1] + offsetContour[3]) / 2))
            print("offset center {}".format(offsetCenter))

            # determine coefficient points
            ret, smallContourAreas, contourImage = ImageProcess.processFindContours(erodeImage, minArea=minArea, maxArea=maxArea)
            smallContoursNum = len(smallContourAreas)

            # determine the begin and the end point for calculating pixel to mm
            beginSmallContour = smallContourAreas[0]
            endSmallContour = smallContourAreas[0]
            for smallContour in smallContourAreas:
                if smallContour[0] < beginSmallContour[0]:
                    beginSmallContour = smallContour
                if smallContour[0] > endSmallContour[0]:
                    endSmallContour = smallContour
            beginCenter = (int((beginSmallContour[0] + beginSmallContour[2]) / 2),
                           int((beginSmallContour[1] + beginSmallContour[3]) / 2))
            endCenter = (
            int((endSmallContour[0] + endSmallContour[2]) / 2), int((endSmallContour[1] + endSmallContour[3]) / 2))

            print("begin {}".format(beginCenter))
            print("end {}".format(endCenter))
            if len(sourceImage.shape) < 3:
                drawImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_GRAY2BGR)
            else:
                drawImage = sourceImage.copy()

            pixelDistance = ImageProcess.calculateDistanceBy2Points(beginCenter, endCenter)
            print("pixel distance: {}".format(pixelDistance))

            eachPointDistance = 15
            mmDistance = eachPointDistance * (smallContoursNum - 1)
            print("mm distance: {}".format(mmDistance))

            coefficient = mmDistance / pixelDistance
            print("Coefficient: {}".format(coefficient))
        else:
            maxArea = _maxArea
            minArea = _minArea
            # determine offset point
            ret, bigContours, contourImage = ImageProcess.processFindContours(erodeImage, minArea=maxArea,
                                                                 maxArea=int(
                                                                     erodeImage.shape[0] * erodeImage.shape[1] / 2),
                                                                 maxWidth=erodeImage.shape[1] / 3 * 2,
                                                                 maxHeight=erodeImage.shape[0] / 3 * 2)
            offsetContour = bigContours[0]
            offsetCenter = (
            int((offsetContour[0] + offsetContour[2]) / 2), int((offsetContour[1] + offsetContour[3]) / 2))
            print("offset center {}".format(offsetCenter))

        return (coefficient, beginCenter, endCenter), offsetCenter, (minArea, maxArea)

    def setOffset(self, robotPos):
        robotPosX = robotPos[0]
        robotPosY = robotPos[1]
        self.offsetXEntry.delete(0, END)
        self.offsetYEntry.delete(0, END)

        self.offsetXEntry.insert(0, "{}".format(robotPosX - self.cameraPos[0]))
        self.offsetYEntry.insert(0, "{}".format(robotPosY - self.cameraPos[1]))

    def clickBtnSelectCASType(self):
        cas_select_window = CASTypeSelectWindow(self.mainWindow)
        cas_select_window.wait_window()
        if cas_select_window.isChanged:
            self.robot_coordinates_type.setValue(cas_select_window.cas_type.value)

    def showCurrentASParam(self):
        current_as_param: AS_Parameter = self.mainWindow.as_manager.getCurrentAS()
        if current_as_param is None:
            messagebox.showwarning("Axis System", "Please create a new Axis system")
            return
        self.nameEntry.delete(0, END)
        self.nameEntry.insert(0, current_as_param.name)
        self.as_type_comb.set(self.current_as_type)

        if self.current_as_type == AS_Type.on_robot_hand.value:
            self.robot_coordinates_type.setValue(current_as_param.casType)
            self.mm_moving_Scale.setValue(current_as_param.robot_mm_moving_Scale)
            self.exceptDelta.setValue(current_as_param.exceptDelta)
            self.delayTime.setValue(current_as_param.delayTakepicTime)
            self.rotate.setStringValue(current_as_param.rotate)

            self.pixel_mm_Scale.setValue(current_as_param.robot_pixel_mm_Scale)

            self.offsetXEntry.delete(0, END)
            self.offsetXEntry.insert(0, current_as_param.robotOffset[0])

            self.offsetYEntry.delete(0, END)
            self.offsetYEntry.insert(0, current_as_param.robotOffset[1])

            self.preProcess_algorithm.setStringValue(current_as_param.preProcess_algorithm)
        elif self.current_as_type == AS_Type.fixed_camera.value:
            self.image_point1.setValue(current_as_param.image_point_1)
            self.image_point2.setValue(current_as_param.image_point_2)
            self.image_point3.setValue(current_as_param.image_point_3)

            self.robot_point1.setValue(current_as_param.robot_point_1)
            self.robot_point2.setValue(current_as_param.robot_point_2)
            self.robot_point3.setValue(current_as_param.robot_point_3)

            self.getImagePointAlgorithm.setStringValue(current_as_param.getPointsAlgorithm)

    def save(self, notification=True):
        try:
            current_as_param: AS_Parameter = self.mainWindow.as_manager.getCurrentAS()
            current_as_param.name = self.nameEntry.get()
            current_as_param.as_type = self.as_type_comb.get()

            if current_as_param.as_type == AS_Type.on_robot_hand.value:
                current_as_param.casType = self.robot_coordinates_type.getValue()
                current_as_param.delayTakepicTime = self.delayTime.getIntValue()
                current_as_param.exceptDelta = self.exceptDelta.getIntValue()
                current_as_param.robot_mm_moving_Scale = self.mm_moving_Scale.getFloatValue()
                current_as_param.rotate = self.rotate.getValue()
                current_as_param.robot_pixel_mm_Scale = self.pixel_mm_Scale.getFloatValue()
                current_as_param.robotOffset = (float(self.offsetXEntry.get()), float(self.offsetYEntry.get()))
                current_as_param.preProcess_algorithm = self.preProcess_algorithm.getValue()

            else:
                current_as_param.image_point_1 = self.image_point1.getIntValue()
                current_as_param.image_point_2 = self.image_point2.getIntValue()
                current_as_param.image_point_3 = self.image_point3.getIntValue()

                current_as_param.robot_point_1 = self.robot_point1.getIntValue()
                current_as_param.robot_point_2 = self.robot_point2.getIntValue()
                current_as_param.robot_point_3 = self.robot_point3.getIntValue()
                current_as_param.getPointsAlgorithm = self.getImagePointAlgorithm.getValue()
                current_as_param.transform_matrix = self.get_as_matrix()


            self.mainWindow.as_manager.save()
            self.mainWindow.as_manager.changeCurrentAS(current_as_param.name)
            self.asNameList = self.mainWindow.as_manager.getNameList()
            self.asComboBox.config(value=self.asNameList)
            if notification:
                messagebox.showinfo("Save Axis system information", "Save the Axis system information successfully!")
            return True
        except Exception as error:
            text = "ERROR Save Axis System parameter. Detail: {}".format(error)
            self.mainWindow.runningTab.insertLog(text)

            if notification:
                messagebox.showwarning("Save Axis System parameter", "Cannot save the Axis System parameter.\nDetail: {}".format(error))

            return False

    def get_as_matrix(self):
        return ImageProcess.getAffineTransFormMatrix((self.robot_point1.getIntValue(), self.robot_point2.getIntValue(), self.robot_point3.getIntValue()),
                                                     (self.image_point1.getIntValue(), self.image_point2.getIntValue(), self.image_point3.getIntValue()))


    def isChanged(self):
        ret = False
        current_as_param: AS_Parameter = self.mainWindow.as_manager.getCurrentAS()
        ret = ret or current_as_param.name != self.nameEntry.get()

        if self.current_as_type == AS_Type.on_robot_hand.value:
            ret = ret or current_as_param.casType != self.robot_coordinates_type.getValue()
            ret = ret or current_as_param.robot_mm_moving_Scale != self.mm_moving_Scale.getFloatValue()
            ret = ret or current_as_param.exceptDelta != self.exceptDelta.getIntValue()
            ret = ret or current_as_param.rotate != self.rotate.getValue()
            ret = ret or current_as_param.delayTakepicTime != self.delayTime.getIntValue()
            ret = ret or current_as_param.robot_pixel_mm_Scale != self.pixel_mm_Scale.getFloatValue()
            ret = ret or current_as_param.robotOffset != (float(self.offsetXEntry.get()), float(self.offsetYEntry.get()))
            ret = ret or current_as_param.preProcess_algorithm != self.preProcess_algorithm.getValue()
            return ret
        elif self.current_as_type == AS_Type.fixed_camera.value:
            ret = ret or current_as_param.image_point_1 != self.image_point1.getIntValue()
            ret = ret or current_as_param.image_point_2 != self.image_point2.getIntValue()
            ret = ret or current_as_param.image_point_3 != self.image_point3.getIntValue()
            ret = ret or current_as_param.robot_point_1 != self.robot_point1.getIntValue()
            ret = ret or current_as_param.robot_point_2 != self.robot_point2.getIntValue()
            ret = ret or current_as_param.robot_point_3 != self.robot_point3.getIntValue()
            ret = ret or current_as_param.getPointsAlgorithm != self.getImagePointAlgorithm.getValue()
            return ret


    def setupBtnAddNew(self):
        self.btnASAddNew = AddButton(self, command=self.clickBtnAddNew)
        self.btnASAddNew.place(relx=0.02, rely=0.92, relwidth=0.225, relheight=0.05)

    def setupDuplicateButton(self):
        self.btnDuplicate = CopyButton(self, command=self.duplicateAS)
        self.btnDuplicate.place(relx=0.265, rely=0.92, relwidth=0.225, relheight=0.05)

    def setupBtnDelete(self):
        self.btnAS_Delete = DeleteButton(self, command=self.clickBtnDelete)
        self.btnAS_Delete.place(relx=0.510, rely=0.92, relwidth=0.225, relheight=0.05)

    def setupBtnSave(self):
        self.btnAS_Save = SaveButton(self, command=self.clickBtnSave)
        self.btnAS_Save.place(relx=0.755, rely=0.92, relwidth=0.225, relheight=0.05)

    def clickBtnDelete(self):
        confirm = messagebox.askyesno("Delete algorithm", "Are you sure that want delete this algorithm?")
        if confirm:
            self.mainWindow.algorithmManager.deleteCurrentAlgorithm()

    def duplicateAS(self):
        if not self.save():
            return
        try:
            current_as_param: AS_Parameter = self.mainWindow.as_manager.getCurrentAS()
            new_as_parameter = copy.deepcopy(current_as_param)
            new_name = current_as_param.name + "_Copy"
            index = 1
            while self.mainWindow.as_manager.as_name_existed(new_name):
                new_name = current_as_param.name + "_Copy_{}".format(index)
                index += 1

            new_as_parameter.name = new_name

            self.mainWindow.as_manager.addAxisSystem(new_as=new_as_parameter)

        except Exception as error:
            text = "ERROR Cannot add a new Axis System. Detail: {}".format(error)
            messagebox.showerror("Duplicate Axis System", text)

    def clickBtnSave(self):
        if self.mainWindow.as_manager.currentName != self.nameEntry.get() and \
                self.mainWindow.as_manager.as_name_existed(self.nameEntry.get()):
            askChange = messagebox.askyesno("Axis System Name",
                                            "The AS name \"{}\" is existed, Do you want to change another name?\nyes = stay and change\nno = move without saving".format(
                                                self.nameEntry.get()))
            if askChange:
                self.asComboBox.current(self.mainWindow.as_manager.getCurrentPos())
                return
        else:
            self.save()
            self.asComboBox.current(self.mainWindow.as_manager.getCurrentPos())

    def clickBtnAddNew(self):
        newAlgorithmView = NewAxisSystemWindow(self.mainWindow)
        newAlgorithmView.wait_window()
        self.updateParameterForNewList()

    def updateParameterForNewList(self):
        try:
            self.asNameList = self.mainWindow.as_manager.getNameList()
            self.asComboBox.config(value=self.asNameList)
            self.asComboBox.current(self.mainWindow.as_manager.getCurrentPos())
            self.show_parameter_frame()
            self.showCurrentASParam()
        except Exception as error:
            text = "ERROR Update Axis System parameter. Detail: {}".format(error)
            self.mainWindow.runningTab.insertLog(text)

            messagebox.showwarning("Update axis system parameter", "Cannot show the current AS parameter!\nDetail: {}".format(error))

    def updateAlgorithmList(self):
        algorithmList = [algorithm.algorithmParameter.name for algorithm in self.mainWindow.algorithmManager.algorithmList]

        if self.current_as_type == AS_Type.fixed_camera.value:
            self.getImagePointAlgorithm.updateValueList(algorithmList)
        elif self.current_as_type == AS_Type.on_robot_hand.value:
            self.preProcess_algorithm.updateValueList(algorithmList)