from Modules.ModelSetting.ModelParameter import ModelParameter
from View.Common.VisionUI import *
from View.Common.CommonStepFrame import *
from Modules.ModelSetting.DDK_Algorithm_Choose import DDK_Algorithm_Choose
from View.Common.ScrollFrame import ScrollView


class DDK_Inspection_Model_Setting(VisionLabelFrame):

    yDistance = 35
    xDistance = 150
    scrollView: ScrollView
    algorithm_list = []
    save_ok_image: SaveImageOption
    save_ng_image: SaveImageOption
    num_of_step: InputParamFrame
    def __init__(self, master, text=""):
        from View.ModelSetting.ModelSettingTab import ModelSettingTab
        VisionLabelFrame.__init__(self, master, text=text)
        self.modelSettingTab: ModelSettingTab = master
        self.mainWindow = self.modelSettingTab.mainWindow
        self.parameter = ModelParameter()
        self.setupView()

    def updateValue(self, parameter: ModelParameter):
        self.parameter = parameter
        for algorithm, save_algorithm in zip(self.algorithm_list, parameter.ddk_algorithm_list):
            algorithm.setStringValue(save_algorithm)
            algorithm.model_name = self.parameter.name
        self.save_ok_image.setValue(parameter.save_ok_image)
        self.save_ng_image.setValue(parameter.save_ng_image)
        self.num_of_step.setValue(parameter.ddk_num_of_step)

    def save(self, parameter: ModelParameter):
        algorithm_list = []

        for algorithm in self.algorithm_list:
            algorithm_list.append(algorithm.getValue())
        parameter.ddk_algorithm_list = algorithm_list
        parameter.save_ok_image = self.save_ok_image.getValue()
        parameter.save_ng_image = self.save_ng_image.getValue()
        parameter.ddk_num_of_step = self.num_of_step.getIntValue()
        self.parameter = parameter
        return parameter

    def isChanged(self, parameter: ModelParameter):
        ret = False
        for algorithm, save_algorithm in zip(self.algorithm_list, parameter.ddk_algorithm_list):
            ret = ret or algorithm.getValue() != save_algorithm
        ret = ret or self.save_ok_image.getValue() != parameter.save_ok_image
        ret = ret or self.save_ng_image.getValue() != parameter.save_ng_image
        ret = ret or self.num_of_step.getIntValue() != parameter.ddk_num_of_step
        return ret

    def updateAlgorithmList(self):
        algorithmList = []
        for algorithm in self.modelSettingTab.mainWindow.algorithmManager.algorithmList:
            algorithmList.append(algorithm.algorithmParameter.name)
        for algorithm_ in self.algorithm_list:
            algorithm_.updateValueList(algorithmList)
        # self.origin_algorithm.updateValueList(algorithmList)


    def setupView(self):
        self.algorithm_list = []
        algorithmList = [algorithm.algorithmParameter.name for algorithm in
                         self.mainWindow.algorithmManager.algorithmList]

        self.scrollView = ScrollView(self, displayHeight=1000, borderwidth=0)
        self.scrollView.place(relx=0, rely=0.01, relwidth=1, relheight=0.98)
        for i in range(20):
            self.algorithm_list.append(DDK_Algorithm_Choose(self.scrollView.display, f"Step {i + 1}", yPos=i * self.yDistance + 5,
                                                            step=i+1,
                                                            height=self.yDistance, valueList=algorithmList,
                                                            mainWindow=self.mainWindow,
                                                            add_new_done_cmd=self.updateAlgorithmList))

        self.save_ok_image = SaveImageOption(self.scrollView.display, text="Save OK Image: ", yPos=20 * self.yDistance + 5, height=self.yDistance)
        self.save_ng_image = SaveImageOption(self.scrollView.display, text="Save NG Image: ", yPos=21 * self.yDistance + 5,height=self.yDistance)
        self.num_of_step = InputParamFrame(self.scrollView.display, "Num of step: ", yPos=22 * self.yDistance + 5, height=self.yDistance)

