from Modules.ModelSetting.ModelParameter import ModelParameter
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from View.Common.VisionUI import *
class DemoLocationDetectSettingFrame(VisionLabelFrame):

    yDistance = 35
    xDistance = 150

    demo_location_detect_algorithm: ComboForFlexibleValue

    def __init__(self, master, text=""):
        from View.ModelSetting.ModelSettingTab import ModelSettingTab
        VisionLabelFrame.__init__(self, master, text=text)
        self.modelSettingTab: ModelSettingTab = master
        self.parameter = ModelParameter()
        self.setupView()

    def updateValue(self, parameter: ModelParameter):
        # Rear check missing
        self.parameter = parameter
        self.demo_location_detect_algorithm.setStringValue(parameter.demo_location_algorithm)

    def save(self, model: ModelParameter):
        model.demo_location_algorithm = self.demo_location_detect_algorithm.getValue()
        return model

    def isChanged(self, model: ModelParameter):
        return model.demo_location_algorithm != self.demo_location_detect_algorithm.getValue()

    def setupView(self):
        distanceY = 0.07
        algorithmList = []
        for algorithm in self.modelSettingTab.mainWindow.algorithmManager.algorithmList:
            algorithmList.append(algorithm.algorithmParameter.name)

        self.demo_location_detect_algorithm = ComboForFlexibleValue(self, "Algorithm:", yPos=5,
                                                                    height=self.yDistance, valueList=algorithmList)

    def updateAlgorithmList(self):
        algorithmList = []
        for algorithm in self.modelSettingTab.mainWindow.algorithmManager.algorithmList:
            algorithmList.append(algorithm.algorithmParameter.name)

        self.demo_location_detect_algorithm.updateValueList(algorithmList)