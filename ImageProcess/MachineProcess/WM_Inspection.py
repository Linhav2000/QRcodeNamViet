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

class WM_Inspection:
    currentModel: ModelParameter = None
    camera_1: Camera = None
    data_dir = "./data/WashingMachineInspection"

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def updateModel(self):
        self.currentModel = self.mainWindow.modelSettingTab.modelManager.getCurrentModel()
        self.camera_1 = self.mainWindow.workingThread.cameraManager.cameraList[self.currentModel.wmi_camera_1_id]

    def checkReady(self):
        self.updateModel()
        ret = True
        if not self.camera_1.connect():
            messagebox.showerror("Camera connection", "Please check the CAMERA 1 connection!")
            ret = False
        if not self.currentModel.wmi_use_hardware_trigger:
            if not self.mainWindow.workingThread.connectionManager.isReady():
                ret = self.mainWindow.workingThread.connectionManager.connect()
        else:
            self.hardware_trigger()
        return ret

    def do_process(self):
        if not self.currentModel.wmi_use_hardware_trigger:
            self.software_trigger()

    def software_trigger(self):
        PathFileControl.generatePath("./data")
        PathFileControl.generatePath(self.data_dir)
        image_path = f"{self.data_dir}/{TimeControl.time()}.bmp"

        ret, image = self.camera_1.takePicture()
        if ret:
            self.mainWindow.showImage(image, original=True)
            cv.imencode(".bmp", self.mainWindow.originalImage)[1].tofile(image_path)
            # cv.imwrite(filename=image_path, img=self.mainWindow.originalImage)
        else:
            self.mainWindow.runningTab.insertLog("ERROR Cannot take image. Please check camera")

    def hardware_trigger(self):
        self.camera_1.baslerHardwareTrigger(process_cmd=self.save_image)

    def save_image(self, image):
        PathFileControl.generatePath("./data")
        PathFileControl.generatePath(self.data_dir)
        image_path = f"{self.data_dir}/{TimeControl.time()}.bmp"
        self.mainWindow.showImage(image, original=True)
        # cv.imwrite(filename=image_path, img=self.mainWindow.originalImage)
        cv.imencode(".bmp", self.mainWindow.originalImage)[1].tofile(image_path)
