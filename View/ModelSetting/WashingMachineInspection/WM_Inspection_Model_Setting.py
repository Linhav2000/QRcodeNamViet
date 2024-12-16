from Modules.ModelSetting.ModelParameter import ModelParameter
from View.Common.CommonStepFrame import InputParamFrame
from View.Common.VisionUI import *
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from tkinter import filedialog
from CommonAssit import PathFileControl
from CommonAssit import TimeControl
import cv2 as cv
from View.Common.CommonStepFrame import *

class WM_Inspection_Model_Setting(VisionLabelFrame):

    yDistance = 35
    xDistance = 150
    origin_algorithm: ComboForFlexibleValue
    use_hardware_trigger: CheckboxStepParamFrame
    camera_1: ComboForFlexibleValue

    def __init__(self, master, text=""):
        from View.ModelSetting.ModelSettingTab import ModelSettingTab
        VisionLabelFrame.__init__(self, master, text=text)
        self.modelSettingTab: ModelSettingTab = master
        self.mainWindow = self.modelSettingTab.mainWindow
        self.parameter = ModelParameter()
        self.setupView()

    def updateValue(self, parameter: ModelParameter):
        self.parameter = parameter
        self.origin_algorithm.setStringValue(parameter.ddk_origin_algorithm)
        self.use_hardware_trigger.setValue(parameter.wmi_use_hardware_trigger)
        self.camera_1.setPosValue(parameter.wmi_camera_1_id)

    def save(self, parameter: ModelParameter):
        parameter.ddk_origin_algorithm = self.origin_algorithm.getValue()
        parameter.wmi_use_hardware_trigger = self.use_hardware_trigger.getValue()
        parameter.wmi_camera_1_id = self.camera_1.getPosValue()
        return parameter

    def isChanged(self, parameter: ModelParameter):
        ret = parameter.ddk_origin_algorithm != self.origin_algorithm.getValue()
        ret = ret or parameter.wmi_use_hardware_trigger != self.use_hardware_trigger.getValue()
        ret = ret or parameter.wmi_camera_1_id != self.camera_1.getPosValue()
        return ret

    def updateAlgorithmList(self):
        algorithmList = []
        for algorithm in self.modelSettingTab.mainWindow.algorithmManager.algorithmList:
            algorithmList.append(algorithm.algorithmParameter.name)

        self.origin_algorithm.updateValueList(algorithmList)


    def setupView(self):
        self.use_hardware_trigger = CheckboxStepParamFrame(self, "Use hardware trigger: ",
                                                           yPos=0 * self.yDistance + 5, height= self.yDistance)

        algorithmList = [algorithm.algorithmParameter.name for algorithm in
                         self.mainWindow.algorithmManager.algorithmList]
        self.origin_algorithm = ComboForFlexibleValue(self, "Origin Algorithm: ", yPos=1 * self.yDistance + 5,
                                                      height=self.yDistance, valueList=algorithmList)

        camera_name_list = []
        for i in range(10):
            camera_name_list.append(f"Camera {i}")

        self.camera_1 = ComboForFlexibleValue(self, "Camera 1:", yPos=2 * self.yDistance + 5,
                                                       height=self.yDistance, valueList=camera_name_list)