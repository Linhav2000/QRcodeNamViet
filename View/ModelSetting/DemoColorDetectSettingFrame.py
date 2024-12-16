from Modules.ModelSetting.ModelParameter import ModelParameter
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from View.Common.VisionUI import *
class DemoColorDetectSettingFrame(VisionLabelFrame):

    yDistance = 35
    xDistance = 150

    colorDetectAlgorithm: ComboForFlexibleValue

    def __init__(self, master, text=""):
        from View.ModelSetting.ModelSettingTab import ModelSettingTab
        VisionLabelFrame.__init__(self, master, text=text)
        self.modelSettingTab: ModelSettingTab = master
        self.parameter = ModelParameter()
        self.setupView()

    def updateValue(self, parameter: ModelParameter):
        # Rear check missing
        self.parameter = parameter
        self.colorDetectAlgorithm.setStringValue(parameter.demo_color_detect_algorithm)

    def save(self, model: ModelParameter):
        model.demo_color_detect_algorithm = self.colorDetectAlgorithm.getValue()
        return model

    def isChanged(self, model: ModelParameter):
        return model.demo_color_detect_algorithm != self.colorDetectAlgorithm.getValue()

    def setupView(self):
        distanceY = 0.07
        algorithmList = []
        for algorithm in self.modelSettingTab.mainWindow.algorithmManager.algorithmList:
            algorithmList.append(algorithm.algorithmParameter.name)

        self.colorDetectAlgorithm = ComboForFlexibleValue(self, "Algorithm:", yPos=5,
                                                          height=self.yDistance, valueList=algorithmList)

    def updateAlgorithmList(self):
        algorithmList = []
        for algorithm in self.modelSettingTab.mainWindow.algorithmManager.algorithmList:
            algorithmList.append(algorithm.algorithmParameter.name)

        self.colorDetectAlgorithm.updateValueList(algorithmList)