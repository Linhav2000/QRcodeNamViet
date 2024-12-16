from Modules.ModelSetting.ModelParameter import ModelParameter
import numpy as np
import cv2 as cv
from tkinter import messagebox
from ImageProcess.Algorithm.Algorithm import Algorithm
from CommonAssit import TimeControl

class THCP_Checking:
    currentModel: ModelParameter = None
    resultMatrix = None
    ng_find_algorithm: Algorithm = None

    countingThresh = 1
    oldValue = 0
    currentValue = 0
    tempValue = 0
    tempTime = 0
    tempTimeThresh = 1000

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow

    def updateModel(self):
        self.currentModel = self.mainWindow.modelSettingTab.modelManager.getCurrentModel()
        self.ng_find_algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName(self.currentModel.thcp_ng_finding_algorithm)
        self.mainWindow.workingThread.cameraManager.currentCamera.connect()
        self.countingThresh = self.currentModel.thcp_rows * self.currentModel.thcp_cols

    def checkReady(self):
        self.updateModel()
        if not self.mainWindow.workingThread.cameraManager.currentCamera.ready:
            messagebox.showerror("Camera connection", "Please check the camera connection!")
        if self.ng_find_algorithm is None:
            messagebox.showerror("Algorithm setting", "Please choose NG algorithm for model!")
        ret = self.mainWindow.workingThread.cameraManager.currentCamera.ready and self.ng_find_algorithm is not None
        return ret

    def do_process(self, sourceImage=None):
        if sourceImage is None:
            ret, sourceImage = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture(False)
            if not ret:
                return False

        value = self.counting(sourceImage)
        if value == self.tempValue:
            if self.checkTime():
                self.currentValue = self.tempValue
        else:
            self.tempTime = TimeControl.time()
            self.tempValue = value

        self.mainWindow.stateLabel.config(text=f"Count ={self.oldValue}")

        if self.currentValue == self.oldValue:
            return True
        else:
            if self.currentValue == 0:
                if self.oldValue < self.countingThresh:
                    self.oldValue = self.currentValue
                    return False
                else:
                    self.oldValue = self.currentValue
                    return True
            else:
                self.oldValue = self.currentValue
                return True

    def counting(self, sourceImage):
        if sourceImage is None:
            messagebox.showerror("Empty Image", "The source image is Empty!")
            self.mainWindow.runningTab.insertLog("ERROR The source image is empty!")
            return 0
        count = 0
        self.resultMatrix = np.zeros((self.currentModel.thcp_rows, self.currentModel.thcp_cols),dtype=np.int8)
        for row in range(self.currentModel.thcp_rows):
            for column in range(self.currentModel.thcp_cols):
                passed = True
                point1 = (self.currentModel.thcp_start_point[0] + self.currentModel.thcp_distanceX * column,
                          self.currentModel.thcp_start_point[1] + self.currentModel.thcp_distanceY * row)
                point2 = (point1[0] + self.currentModel.thcp_size_rect[0],
                          point1[1] + self.currentModel.thcp_size_rect[1])

                roi_process = sourceImage[point1[1]: point2[1], point1[0]: point2[0]]
                ret, resultList, text = self.ng_find_algorithm.executeAlgorithm(image=roi_process)
                if ret:
                    # cv.rectangle(sourceImage, pt1=point1, pt2=point2, color=(0, 255, 0), thickness=5,
                    #              lineType=cv.LINE_AA)

                    for result in resultList:
                        if not result.passed:
                            self.resultMatrix[row][column] = 1
                            # cv.rectangle(sourceImage,pt1=point1, pt2=point2, color=(0, 0, 255), thickness=5, lineType=cv.LINE_AA)
                            passed = False
                            break

                if passed:
                    count += 1

                else:
                    self.resultMatrix[row][column] = 1
                # cv.rectangle(sourceImage, pt1=point1, pt2=point2, color=(0, 255, 255), thickness=3, lineType=cv.LINE_AA)

        print(count)
        self.mainWindow.showImage(sourceImage)
        return count

    def checkTime(self):
        currentTime = TimeControl.time()
        if currentTime - self.tempTime > self.tempTimeThresh:
            return True
        else:
            return False
