from Modules.ModelSetting.ModelParameter import ModelParameter
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from View.Common.VisionUI import *
class LocationDetectSettingFrame(VisionLabelFrame):

    yDistance = 35
    xDistance = 150

    detectLocationAlgorithm: ComboForFlexibleValue

    def __init__(self, master, text=""):
        from View.ModelSetting.ModelSettingTab import ModelSettingTab
        VisionLabelFrame.__init__(self, master, text=text)
        self.modelSettingTab: ModelSettingTab = master
        self.parameter = ModelParameter()
        self.setupView()

    def updateValue(self, parameter: ModelParameter):
        # Rear check missing
        self.parameter = parameter
        self.detectLocationAlgorithm.setStringValue(parameter.detectLocationAlgorithm)

    def save(self, model: ModelParameter):
        model.detectLocationAlgorithm = self.detectLocationAlgorithm.getValue()
        return model

    def isChanged(self, model: ModelParameter):
        return model.detectLocationAlgorithm != self.detectLocationAlgorithm.getValue()

    def setupView(self):
        distanceY = 0.07
        algorithmList = []
        for algorithm in self.modelSettingTab.mainWindow.algorithmManager.algorithmList:
            algorithmList.append(algorithm.algorithmParameter.name)

        self.detectLocationAlgorithm = ComboForFlexibleValue(self, "Algorithm:",yPos=5,
                                                                height=self.yDistance, valueList=algorithmList)

    def updateAlgorithmList(self):
        algorithmList = []
        for algorithm in self.modelSettingTab.mainWindow.algorithmManager.algorithmList:
            algorithmList.append(algorithm.algorithmParameter.name)

        self.detectLocationAlgorithm.updateValueList(algorithmList)