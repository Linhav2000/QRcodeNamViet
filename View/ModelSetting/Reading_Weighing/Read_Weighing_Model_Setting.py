from Modules.ModelSetting.ModelParameter import ModelParameter
from View.Common.CommonStepFrame import *
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from Modules.ModelSetting.AdjustValueFrame import AdjustValueFrame
from tkinter import messagebox
from ImageProcess import ImageProcess
from ImageProcess.Algorithm.Algorithm import Algorithm
from ImageProcess.Algorithm.MethodList import MethodList
import cv2 as cv


class Read_Weighing_Model_Setting(VisionLabelFrame):
    yDistance = 35
    xDistance = 150

    centerX: AdjustValueFrame
    centerY: AdjustValueFrame
    startX: AdjustValueFrame
    startY: AdjustValueFrame
    endX: AdjustValueFrame
    endY: AdjustValueFrame
    startValue: InputParamFrame
    endValue: InputParamFrame
    find_finger_algorithm: ComboForFlexibleValue


    def __init__(self, master, mainWindow):
        self.mainWindow = mainWindow
        VisionLabelFrame.__init__(self,master=master, text="Read weighing model setting")
        self.setupView()

    def setupView(self):
        labelCenter = VisionLabel(self, text="Center :")
        labelCenter.place(x=5, y= 0 * self.yDistance + 5, height=self.yDistance)

        self.centerX = AdjustValueFrame(self, maxVal=1000000)
        self.centerX.place(x=152, y=0 * self.yDistance + 5, width=70, height=25)

        self.centerY = AdjustValueFrame(self, maxVal=1000000)
        self.centerY.place(x=262, y=0 * self.yDistance + 5, width=70, height=25)

        labelStartPoint = VisionLabel(self, text="Start point :")
        labelStartPoint.place(x=5, y=1 * self.yDistance + 5, height=self.yDistance)

        self.startX = AdjustValueFrame(self, maxVal=1000000)
        self.startX.place(x=152, y=1 * self.yDistance + 5, width=70, height=25)

        self.startY = AdjustValueFrame(self, maxVal=1000000)
        self.startY.place(x=262, y=1 * self.yDistance + 5, width=70, height=25)

        labelEndPoint = VisionLabel(self, text="End point :")
        labelEndPoint.place(x=5, y=2 * self.yDistance + 5, height=self.yDistance)

        self.endX = AdjustValueFrame(self, maxVal=1000000)
        self.endX.place(x=152, y=2 * self.yDistance + 5, width=70, height=25)

        self.endY = AdjustValueFrame(self, maxVal=1000000)
        self.endY.place(x=262, y=2 * self.yDistance + 5, width=70, height=25)


        self.startValue = InputParamFrame(self, "Start Value : ", yPos=3*self.yDistance + 5, height=self.yDistance)
        self.endValue = InputParamFrame(self, "End Value : ", yPos=4*self.yDistance + 5, height=self.yDistance)

        algorithmList = [algorithm.algorithmParameter.name for algorithm in
                         self.mainWindow.algorithmManager.algorithmList]
        self.find_finger_algorithm = ComboForFlexibleValue(self, "Finger Finding Algorithm: ", yPos=6 * self.yDistance + 5,
                                                       height=self.yDistance, valueList=algorithmList)

    def save(self, parameter: ModelParameter):
        parameter.rw_center = (self.centerX.getValue(), self.centerY.getValue())
        parameter.rw_start_point = (self.startX.getValue(), self.startY.getValue())
        parameter.rw_end_point = (self.endX.getValue(), self.endY.getValue())
        parameter.rw_start_value = self.startValue.getFloatValue()
        parameter.rw_end_value = self.endValue.getFloatValue()
        parameter.rw_finger_finding_algorithm = self.find_finger_algorithm.getValue()
        return parameter

    def isChanged(self, model: ModelParameter):
        ret = False
        ret = ret or model.rw_center != (self.centerX.getValue(), self.centerY.getValue())
        ret = ret or model.rw_start_point != (self.startX.getValue(), self.startY.getValue())
        ret = ret or model.rw_end_point != (self.endX.getValue(), self.endY.getValue())
        ret = ret or model.rw_start_value != self.startValue.getFloatValue()
        ret = ret or model.rw_end_value != self.endValue.getFloatValue()
        ret = ret or model.rw_finger_finding_algorithm != self.find_finger_algorithm.getValue()
        return ret

    def updateValue(self, parameter: ModelParameter):
        self.centerX.setValue(parameter.rw_center[0])
        self.centerY.setValue(parameter.rw_center[1])

        self.startX.setValue(parameter.rw_start_point[0])
        self.startY.setValue(parameter.rw_start_point[1])

        self.endX.setValue(parameter.rw_end_point[0])
        self.endY.setValue(parameter.rw_end_point[1])

        self.startValue.setValue(parameter.rw_start_value)
        self.endValue.setValue(parameter.rw_end_value)

        self.find_finger_algorithm.setStringValue(parameter.rw_finger_finding_algorithm)

    def testDraw(self):
        self.mainWindow.showStateLabel()
        sourceImage = self.mainWindow.originalImage.copy()
        if sourceImage is None:
            messagebox.showerror("Source image", "Please take image first!")
            return
        self.master.save(False)
        self.mainWindow.workingThread.create_reading_weighing()
        self.mainWindow.workingThread.read_weighing.updateModel()
        self.mainWindow.workingThread.read_weighing.do_process(sourceImage)
        return
        currentAlgorithm: Algorithm = self.mainWindow.algorithmManager.getCurrentAlgorithm()
        ret, resultList, text = currentAlgorithm.executeAlgorithm(sourceImage)
        real_point = (0, 0)
        if   ret:
            for result in resultList:
                if result.methodName == MethodList.findContour.value:
                    real_point = result.pointList[0]
        rw_center = (self.centerX.getValue(), self.centerY.getValue())
        rw_start_point = (self.startX.getValue(), self.startY.getValue())
        rw_end_point = (self.endX.getValue(), self.endY.getValue())
        rw_start_value = self.startValue.getFloatValue()
        rw_end_value = self.endValue.getFloatValue()
        cv.line(sourceImage, pt1=rw_center, pt2=real_point, color=(0, 255, 0),thickness=9, lineType=cv.LINE_AA)
        cv.line(sourceImage, pt1=rw_center, pt2=rw_start_point, color=(0, 0, 255),thickness=5, lineType=cv.LINE_AA)
        cv.line(sourceImage, pt1=rw_center, pt2=rw_end_point, color=(0, 0, 255),thickness=5, lineType=cv.LINE_AA)
        # cv.line(sourceImage, pt1=rw_center, pt2=rw_end_point, color=(0, 255, 0),thickness=3, lineType=cv.LINE_AA)

        # angle = ImageProcess.angleFrom2Vec((rw_center[0] - rw_end_point[0], rw_center[0] - rw_end_point[0]),
        #                                    (rw_center[0]-rw_start_point[0], rw_center[1]-rw_start_point[1]))

        angle_end_start = ImageProcess.findAngleByLine((rw_center, rw_start_point), (rw_center, rw_end_point))
        angle_start_current = ImageProcess.findAngleByLine((rw_center, rw_start_point), (rw_center, real_point))
        angle_current_end = ImageProcess.findAngleByLine((rw_center, real_point), (rw_center, rw_end_point))
        angle_2_value = (rw_end_value - rw_start_value) / (360 + angle_end_start)

        if angle_start_current < 0:
            angle_start_current = 360 + angle_start_current

        print(f"angle start end:  = {angle_end_start}")
        print(f"angle start current:  = {angle_start_current}")
        print(f"angle current end:  = {angle_current_end}")
        print(f"angle_2_value = {angle_2_value}")



        self.mainWindow.stateLabel.config(text=f"Value = {round(angle_2_value * angle_start_current, 2)}")
        self.mainWindow.showImage(sourceImage)

    def updateAlgorithmList(self):
        algorithmList = [algorithm.algorithmParameter.name for algorithm in self.mainWindow.algorithmManager.algorithmList]
        self.find_finger_algorithm.updateValueList(algorithmList)