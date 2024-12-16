from tkinter import messagebox
from Modules.ModelSetting.ModelParameter import ModelParameter
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from View.Common.VisionUI import *

class VisionForFuAssyWindow(VisionTopLevel):

    yDistance = 35
    xDistance = 150

    ruCameraCmb: ComboForFlexibleValue
    fuCameraCmb: ComboForFlexibleValue
    ruAlgorithmCmb: ComboForFlexibleValue
    fuAlgorithmCmb: ComboForFlexibleValue
    ruLightCmb: ComboForFlexibleValue
    fuLightCmb: ComboForFlexibleValue

    ruCameraId = 0
    fuCameraId = 0
    ruAlgorithm = ""
    fuAlgorithm = ""
    saveFlag = False

    def __init__(self, mainWindow, parameter):
        VisionTopLevel.__init__(self)
        self.mainWindow = mainWindow
        self.parameter: ModelParameter = parameter
        self.setupWindow()
        self.setupView()
        self.showLastSetting()

    def setupWindow(self):
        width = 436
        height = 333
        self.title("Vision Setting")
        self.iconbitmap('./resource/appIcon.ico')
        self.geometry("{}x{}+{}+{}".format(width, height,
                                           int(self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width() / 2 - width / 2),
                                           int(self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height() / 2 - height / 2)))
        self.resizable(0, 0)
        self.grab_set()

    def setupView(self):
        self.setupButton()

        distanceY = 0.07
        cameraList = []
        for i in range(10):
            cameraList.append("Camera {}".format(i))

        algorithmList = []
        for algorithm in self.mainWindow.algorithmManager.algorithmList:
            algorithmList.append(algorithm.algorithmParameter.name)

        lightList = []
        for i in range(16):
            lightList.append("Light {}".format(i))

        self.ruCameraCmb = ComboForFlexibleValue(self, "RU Camera: ", yPos=5,
                                                 height=self.yDistance, valueList=cameraList)
        self.fuCameraCmb = ComboForFlexibleValue(self, "FU Camera: ", self.yDistance,
                                                 self.yDistance, cameraList)

        self.ruAlgorithmCmb = ComboForFlexibleValue(self, "RU algorithm:", 2 * self.yDistance,
                                                    self.yDistance, algorithmList)
        self.fuAlgorithmCmb = ComboForFlexibleValue(self, "FU algorithm:", 3 * self.yDistance,
                                                    self.yDistance, algorithmList)

        self.ruLightCmb = ComboForFlexibleValue(self, "RU Light:", 4*self.yDistance, self.yDistance, lightList)
        self.fuLightCmb = ComboForFlexibleValue(self, "FU Light:", 5*self.yDistance, self.yDistance, lightList)


    def setupButton(self):
        self.btnSave = SaveButton(self, command=self.clickBtnSave)
        self.btnSave.place(relx = 0.2, rely = 0.8, width=120, height=40)

        self.btnCancel = CancelButton(self, command=self.clickBtnCancel)
        self.btnCancel.place(relx=0.6, rely=0.8, width=120, height=40)

    def clickBtnSave(self):
        try:
            self.parameter.ruCameraId = self.ruCameraCmb.getPosValue()
            self.parameter.fuCameraId = self.fuCameraCmb.getPosValue()
            self.parameter.ruAlgorithm = self.ruAlgorithmCmb.getValue()
            self.parameter.fuAlgorithm = self.fuAlgorithmCmb.getValue()
            self.parameter.ruLightId = self.ruLightCmb.getPosValue()
            self.parameter.fuLightId = self.fuLightCmb.getPosValue()
            self.saveFlag = True
            self.destroy()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Vision Setting: {}".format(error))
            messagebox.showerror("Save Vision Setting", "Please check the setting values!\nDetail: {}".format(error))
            return

    def clickBtnCancel(self):
        self.destroy()

    def showLastSetting(self):
        try:
            self.ruCameraCmb.setPosValue(self.parameter.ruCameraId)
            self.fuCameraCmb.setPosValue(self.parameter.fuCameraId)
            self.ruAlgorithmCmb.setStringValue(self.parameter.ruAlgorithm)
            self.fuAlgorithmCmb.setStringValue(self.parameter.fuAlgorithm)
            self.ruLightCmb.setPosValue(self.parameter.ruLightId)
            self.fuLightCmb.setPosValue(self.parameter.fuLightId)

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Vision setting show last setting: {}".format(error))
            print("Vision setting show last setting", "{}".format(error))