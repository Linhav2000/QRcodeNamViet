import Modules.Camera.IC_Lib.tisgrabber as IC

class ImagingSourceCamera:

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.camera = IC.TIS_CAM()


    def connect(self, cameraId=None, cameraName=None):
        try:
            devices = self.camera.GetDevices()
            if len(devices) < 1:
                text = "There no the imaging source camera connected!, Check cable or setting!"
                self.mainWindow.runningTab.insertLog("There no the imaging source camera connected!, Check cable or setting!")
                self.mainWindow.showError(text=text)
                return False

            if cameraId is not None:
                if cameraId > len(devices):
                    text = "There camera Id is grater than number of connected camera!\nPlease change the camera ID"
                    self.mainWindow.runningTab.insertLog(text)
                    self.mainWindow.showError(text=text)
                    return False
                deviceName = devices[cameraId].decode("utf-8")
                self.camera.open(deviceName)
                self.camera.StartLive(1)
                text = "Connect the imaging source camera id = {}. name = {} successfully!".format(cameraId, deviceName)
                self.mainWindow.runningTab.insertLog(text)
                self.mainWindow.showBottomMiddleText(text=text)
                return True

        except Exception as error:
            text = "Cannot connect Imaging source camera\nDetail: {}".format(error)
            self.mainWindow.showError(text=text)
            self.mainWindow.runningTab.insertLog(text)
            return False

    def disconnect(self):
        try:
            self.camera.StopLive()
        except Exception as error:
            text = "Cannot disconnect Imaging source camera\nDetail: {}".format(error)
            self.mainWindow.showError(text=text)
            self.mainWindow.runningTab.insertLog(text)

    def takePicture(self):
        try:
            # Snap an image
            self.camera.SnapImage()
            # Get the image
            image = self.camera.GetImage()
            return True, image
        except Exception as error:
            text = "Cannot take picture from Imaging source camera\nDetail: {}".format(error)
            self.mainWindow.showError(text=text)
            self.mainWindow.runningTab.insertLog(text)
            return False, None
