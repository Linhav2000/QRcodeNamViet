from Modules.ModelSetting.ModelParameter import ModelParameter
from View.Common.CommonStepFrame import InputParamFrame
from View.Common.VisionUI import *


class HikBarcodeDemoSetting(VisionLabelFrame):

    yDistance = 35
    xDistance = 150

    def __init__(self, master, text=""):
        from View.ModelSetting.ModelSettingTab import ModelSettingTab
        VisionLabelFrame.__init__(self, master, text=text)
        self.modelSettingTab: ModelSettingTab = master
        self.mainWindow = self.modelSettingTab.mainWindow
        self.parameter = ModelParameter()
        self.setupView()

    def updateValue(self, parameter: ModelParameter):
        self.parameter = parameter

    def save(self, model: ModelParameter):
        return model

    def isChanged(self, model: ModelParameter):
        ret = False
        return ret

    def setupView(self):
        #
        # self.numContourThresh = InputParamFrame(self, "Number Contours Thresh: ",
        #                                         6 * self.yDistance + 5, self.yDistance)
        return