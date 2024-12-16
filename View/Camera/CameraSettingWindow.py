from CommonAssit.FileManager import JsonFile
import tkinter.messagebox as messagebox
from Modules.Camera.CameraParameter import CameraParameter
from Modules.Camera.CameraParameter import CameraInterface
from Modules.Camera.CameraParameter import CameraBrand
from Modules.Camera.CameraParameter import CameraFlip
from Modules.Camera.CameraParameter import CameraRotate
import os
import CommonAssit.CommonAssit as CommonAssit
from Modules.Camera.CameraNameList import CameraNameList
from View.Common.CommonStepFrame import InputParamFrame
import jsonpickle
from View.Common.VisionUI import *

class CameraSettingWindow(VisionTopLevel):

    parameterList =[]
    listCameraId = []
    listIdCmb: ttk.Combobox
    listTypeComboBox: ttk.Combobox
    listBrandComboBox: ttk.Combobox
    listFlipCombobox: ttk.Combobox
    listRotateCombobox: ttk.Combobox

    idChoosen = 0
    listType = []
    listBrand = []
    listFlip = []
    listRotate = []

    btnClose: CloseButton
    btnOk: OkButton

    def __init__(self, mainWindow, cameraManger):
        from MainWindow import MainWindow
        from Connection.Camera import CameraManager
        VisionTopLevel.__init__(self)
        self.mainWindow: MainWindow = mainWindow
        self.cameraManger: CameraManager = cameraManger
        self.currentCameraParameter = CameraParameter()

        self.initValue()
        self.windowSetting()
        self.createView()
        self.showCurrentCameraParameter(0)
        self.registerNotification()

    def registerNotification(self):
        self.mainWindow.notificationCenter.add_observer(with_block=self.destroy, for_name="Press_Escape")
        # self.mainWindow.notificationCenter.add_observer(with_block=self.clickBtnOk, for_name="Press_Enter")
        self.mainWindow.notificationCenter.add_observer(with_block=self.clickBtnOk, for_name="Press_Enter")

    def initValue(self):
        self.listBrand = []
        self.listType = []
        self.listRotate = []
        self.listFlip = []
        self.parameterList = []

        for camera in self.cameraManger.cameraList:
            self.parameterList.append(camera.parameter)
        self.currentCameraParameter = self.parameterList[0]

        for type in CameraInterface:
            self.listType.append(type.value)
        for brand in CameraBrand:
            self.listBrand.append(brand.value)

        for flip in CameraFlip:
            self.listFlip.append(flip.value)

        for rotate in CameraRotate:
            self.listRotate.append(rotate.value)

    def windowSetting(self):
        self.title(self.mainWindow.languageManager.localized("settingCamera"))
        width = 280
        height = 433
        self.iconbitmap(CommonAssit.resource_path('resource\\appIcon.ico'))
        self.geometry("{}x{}+{}+{}".format(width, height, int
        (self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width() / 2 - width / 2),
                                           int
                                           (
                                               self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height() / 2 - height / 2)))
        self.resizable(0, 0)
        self.grab_set()

    def createView(self):
        self.listCameraId = []
        self.listCameraName = []
        for idx in range(15):
            self.listCameraId.append(idx)

        for name in CameraNameList:
            self.listCameraName.append(name.value)

        xdistance = 75
        ydistance = 45

        self.nameLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("name"))
        self.nameLabel.place(x=5, y=5)
        self.listnameCmb = ttk.Combobox(self, value=self.listCameraName, state='readonly', cursor="hand2")
        self.listnameCmb.bind("<<ComboboxSelected>>", self.cameraNameSelected)
        self.listnameCmb.place(x=xdistance, y=5)

        self.idLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("id"))
        self.idLabel.place(x=5, y=5 + ydistance)
        self.listIdCmb = ttk.Combobox(self, value=self.listCameraId, state='readonly', cursor="hand2")
        self.listIdCmb.bind("<<ComboboxSelected>>", self.camIdSelected)
        self.listIdCmb.place(x=xdistance, y=5 + ydistance)

        self.typeLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("connectionType"))
        self.typeLabel.place(x=5, y= 5 + 2*ydistance)
        self.listTypeComboBox = ttk.Combobox(self, value=self.listType, state='readonly', cursor="hand2")
        self.listTypeComboBox.bind("<<ComboboxSelected>>", self.typeSelected)
        self.listTypeComboBox.place(x=xdistance, y=5 +2*ydistance)

        self.brandLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("brand"))
        self.brandLabel.place(x=5, y=5 + 3*ydistance)
        self.listBrandComboBox = ttk.Combobox(self, value=self.listBrand, state="readonly", cursor="hand2")
        self.listBrandComboBox.bind("<<ComboboxSelected>>", self.brandSelected)
        self.listBrandComboBox.place(x=xdistance, y=5 + 3*ydistance)

        self.flipLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("flipCamera"))
        self.flipLabel.place(x=5, y=5 + 4 * ydistance)
        self.listFlipCombobox = ttk.Combobox(self, value=self.listFlip, state="readonly", cursor="hand2")
        self.listFlipCombobox.bind("<<ComboboxSelected>>", self.flipSelected)
        self.listFlipCombobox.place(x=xdistance, y=5 + 4 * ydistance)

        self.rotateLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("rotateCamera"))
        self.rotateLabel.place(x=5, y=5 + 5 * ydistance)
        self.listRotateCombobox = ttk.Combobox(self, value=self.listRotate, state="readonly", cursor="hand2")
        self.listRotateCombobox.bind("<<ComboboxSelected>>", self.rotateSelected)
        self.listRotateCombobox.place(x=xdistance, y=5 + 5 * ydistance)

        self.textScale = InputParamFrame(self, "Text size : ", yPos=5 + 6 * ydistance, height=ydistance)
        self.textThickness = InputParamFrame(self, "Text thickness : ", yPos=5 + 7 * ydistance, height=ydistance)


        self.btnOk = OkButton(self, command=self.clickBtnOk)
        self.btnOk.place(relx=0.15,y=5 + 8.5 * ydistance, width=80, height=28)

        self.btnClose = CloseButton(self, command=self.destroy)
        self.btnClose.place(relx=0.55, y=5 + 8.5 * ydistance, width=80, height=28)


    def showLastSetting(self):
        return
        # cameraSetting = JsonFile("./config/camera.json")
        # cameraSetting.readFile()
        # self.interfaceChosen = CameraInterface.usb3InterFace.value
        # self.brandChosen = CameraBrand.basler.value
        #
        # if len(cameraSetting.data) != 0:
        #     self.idChoosen = cameraSetting.data[0][0]
        #     try:
        #         self.interfaceChosen = cameraSetting.data[0][1]
        #         self.brandChosen = cameraSetting.data[0][2]
        #         self.flipChosen = cameraSetting.data[0][3]
        #         self.rotateChosen = cameraSetting.data[0][4]
        #     except:
        #         pass
        #
        # self.listIdCmb.current(self.idChoosen)
        # self.listTypeComboBox.current(self.listType.index(self.interfaceChosen))
        # self.listBrandComboBox.current(self.listBrand.index(self.brandChosen))
        # self.listFlipCombobox.current(self.listFlip.index(self.flipChosen))
        # self.listRotateCombobox.current(self.listRotate.index(self.rotateChosen))


    def showCurrentCameraParameter(self, index = None):
        if index is not None:
            cameraPos = index
        else:
            cameraPos = self.listnameCmb.current()

        currentCamera = self.parameterList[cameraPos]

        self.listnameCmb.current(index)
        self.listIdCmb.current(self.listCameraId.index(currentCamera.id))
        self.listTypeComboBox.current(self.listType.index(currentCamera.interface))
        self.listBrandComboBox.current(self.listBrand.index(currentCamera.brand))
        self.listFlipCombobox.current(self.listFlip.index(currentCamera.flip))
        self.listRotateCombobox.current(self.listRotate.index(currentCamera.rotate))
        self.textScale.setValue(currentCamera.textScale)
        self.textThickness.setValue(currentCamera.textThickness)

    def clickBtnOk(self):
        try:
            self.saveCameraSelected()
            self.cameraManger.getInfo()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Camera setting : {}".format(error))
            messagebox.showerror(self.mainWindow.languageManager.localized("cameraChangeTitle"), "{}".format(error))
        self.destroy()

    def cameraNameSelected(self, event):
        self.currentCameraParameter = self.parameterList[self.listnameCmb.current()]
        self.showCurrentCameraParameter()

    def camIdSelected(self, event):
        value = self.listIdCmb.current()
        self.currentCameraParameter.id = value
        self.saveCameraSelected()

    def typeSelected(self, event):
        value = self.listTypeComboBox.get()
        self.currentCameraParameter.interface = value
        self.saveCameraSelected()

    def brandSelected(self, event):
        value = self.listBrandComboBox.get()
        self.currentCameraParameter.brand = value
        self.saveCameraSelected()

    def flipSelected(self, event):
        value = self.listFlipCombobox.get()
        self.currentCameraParameter.flip = value
        self.saveCameraSelected()

    def rotateSelected(self, event):
        value = self.listRotateCombobox.get()
        self.currentCameraParameter.rotate = value
        self.saveCameraSelected()

    def saveCameraSelected(self):
        try:
            self.currentCameraParameter.textScale = self.textScale.getFloatValue()
            self.currentCameraParameter.textThickness = self.textThickness.getIntValue()
        except Exception as error:
            messagebox.showwarning("Save camera parameter", "Detail: {}".format(error))
        self.parameterList[self.listnameCmb.current()] = self.currentCameraParameter
        self.cameraManger.save(self.parameterList)

    def show(self):
        return
