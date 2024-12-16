from View.Common.VisionUI import *
from Modules.ModelSetting.ModelParameter import ModelParameter
from View.Common.CommonStepFrame import *
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from Modules.ModelSetting.AdjustValueFrame import AdjustValueFrame
from tkinter import messagebox
from ImageProcess import ImageProcess
import cv2 as cv

class E_Map_Model_Setting(VisionLabelFrame):

    startXInput: AdjustValueFrame
    startYInput: AdjustValueFrame

    model_code: InputParamFrame

    rowInput: InputParamFrame
    columnInput: InputParamFrame

    distanceX: InputParamFrame
    distanceY: InputParamFrame

    sizeRectX: AdjustValueFrame
    sizeRectY: AdjustValueFrame


    ng_find_algorithm: ComboForFlexibleValue
    code_reading_algorithm: ComboForFlexibleValue

    ng_finding_camera: ComboForFlexibleValue
    code_reading_camera: ComboForFlexibleValue

    yDistance = 35
    xDistance = 150



    def __init__(self, master, mainWindow):
        self.mainWindow = mainWindow
        VisionLabelFrame.__init__(self,master=master, text="EMAP model setting")
        self.setupView()

    def setupView(self):
        self.model_code = InputParamFrame(self, "Model code : ", yPos=0*self.yDistance + 5, height=self.yDistance, width=200)

        self.rowInput = InputParamFrame(self, "Row : ", yPos=1*self.yDistance + 5, height=self.yDistance)
        self.columnInput = InputParamFrame(self, "Column : ", yPos=2*self.yDistance + 5, height=self.yDistance)
        self.distanceX = InputParamFrame(self, "Distance X: ", yPos=3*self.yDistance + 5, height=self.yDistance)
        self.distanceY = InputParamFrame(self, "Distance Y: ", yPos=4*self.yDistance + 5, height=self.yDistance)

        labelStartPoint = VisionLabel(self, text="Start point: ")
        labelStartPoint.place(x=5, y=5 * self.yDistance + 5, height=self.yDistance)

        self.startXInput = AdjustValueFrame(self, maxVal=10000)
        self.startXInput.place(x=152, y=5 * self.yDistance + 5, width=70, height=25)

        self.startYInput = AdjustValueFrame(self, maxVal=10000)
        self.startYInput.place(x=262, y=5 * self.yDistance + 5, width=70, height=25)

        labelSize = VisionLabel(self, text="Rect Size :")
        labelSize.place(x=5, y=6 * self.yDistance + 5, height=self.yDistance)

        self.sizeRectX = AdjustValueFrame(self, maxVal=10000)
        self.sizeRectX.place(x=152, y=6 * self.yDistance + 5, width=70, height=25)

        self.sizeRectY = AdjustValueFrame(self, maxVal=10000)
        self.sizeRectY.place(x=262, y=6 * self.yDistance + 5, width=70, height=25)

        algorithmList = [algorithm.algorithmParameter.name for algorithm in self.mainWindow.algorithmManager.algorithmList]
        self.ng_find_algorithm = ComboForFlexibleValue(self, "NG finding algorithm :", yPos=7 * self.yDistance + 5,
                                                        height=self.yDistance, valueList=algorithmList)

        self.code_reading_algorithm = ComboForFlexibleValue(self, "Code reading algorithm :", yPos=8 * self.yDistance + 5,
                                                       height=self.yDistance, valueList=algorithmList)
        camera_name_list = []
        for i in range(10):
            camera_name_list.append(f"Camera {i}")

        self.ng_finding_camera = ComboForFlexibleValue(self, "NG finding Camera :", yPos=9 * self.yDistance + 5,
                                                       height=self.yDistance, valueList=camera_name_list)


        self.code_reading_camera = ComboForFlexibleValue(self, "Code reading Camera :", yPos=10 * self.yDistance + 5,
                                                       height=self.yDistance, valueList=camera_name_list)


    def save(self, parameter: ModelParameter):
        parameter.emap_rows = self.rowInput.getIntValue()
        parameter.emap_cols = self.columnInput.getIntValue()
        parameter.emap_start_point = (self.startXInput.getValue(), self.startYInput.getValue())
        parameter.emap_size_rect = (self.sizeRectX.getValue(), self.sizeRectY.getValue())
        parameter.emap_distanceX = self.distanceX.getIntValue()
        parameter.emap_distanceY = self.distanceY.getIntValue()
        parameter.emap_ng_finding_algorithm = self.ng_find_algorithm.getValue()
        parameter.emap_code_reading_algorithm = self.code_reading_algorithm.getValue()
        parameter.emap_model_code = self.model_code.getValue()
        parameter.emap_ng_finding_camera_id = self.ng_finding_camera.getPosValue()
        parameter.emap_code_reading_camera_id = self.code_reading_camera.getPosValue()
        return parameter

    def isChanged(self, model: ModelParameter):
        ret = model.emap_rows != self.rowInput.getIntValue()
        ret = ret or model.emap_cols != self.columnInput.getIntValue()
        ret = ret or model.emap_start_point != (self.startXInput.getValue(), self.startYInput.getValue())
        ret = ret or model.emap_size_rect != (self.sizeRectX.getValue(), self.sizeRectY.getValue())
        ret = ret or model.emap_distanceX != self.distanceX.getIntValue()
        ret = ret or model.emap_distanceY != self.distanceY.getIntValue()
        ret = ret or model.emap_ng_finding_algorithm != self.ng_find_algorithm.getValue()
        ret = ret or model.emap_code_reading_algorithm != self.code_reading_algorithm.getValue()
        ret = ret or model.emap_model_code != self.model_code.getValue()
        ret = ret or model.emap_code_reading_camera_id != self.code_reading_camera.getPosValue()
        ret = ret or model.emap_ng_finding_camera_id != self.ng_finding_camera.getPosValue()

        return ret

    def updateValue(self, parameter: ModelParameter):
        self.rowInput.setValue(parameter.emap_rows)
        self.columnInput.setValue(parameter.emap_cols)
        self.distanceX.setValue(parameter.emap_distanceX)
        self.distanceY.setValue(parameter.emap_distanceY)
        self.startXInput.setValue(parameter.emap_start_point[0])
        self.startYInput.setValue(parameter.emap_start_point[1])
        self.sizeRectX.setValue(parameter.emap_size_rect[0])
        self.sizeRectY.setValue(parameter.emap_size_rect[1])
        self.ng_find_algorithm.setStringValue(parameter.emap_ng_finding_algorithm)
        self.code_reading_algorithm.setStringValue(parameter.emap_code_reading_algorithm)
        self.model_code.setValue(parameter.emap_model_code)
        self.ng_finding_camera.setPosValue(parameter.emap_ng_finding_camera_id)
        self.code_reading_camera.setPosValue(parameter.emap_code_reading_camera_id)

    def testDraw(self):
        sourceImage = self.mainWindow.originalImage.copy()
        if sourceImage is None:
            messagebox.showwarning("Image None", "Please choose the image for testing draw")
            return

        if len(sourceImage.shape) < 3:
            sourceImage = ImageProcess.processCvtColor(sourceImage, cv.COLOR_GRAY2BGR)

        emap_rows = self.rowInput.getIntValue()
        emap_cols = self.columnInput.getIntValue()
        emap_start_point = (self.startXInput.getValue(), self.startYInput.getValue())
        emap_size_rect = (self.sizeRectX.getValue(), self.sizeRectY.getValue())
        emap_distanceX = self.distanceX.getIntValue()
        emap_distanceY = self.distanceY.getIntValue()

        for column in range(emap_cols):
            for row in range(emap_rows):
                point1 = (emap_start_point[0] + emap_distanceX * column, emap_start_point[1] + emap_distanceY * row)
                point2 = (point1[0] + emap_size_rect[0], point1[1] + emap_size_rect[1])
                cv.rectangle(sourceImage,pt1=point1,pt2=point2,color=(0, 255, 255),thickness=3,lineType=cv.LINE_AA )


        self.mainWindow.showImage(sourceImage)


    def updateAlgorithmList(self):
        algorithmList = [algorithm.algorithmParameter.name for algorithm in self.mainWindow.algorithmManager.algorithmList]
        self.ng_find_algorithm.updateValueList(algorithmList)
        self.code_reading_algorithm.updateValueList(algorithmList)