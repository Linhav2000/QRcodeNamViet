from Modules.ModelSetting.ModelParameter import ModelParameter
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from Modules.ModelSetting.DisplayParamFrame import DisplayParamFrame
from View.Common.CommonStepFrame import CheckboxStepParamFrame
from View.ModelSetting.RoboWeighingRobot.CASTypeSelectWindow import CASTypeSelectWindow
from Modules.ModelSetting.CAS_Type import CAS_Type
from View.Common.CommonStepFrame import InputParamFrame
from View.Common.VisionUI import *
from ImageProcess import ImageProcess

class RotoWeighingSettingModelFrame(VisionLabelFrame):

    yDistance = 35
    xDistance = 150

    rotoAlgorithmStep0: ComboForFlexibleValue
    rotoAlgorithmStep1: ComboForFlexibleValue
    multiPoint: CheckboxStepParamFrame
    robot_coordinates_type: DisplayParamFrame
    btnSelectRobotCASType: VisionButton
    pixel_mm_Scale_1: InputParamFrame
    mm_moving_Scale: InputParamFrame
    delayTime: InputParamFrame
    mode_detect: ComboForFlexibleValue
    exceptDelta: InputParamFrame
    btnGetScale1: VisionButton
    offsetLabel_1: VisionLabel
    offsetXEntry_1: VisionEntry
    offsetYEntry_1: VisionEntry
    btnGetOffset_1: VisionButton
    getOffsetFlag = False
    caliOffsetFlag = False
    btnGetScale2: VisionButton
    offsetLabel_2: VisionLabel
    offsetXEntry_2: VisionEntry
    offsetYEntry_2: VisionEntry
    btnGetOffset_2: VisionButton
    multiPoint:CheckboxStepParamFrame
    mode_detect : ComboForFlexibleValue
    delayTime:InputParamFrame

    offsetCenter = (0, 0)
    beginCenter = (0, 0)
    endCenter = (0, 0)

    cameraPos_Sys1 = [0, 0]
    workingPos_Sys1 = [0, 0]

    cameraPos_Sys2 = [0, 0]
    workingPos_Sys2 = [0, 0]

    minArea = 0
    maxArea = 0

    isCalibratingSystem1 = False
    isCalibratingSystem2 = False

    def __init__(self, master, mainWindow, text=""):
        from View.ModelSetting.ModelSettingTab import ModelSettingTab
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow
        VisionLabelFrame.__init__(self, master, text=text)

        self.modelSettingTab: ModelSettingTab = master
        self.parameter = ModelParameter()
        self.setupView()
        self.notifyRegister()
    def notifyRegister(self):
        self.mainWindow.notificationCenter.add_observer(with_block=self.changeLanguage, for_name="ChangeLanguage")

    def changeLanguage(self, sender, notification_name, info):
        self.config(text=self.mainWindow.languageManager.localized("roto WR"))
        self.rotoAlgorithmStep0.updateLabelLanguage(self.mainWindow.languageManager.localized("algorithm step 0"))
        self.rotoAlgorithmStep1.updateLabelLanguage(self.mainWindow.languageManager.localized("algorithm step 1"))
        self.multiPoint.updateCheckboxLanguage(self.mainWindow.languageManager.localized("multi point"))
        self.mode_detect.updateLabelLanguage(self.mainWindow.languageManager.localized("check type"))
        self.delayTime.update_Language(new_text =self.mainWindow.languageManager.localized("delay time"))

    def updateValue(self, parameter: ModelParameter):
        # Rear check missing
        self.parameter = parameter
        self.rotoAlgorithmStep0.setStringValue(parameter.rotoAlgorithmStep0)
        self.rotoAlgorithmStep1.setStringValue(parameter.rotoAlgorithmStep1)
        self.mode_detect.setStringValue(parameter.roto_weighing_detect_mode)
        self.multiPoint.setValue(parameter.rw_multiPoint)
        self.delayTime.setValue(parameter.delayTakepicTime)

    def save(self, model: ModelParameter):
        model.rotoAlgorithmStep0 = self.rotoAlgorithmStep0.getValue()
        model.rotoAlgorithmStep1 = self.rotoAlgorithmStep1.getValue()
        model.rw_multiPoint = self.multiPoint.getValue()
        model.roto_weighing_detect_mode = self.mode_detect.getValue()
        model.delayTakepicTime = self.delayTime.getIntValue()
        return model

    def isChanged(self, model: ModelParameter):
        ret = model.rotoAlgorithmStep0 != self.rotoAlgorithmStep0.getValue()
        ret = ret or model.rotoAlgorithmStep1 != self.rotoAlgorithmStep1.getValue()
        ret = ret or model.rw_multiPoint != self.multiPoint.getValue()
        ret = ret or model.delayTakepicTime != self.delayTime.getIntValue()
        return ret

    def setupView(self):
        distanceY = 0.07
        algorithmList = []
        for algorithm in self.modelSettingTab.mainWindow.algorithmManager.algorithmList:
            algorithmList.append(algorithm.algorithmParameter.name)

        self.rotoAlgorithmStep0 = ComboForFlexibleValue(self, self.mainWindow.languageManager.localized("algorithm step 0"), yPos=5,
                                                        height=self.yDistance, valueList=algorithmList)
        self.rotoAlgorithmStep1 = ComboForFlexibleValue(self, self.mainWindow.languageManager.localized("algorithm step 1"), yPos=5 + self.yDistance,
                                                        height=self.yDistance, valueList=algorithmList)

        # self.multiPoint = CheckboxStepParamFrame(self,self.mainWindow.languageManager.localized("multi point"), yPos=5 + 2*self.yDistance, height=self.yDistance)
        self.multiPoint = CheckboxStepParamFrame(self,self.mainWindow.languageManager.localized("multi point"), yPos=5 + 2*self.yDistance, height=self.yDistance)


        mode_detect_list = ["Tìm tâm", "Kiểm tra tai"]
        self.mode_detect = ComboForFlexibleValue(self,self.mainWindow.languageManager.localized("check type"), yPos=5 + 3*self.yDistance,
                                                        height=self.yDistance, valueList=mode_detect_list)

        self.delayTime = InputParamFrame(self,self.mainWindow.languageManager.localized("delay time"),
                                         yPos=5 + 4 * self.yDistance, height=self.yDistance, width=100)



    def updateAlgorithmList(self):
        algorithmList = []
        for algorithm in self.modelSettingTab.mainWindow.algorithmManager.algorithmList:
            algorithmList.append(algorithm.algorithmParameter.name)

        self.rotoAlgorithmStep0.updateValueList(algorithmList)
        self.rotoAlgorithmStep1.updateValueList(algorithmList)