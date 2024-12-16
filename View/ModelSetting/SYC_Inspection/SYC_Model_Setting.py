from Modules.ModelSetting.ModelParameter import ModelParameter
from View.Common.VisionUI import *
from Modules.ModelSetting.Algorithm_Choose import Algorithm_Choose
from View.Common.CommonStepFrame import *


class SYC_Model_Setting(VisionLabelFrame):

    yDistance = 35
    xDistance = 150
    save_NG_image: SaveImageOption
    save_OK_image: SaveImageOption
    hardware_trigger_mode: CheckboxStepParamFrame
    algorithm_list = []

    def __init__(self, master, text=""):
        from View.ModelSetting.ModelSettingTab import ModelSettingTab
        VisionLabelFrame.__init__(self, master, text=text)
        self.modelSettingTab: ModelSettingTab = master
        self.mainWindow = self.modelSettingTab.mainWindow
        self.parameter = ModelParameter()
        self.setupView()

    def updateValue(self, parameter: ModelParameter):
        self.parameter = parameter
        self.save_NG_image.setValue(parameter.syc_save_NG_image)
        self.save_OK_image.setValue(parameter.syc_save_OK_image)
        self.hardware_trigger_mode.setValue(parameter.syc_hardware_trigger)
        for algorithm, save_algorithm in zip(self.algorithm_list, parameter.syc_algorithm_list):
            algorithm.setStringValue(save_algorithm)
            algorithm.model_name = self.parameter.name

    def save(self, parameter: ModelParameter):
        parameter.syc_save_NG_image = self.save_NG_image.getValue()
        parameter.syc_save_OK_image = self.save_OK_image.getValue()
        parameter.syc_hardware_trigger = self.hardware_trigger_mode.getValue()
        algorithm_list = []
        for algorithm in self.algorithm_list:
            algorithm_list.append(algorithm.getValue())
        parameter.syc_algorithm_list = algorithm_list
        self.parameter = parameter
        return parameter

    def isChanged(self, parameter: ModelParameter):
        ret = False
        ret = ret or parameter.syc_save_NG_image != self.save_NG_image.getValue()
        ret = ret or parameter.syc_save_OK_image != self.save_OK_image.getValue()
        ret = ret or parameter.syc_hardware_trigger != self.hardware_trigger_mode.getValue()

        for algorithm, save_algorithm in zip(self.algorithm_list, parameter.syc_algorithm_list):
            ret = ret or algorithm.getValue() != save_algorithm
        return ret

    def updateAlgorithmList(self):
        algorithmList = [algorithm.algorithmParameter.name for algorithm in self.mainWindow.algorithmManager.algorithmList]
        for algorithm in self.algorithm_list:
            algorithm.updateValueList(algorithmList)


    def setupView(self):
        self.algorithm_list = []
        algorithmList = [algorithm.algorithmParameter.name for algorithm in
                         self.mainWindow.algorithmManager.algorithmList]

        for i in range(5):
            self.algorithm_list.append(Algorithm_Choose(self, f"Algorithm {i + 1}", yPos=i * self.yDistance + 5,
                                                        height=self.yDistance, valueList=algorithmList,
                                                        mainWindow=self.mainWindow, combo_width=135,
                                                        add_new_done_cmd=self.updateAlgorithmList))
        self.save_OK_image = SaveImageOption(self, text="Save OK Image: ", yPos=5* self.yDistance + 5, height=self.yDistance)
        self.save_NG_image = SaveImageOption(self, text="Save NG Image: ", yPos=6 * self.yDistance + 5,height=self.yDistance)
        self.hardware_trigger_mode = CheckboxStepParamFrame(self, "Hardware trigger: ", yPos=5 + 7*self.yDistance, height=self.yDistance)
