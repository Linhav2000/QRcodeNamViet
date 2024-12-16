from Modules.ModelSetting.ModelParameter import ModelParameter
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from View.Common.VisionUI import *
class RearCheckMissingFrame(VisionLabelFrame):

    yDistance = 35
    xDistance = 150

    leftCameraCmb: ComboForFlexibleValue
    rightCameraCmb: ComboForFlexibleValue
    leftAlgorithm: ComboForFlexibleValue
    rightAlgorithm: ComboForFlexibleValue


    def __init__(self, master, text=""):
        from View.ModelSetting.ModelSettingTab import ModelSettingTab
        VisionLabelFrame.__init__(self, master, text=text)
        self.modelSettingTab: ModelSettingTab = master
        self.parameter = ModelParameter()
        self.setupView()

    def updateValue(self, parameter: ModelParameter):
        # Rear check missing
        self.parameter = parameter
        self.leftCameraCmb.setPosValue(parameter.leftCameraId)
        self.rightCameraCmb.setPosValue(parameter.rightCameraId)
        self.leftAlgorithm.setStringValue(parameter.leftAlgorithm)
        self.rightAlgorithm.setStringValue(parameter.rightAlgorithm)

    def save(self, model: ModelParameter):
        model.leftCameraId = self.leftCameraCmb.getPosValue()
        model.rightCameraId = self.rightCameraCmb.getPosValue()
        model.leftAlgorithm = self.leftAlgorithm.getValue()
        model.rightAlgorithm = self.rightAlgorithm.getValue()

        print(self.modelSettingTab.currentModelParameter.leftCameraId)
        return model

    def isChanged(self, model: ModelParameter):
        return (model.leftCameraId != self.leftCameraCmb.getPosValue()) \
                or (model.rightCameraId != self.rightCameraCmb.getPosValue()) \
                or (model.leftAlgorithm != self.leftAlgorithm.getValue()) \
                or (model.rightAlgorithm != self.rightAlgorithm.getValue())

    def setupView(self):
        distanceY = 0.07
        cameraList = []
        for i in range(10):
            cameraList.append("Camera {}".format(i))

        algorithmList = []
        for algorithm in self.modelSettingTab.mainWindow.algorithmManager.algorithmList:
            algorithmList.append(algorithm.algorithmParameter.name)

        self.leftCameraCmb = ComboForFlexibleValue(self, "Left Camera: ", yPos=5,
                                                   height=self.yDistance, valueList=cameraList)
        self.rightCameraCmb = ComboForFlexibleValue(self, "Right Camera: ", self.yDistance,
                                                    self.yDistance, cameraList)

        self.leftAlgorithm = ComboForFlexibleValue(self, "Left algorithm:", 2 * self.yDistance,
                                                   self.yDistance, algorithmList)
        self.rightAlgorithm = ComboForFlexibleValue(self, "Right algorithm:", 3 * self.yDistance,
                                                    self.yDistance, algorithmList)

    def updateAlgorithmList(self):
        algorithmList = []
        for algorithm in self.modelSettingTab.mainWindow.algorithmManager.algorithmList:
            algorithmList.append(algorithm.algorithmParameter.name)

        self.leftAlgorithm.updateValueList(algorithmList)
        self.rightAlgorithm.updateValueList(algorithmList)