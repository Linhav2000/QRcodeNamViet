from View.Common.VisionUI import *
from Modules.ModelSetting.ModelParameter import ModelParameter
from View.Common.CommonStepFrame import *
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from Modules.ModelSetting.AdjustValueFrame import AdjustValueFrame
from tkinter import messagebox
from ImageProcess import ImageProcess
import cv2 as cv

class THCP_Model_Setting(VisionLabelFrame):

    startXInput: AdjustValueFrame
    startYInput: AdjustValueFrame

    rowInput: InputParamFrame
    columnInput: InputParamFrame

    distanceX: InputParamFrame
    distanceY: InputParamFrame

    sizeRectX: AdjustValueFrame
    sizeRectY: AdjustValueFrame


    ng_find_algorithm: ComboForFlexibleValue

    yDistance = 35
    xDistance = 150



    def __init__(self, master, mainWindow):
        self.mainWindow = mainWindow
        VisionLabelFrame.__init__(self,master=master, text="Housing connector packing model setting")
        self.setupView()

    def setupView(self):
        self.rowInput = InputParamFrame(self, "Row : ", yPos=0*self.yDistance + 5, height=self.yDistance)
        self.columnInput = InputParamFrame(self, "Column : ", yPos=1*self.yDistance + 5, height=self.yDistance)
        self.distanceX = InputParamFrame(self, "Distance X: ", yPos=2*self.yDistance + 5, height=self.yDistance)
        self.distanceY = InputParamFrame(self, "Distance Y: ", yPos=3*self.yDistance + 5, height=self.yDistance)

        labelStartPoint = VisionLabel(self, text="Start point: ")
        labelStartPoint.place(x=5, y=4 * self.yDistance + 5, height=self.yDistance)

        self.startXInput = AdjustValueFrame(self, maxVal=10000)
        self.startXInput.place(x=152, y=4 * self.yDistance + 5, width=70, height=25)

        self.startYInput = AdjustValueFrame(self, maxVal=10000)
        self.startYInput.place(x=262, y=4 * self.yDistance + 5, width=70, height=25)

        labelSize = VisionLabel(self, text="Rect Size :")
        labelSize.place(x=5, y=5 * self.yDistance + 5, height=self.yDistance)

        self.sizeRectX = AdjustValueFrame(self, maxVal=10000)
        self.sizeRectX.place(x=152, y=5 * self.yDistance + 5, width=70, height=25)

        self.sizeRectY = AdjustValueFrame(self, maxVal=10000)
        self.sizeRectY.place(x=262, y=5 * self.yDistance + 5, width=70, height=25)

        algorithmList = [algorithm.algorithmParameter.name for algorithm in self.mainWindow.algorithmManager.algorithmList]
        self.ng_find_algorithm = ComboForFlexibleValue(self, "NG find algorithm :", yPos=6 * self.yDistance + 5,
                                                        height=self.yDistance, valueList=algorithmList)

    def save(self, parameter: ModelParameter):
        parameter.thcp_rows = self.rowInput.getIntValue()
        parameter.thcp_cols = self.columnInput.getIntValue()
        parameter.thcp_start_point = (self.startXInput.getValue(), self.startYInput.getValue())
        parameter.thcp_size_rect = (self.sizeRectX.getValue(), self.sizeRectY.getValue())
        parameter.thcp_distanceX = self.distanceX.getIntValue()
        parameter.thcp_distanceY = self.distanceY.getIntValue()
        parameter.thcp_ng_finding_algorithm = self.ng_find_algorithm.getValue()
        return parameter

    def isChanged(self, model: ModelParameter):
        ret = model.thcp_rows != self.rowInput.getIntValue()
        ret = ret or model.thcp_cols != self.columnInput.getIntValue()
        ret = ret or model.thcp_start_point != (self.startXInput.getValue(), self.startYInput.getValue())
        ret = ret or model.thcp_size_rect != (self.sizeRectX.getValue(), self.sizeRectY.getValue())
        ret = ret or model.thcp_distanceX != self.distanceX.getIntValue()
        ret = ret or model.thcp_distanceY != self.distanceY.getIntValue()
        ret = ret or model.thcp_ng_finding_algorithm != self.ng_find_algorithm.getValue()
        return ret

    def updateValue(self, parameter: ModelParameter):
        self.rowInput.setValue(parameter.thcp_rows)
        self.columnInput.setValue(parameter.thcp_cols)
        self.distanceX.setValue(parameter.thcp_distanceX)
        self.distanceY.setValue(parameter.thcp_distanceY)
        self.startXInput.setValue(parameter.thcp_start_point[0])
        self.startYInput.setValue(parameter.thcp_start_point[1])
        self.sizeRectX.setValue(parameter.thcp_size_rect[0])
        self.sizeRectY.setValue(parameter.thcp_size_rect[1])
        self.ng_find_algorithm.setStringValue(parameter.thcp_ng_finding_algorithm)

    def testDraw(self):
        sourceImage = self.mainWindow.originalImage.copy()
        if sourceImage is None:
            messagebox.showwarning("Image None", "Please choose the image for testing draw")
            return

        if len(sourceImage.shape) < 3:
            sourceImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_GRAY2BGR)
        self.master.save(False)
        self.mainWindow.workingThread.create_thcp_checking()
        self.mainWindow.showStateLabel()
        self.mainWindow.workingThread.thcp_checking.updateModel()
        count = self.mainWindow.workingThread.thcp_checking.counting(sourceImage=sourceImage.copy())

        thcp_rows = self.rowInput.getIntValue()
        thcp_cols = self.columnInput.getIntValue()
        thcp_start_point = (self.startXInput.getValue(), self.startYInput.getValue())
        thcp_size_rect = (self.sizeRectX.getValue(), self.sizeRectY.getValue())
        thcp_distanceX = self.distanceX.getIntValue()
        thcp_distanceY = self.distanceY.getIntValue()

        for column in range(thcp_cols):
            for row in range(thcp_rows):
                point1 = (thcp_start_point[0] + thcp_distanceX * column, thcp_start_point[1] + thcp_distanceY * row)
                point2 = (point1[0] + thcp_size_rect[0], point1[1] + thcp_size_rect[1])
                cv.rectangle(sourceImage,pt1=point1,pt2=point2,color=(0, 255, 255),thickness=3,lineType=cv.LINE_AA )


        self.mainWindow.showImage(sourceImage)
        self.mainWindow.stateLabel.config(text=f"Count = {count}")


    def updateAlgorithmList(self):
        algorithmList = [algorithm.algorithmParameter.name for algorithm in self.mainWindow.algorithmManager.algorithmList]
        self.ng_find_algorithm.updateValueList(algorithmList)