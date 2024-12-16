from View.Common.VisionUI import *
from Modules.ModelSetting.ModelParameter import ModelParameter
from View.Common.CommonStepFrame import *
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from Modules.ModelSetting.AdjustValueFrame import AdjustValueFrame
from tkinter import messagebox
from ImageProcess import ImageProcess
import cv2 as cv
from CommonAssit import TimeControl



class Counting_In_Conveyor_Setting(VisionLabelFrame):
    find_object_algorithm: ComboForFlexibleValue
    yDistance = 35
    xDistance = 150

    in_boundary: InputParamFrame
    counting_boundary: InputParamFrame
    out_boundary: InputParamFrame
    max_disappeared: InputParamFrame
    max_distance: InputParamFrame
    bip_input: InputParamFrame

    def __init__(self, master, mainWindow):
        self.mainWindow = mainWindow
        VisionLabelFrame.__init__(self,master=master, text="Counting in conveyor model setting")
        self.setupView()

    def setupView(self):
        algorithmList = [algorithm.algorithmParameter.name for algorithm in self.mainWindow.algorithmManager.algorithmList]
        self.find_object_algorithm = ComboForFlexibleValue(self, "Finding object algorithm :", yPos=0 * self.yDistance + 5,
                                                           height=self.yDistance, valueList=algorithmList)

        self.in_boundary = InputParamFrame(self, "In Boundary: ", 1 * self.yDistance + 5,
                                                 self.yDistance)
        self.counting_boundary = InputParamFrame(self, "Counting Boundary: ", 2 * self.yDistance + 5,
                                                 self.yDistance)
        self.out_boundary = InputParamFrame(self, "Out Boundary: ", 3 * self.yDistance + 5,
                                                 self.yDistance)

        self.max_disappeared = InputParamFrame(self, "Max Disappeared: ", 4 * self.yDistance + 5,
                                                 self.yDistance)
        self.max_distance = InputParamFrame(self, "Max Distance: ", 5 * self.yDistance + 5,
                                                 self.yDistance)

        self.bip_input = InputParamFrame(self, "BIP : ", 6 * self.yDistance + 5,
                                                 self.yDistance)


    def save(self, parameter: ModelParameter):
        parameter.cic_find_object_algorithm = self.find_object_algorithm.getValue()
        parameter.cic_in_boundary = self.in_boundary.getIntValue()
        parameter.cic_out_boundary = self.out_boundary.getIntValue()
        parameter.cic_counting_boundary = self.counting_boundary.getIntValue()
        parameter.cic_max_disappeared = self.max_disappeared.getIntValue()
        parameter.cic_bip = self.bip_input.getIntValue()
        parameter.cic_max_distance = self.max_distance.getIntValue()
        return parameter

    def isChanged(self, parameter: ModelParameter):
        ret = parameter.cic_find_object_algorithm != self.find_object_algorithm.getValue()
        ret = ret or parameter.cic_in_boundary != self.in_boundary.getIntValue()
        ret = ret or parameter.cic_out_boundary != self.out_boundary.getIntValue()
        ret = ret or parameter.cic_counting_boundary != self.counting_boundary.getIntValue()
        ret = ret or parameter.cic_max_disappeared != self.max_disappeared.getIntValue()
        ret = ret or parameter.cic_bip != self.bip_input.getIntValue()
        ret = ret or parameter.cic_max_distance != self.max_distance.getIntValue()
        return ret

    def updateValue(self, parameter: ModelParameter):
        self.find_object_algorithm.setStringValue(parameter.cic_find_object_algorithm)
        self.in_boundary.setValue(parameter.cic_in_boundary)
        self.out_boundary.setValue(parameter.cic_out_boundary)
        self.counting_boundary.setValue(parameter.cic_counting_boundary)
        self.max_disappeared.setValue(parameter.cic_max_disappeared)
        self.bip_input.setValue(parameter.cic_bip)
        self.max_distance.setValue(parameter.cic_max_distance)

    def testModel(self):
        if self.mainWindow.originalImage is None:
            messagebox.showwarning("Source Image", "Please take the image first!")
        else:
            sourceImage = self.mainWindow.originalImage.copy()

            self.mainWindow.workingThread.create_counting_in_conveyor()
            self.mainWindow.workingThread.counting_in_conveyor.updateModel()
            self.mainWindow.workingThread.counting_in_conveyor.count_coconut_thread(sourceImage)

    def updateAlgorithmList(self):
        algorithmList = [algorithm.algorithmParameter.name for algorithm in self.mainWindow.algorithmManager.algorithmList]
        self.find_object_algorithm.updateValueList(algorithmList)
