from Modules.ModelSetting.ModelParameter import ModelParameter
import numpy as np
import cv2 as cv
from tkinter import messagebox
from ImageProcess.Algorithm.Algorithm import Algorithm
from Connection.Camera import Camera
from ImageProcess.Algorithm.MethodList import MethodList
from CommonAssit import TimeControl
from CommonAssit import PathFileControl
from CommonAssit.FileManager import *
from ImageProcess import ImageProcess

class Reading_Weighing:
    currentModel: ModelParameter = None
    finger_finding_algorithm: Algorithm = None


    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def updateModel(self):
        self.currentModel = self.mainWindow.modelSettingTab.modelManager.getCurrentModel()
        self.finger_finding_algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName(self.currentModel.rw_finger_finding_algorithm)

    def checkReady(self):
        self.updateModel()
        ret = True
        if self.finger_finding_algorithm is None:
            messagebox.showerror("Algorithm setting", "Please choose find finger algorithm for model!")

        if not self.mainWindow.workingThread.cameraManager.currentCamera.connect():
            messagebox.showerror("Camera connection", "Please check the CODE READING CAMERA connection!")
            ret = False
        return ret

    def do_process(self, sourceImage=None):
        if sourceImage is None:
            ret, sourceImage = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
            if not ret:
                messagebox.showerror("Camera connection", "Please check the camera connection!")
                self.mainWindow.runningTab.insertLog("ERROR Cannot take picture from camera!")
                return
        self.mainWindow.showStateLabel()
        if sourceImage is None:
            messagebox.showerror("Source image", "Please take image first!")
            return

        ret, resultList, text = self.finger_finding_algorithm.executeAlgorithm(sourceImage)
        real_point = (0, 0)
        if ret:
            for result in resultList:
                if result.methodName == MethodList.findContour.value:
                    real_point = (result.pointList[0][0] + result.basePoint[0] + result.workingArea[0],
                                  result.pointList[0][1] + result.basePoint[1] + result.workingArea[1])
        # rw_center = (self.cucenterX.getValue(), self.centerY.getValue())
        # rw_start_point = (self.startX.getValue(), self.startY.getValue())
        # rw_end_point = (self.endX.getValue(), self.endY.getValue())
        # rw_start_value = self.startValue.getFloatValue()
        # rw_end_value = self.endValue.getFloatValue()
        cv.line(sourceImage, pt1=self.currentModel.rw_center, pt2=real_point,
                color=(0, 255, 0), thickness=9, lineType=cv.LINE_AA)
        cv.line(sourceImage, pt1=self.currentModel.rw_center, pt2=self.currentModel.rw_start_point,
                color=(0, 0, 255), thickness=5, lineType=cv.LINE_AA)
        cv.line(sourceImage, pt1=self.currentModel.rw_center, pt2=self.currentModel.rw_end_point,
                color=(0, 0, 255), thickness=5, lineType=cv.LINE_AA)
        # cv.line(sourceImage, pt1=rw_center, pt2=rw_end_point, color=(0, 255, 0),thickness=3, lineType=cv.LINE_AA)

        # angle = ImageProcess.angleFrom2Vec((rw_center[0] - rw_end_point[0], rw_center[0] - rw_end_point[0]),
        #                                    (rw_center[0]-rw_start_point[0], rw_center[1]-rw_start_point[1]))

        angle_end_start = ImageProcess.findAngleByLine((self.currentModel.rw_center, self.currentModel.rw_start_point),
                                                       (self.currentModel.rw_center, self.currentModel.rw_end_point))
        angle_start_current = ImageProcess.findAngleByLine((self.currentModel.rw_center, self.currentModel.rw_start_point),
                                                           (self.currentModel.rw_center, real_point))
        angle_current_end = ImageProcess.findAngleByLine((self.currentModel.rw_center, real_point),
                                                         (self.currentModel.rw_center, self.currentModel.rw_end_point))
        angle_2_value = (self.currentModel.rw_end_value - self.currentModel.rw_start_value) / (360 + angle_end_start)

        if angle_start_current < 0:
            angle_start_current = 360 + angle_start_current

        print(f"angle start end:  = {angle_end_start}")
        print(f"angle start current:  = {angle_start_current}")
        print(f"angle current end:  = {angle_current_end}")
        print(f"angle_2_value = {angle_2_value}")

        self.mainWindow.stateLabel.config(text=f"Value = {round(angle_2_value * angle_start_current, 2)}")
        self.mainWindow.showImage(sourceImage)