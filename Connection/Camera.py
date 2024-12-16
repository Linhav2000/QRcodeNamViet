import cv2 as cv
try:
    import gxipy as gx
except:
    pass
import numpy as np
from pypylon import pylon
try:
    import PyCapture2
except:
    pass
import tkinter.messagebox as messagebox
import ImageProcess.ImageProcess as ImageProcess
from Connection.ConnectionStatus import ConnectionStatus
from CommonAssit.FileManager import JsonFile
from CommonAssit import TimeControl
from CommonAssit import PathFileControl
import jsonpickle
from Modules.Camera.MvImport.MvCameraControl_class import *
from Modules.Camera.MvImport.HikCamera import HikCamera
from Modules.Camera.CameraNameList import CameraNameList
from Modules.Camera.CameraParameter import CameraParameter
from Modules.Camera.CameraParameter import CameraInterface
from Modules.Camera.CameraParameter import CameraBrand
from Modules.Camera.CameraParameter import CameraFlip
from Modules.Camera.CameraParameter import CameraRotate
from tkinter import filedialog
import threading

class Camera:
    cap: cv.VideoCapture
    cam = ()
    ready = False
    reconnectFlag = False
    baslerGigECamera = None
    pgBus = None
    pgCamera = None
    hikCamera: HikCamera = None
    imagingSourceCamera = None
    frameRate = 23
    trigger = False

    isRecording = False
    isPaused = False

    caliPath = "./config/Calibration"

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.parameter = CameraParameter()
        self.mainWindow:MainWindow = mainWindow
        # self.device_manager = gx.DeviceManager()

    def isConnected(self):
        return self.cap.isOpened()


    def connect(self):
        if self.ready:
            return True

        if self.parameter.interface == CameraInterface.gigEInterFace.value and self.parameter.brand == CameraBrand.csr.value:
            self.ready = self.csrGigEConnect()
        elif self.parameter.brand == CameraBrand.basler.value:
            self.ready = self.baslerGigEConnect()
        elif self.parameter.brand == CameraBrand.hikVision.value:
            self.ready = self.hikGigEConnect()
        elif self.parameter.interface == CameraInterface.usb3InterFace.value and self.parameter.brand == CameraBrand.pointGrey.value:
            self.ready = self.pgUsbConnect()
        elif self.parameter.brand == CameraBrand.wc_dshow.value or self.parameter.brand == CameraBrand.wc_default.value:
            self.ready = self.usb3WebcamConnect()
        elif self.parameter.interface == CameraInterface.usb3InterFace.value and self.parameter.brand == CameraBrand.imageSource.value:
            self.ready = self.usb3ISConnect()

        if self.ready:
            self.mainWindow.runningTab.setCameraStatus(ConnectionStatus.connected)
        return self.ready

    def usb3ISConnect(self):
        from Modules.Camera.IC_Lib.ImagingSourceCamrera import ImagingSourceCamera
        try:
            self.imagingSourceCamera = ImagingSourceCamera(self.mainWindow)
            return self.imagingSourceCamera.connect(self.parameter.id)
        except:
            return False

    def usb3WebcamConnect(self):
        try:
            if self.parameter.brand == CameraBrand.wc_dshow.value:
                self.cap = cv.VideoCapture(self.parameter.id + cv.CAP_DSHOW)
            else:
                self.cap = cv.VideoCapture(self.parameter.id)

            # self.cap = cv.VideoCapture(self.cameraParameter.id + cv.CAP_FFMPEG)
            if self.cap.isOpened():
                self.ready = True
                try:
                    self.mainWindow.runningTab.insertLog("Camera is connected successfully!")
                except:
                    pass
                self.mainWindow.runningTab.setCameraStatus(ConnectionStatus.connected)
                return  True
            else:
                text = "Cannot to connect the {0}, check the ID or connection!".format(self.parameter.name)
                self.mainWindow.showError(text=text)
        except:
            text = "Cannot to connect the {0}, check the ID or connection!".format(self.parameter.name)
            self.mainWindow.showError(text=text)
        self.mainWindow.runningTab.insertLog("Connect Camera Failed!")
        return False

    def pgUsbConnect(self):
        if self.pgBus is None:
            try:
                self.pgBus = PyCapture2.BusManager()
                num_cams = self.pgBus.getNumOfCameras()
                print('Number of cameras detected: ', num_cams)
                self.mainWindow.runningTab.insertLog("Point Grey camera connect: Number of cameras detected: {}".format(num_cams))
            except Exception as error:
                self.mainWindow.runningTab.insertLog("ERROR Point Grey camera connect: {}".format(error))
        if self.pgBus is not None:
            try:
                self.pgCamera = PyCapture2.Camera()
                uid = self.pgBus.getCameraFromIndex(self.parameter.id)
                self.pgCamera.connect(uid)
                cam_info = self.pgCamera.getCameraInfo()
                self.mainWindow.runningTab.insertLog('\n*** CAMERA INFORMATION ***\n')
                self.mainWindow.runningTab.insertLog('Serial number - %d' % cam_info.serialNumber)
                self.mainWindow.runningTab.insertLog('Camera model - %s' % cam_info.modelName)
                self.mainWindow.runningTab.insertLog('Camera vendor - %s' % cam_info.vendorName)
                self.mainWindow.runningTab.insertLog('Sensor - %s' % cam_info.sensorInfo)
                self.mainWindow.runningTab.insertLog('Resolution - %s' % cam_info.sensorResolution)
                self.mainWindow.runningTab.insertLog('Firmware version - %s' % cam_info.firmwareVersion)
                self.mainWindow.runningTab.insertLog('Firmware build time - %s' % cam_info.firmwareBuildTime)
                self.ready = True
                return True
            except Exception as error:
                text = "Cannot to connect the {0}, check the ID or connection!".format(self.parameter.name)
                self.mainWindow.showError(text=text)
                self.mainWindow.runningTab.insertLog("ERROR Point Grey camera connect: {}".format(error))
        return False

    def hikGigEConnect(self):
        try:
            self.hikCamera = HikCamera(self.mainWindow)
            return self.hikCamera.connect(self.parameter.id)
        except:
            pass

    def baslerGigEConnect(self):
        try:
            self.converter = pylon.ImageFormatConverter()

            # converting to opencv bgr format
            self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
            self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

            self.pylonManager = pylon.TlFactory.GetInstance()

            cameraIdList = []

            for i in self.pylonManager.EnumerateDevices():
                cameraIdList.append(i)
            self.baslerGigECamera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(cameraIdList[self.parameter.id]))
            self.baslerGigECamera.Open()
            self.baslerGigECamera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        except Exception as error:
            text = "ERROR Basler GigE Connect: {}".format(error)
            self.mainWindow.runningTab.insertLog(text)
            self.mainWindow.showError(text=text)
            return False
        return True
    

    def csrGigEConnect(self):
        try:
            self.device_manager = gx.DeviceManager()
            dev_num, dev_info_list = self.device_manager.update_device_list()
            if dev_num == 0:
                self.mainWindow.showError(text="There is no device connection")
                return False

            self.cam = self.device_manager.open_device_by_index(1)
            # set continuous acquisition
            self.cam.TriggerMode.set(gx.GxSwitchEntry.OFF)

            # set exposure
            self.cam.ExposureTime.set(10000)

            # set gain
            self.cam.Gain.set(10.0)
            try:
                self.mainWindow.runningTab.insertLog("Camera is connected successfully!")
            except:
                pass
            return True
        except:
            text = "Cannot to connect the {0}, check the ID or connection!".format(self.parameter.name)
            self.mainWindow.showError(text=text)
            return False

    def load_feature(self):
        if not PathFileControl.pathExisted(self.parameter.feature_path):
            messagebox.showwarning("Camera Load Feature", "The feature path is not existed!")
            return
        if self.parameter.brand ==CameraBrand.basler.value:
            self.load_basler_feature()

    def load_basler_feature(self):
        if not self.connect():
            return
        try:
            pylon.FeaturePersistence.Load(self.parameter.feature_path, self.baslerGigECamera.GetNodeMap(), True)
        except Exception as error:
            text = f"ERROR Camera load feature. Detail: {error}"
            self.mainWindow.runningTab.insertLog(text)

    def start_record(self):
        if self.parameter.brand == CameraBrand.basler.value:
            basler_record_Thread = threading.Thread(target=self.start_basler_record, args=())
            basler_record_Thread.start()

    def pause_record(self):
        self.isPaused = True

    def stop_record(self):
        self.isPaused = False
        self.isRecording = False

    def start_basler_record(self):
        self.isRecording = True
        image = None
        try:
            if not self.connect():
                self.isRecording = False
                return False, None
            ret, image = self.takePicture()
            if not ret:
                self.mainWindow.showError("Cannot take the picture\nPLease check the camera or connection!")
                return
            tempPath = "./record_camera.avi"
            out = cv.VideoWriter(tempPath,
                                 cv.VideoWriter_fourcc(*"XVID"),
                                 10,
                                 (1920, 1080))
            self.baslerGigECamera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
            while self.baslerGigECamera.IsGrabbing() and self.isRecording:
                if not self.isPaused:
                    grabResult = self.baslerGigECamera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                    if grabResult.GrabSucceeded():
                        # Access the image data
                        img = self.converter.Convert(grabResult)
                        image = img.GetArray()

                        image = self.flipImage(image)
                        image = self.rotateImage(image)
                        image = cv.resize(image, dsize=(1920, 1080))
                        out.write(image)  # writing the RBG image to file
                        self.mainWindow.showImage(image, original=True)
                    grabResult.Release()

            self.baslerGigECamera.StopGrabbing()
            self.isRecording = False
            self.isPaused = False
            fileName = filedialog.asksaveasfilename(title='Select Image',
                                                    filetypes=(('AVI Files', '*.avi'), ('All files', '*.*')),
                                                    initialdir="/áéá")

            if fileName != "":
                if not fileName.endswith(".avi"):
                    fileName = fileName + ".avi"
                PathFileControl.deleteFile(fileName)
                PathFileControl.rename(tempPath, fileName)

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Basler Record Video : {}".format(error))
        return

    def screenRecordThread(self):
        self.isRecording =  True
        fourcc = cv.VideoWriter_fourcc(*"XVID")
        SCREEN_SIZE = (1920, 1080)
        tempPath = "./Recorded.avi"
        out = cv.VideoWriter(tempPath, fourcc, 13,
                             SCREEN_SIZE)  # Here screen resolution is 1366 x 768, you can change it depending upon your need
        while self.isRecording:
            if not self.isPaused:
                img = pyautogui.screenshot()  # capturing screenshot
                frame = np.array(img)  # converting the image into numpy array representation
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  # converting the BGR image into RGB image
                out.write(frame)  # writing the RBG image to file
            TimeControl.sleep(1)
        out.release()  # closing the video file
        self.isRecording = False
        self.isPaused = False
        fileName = filedialog.asksaveasfilename(title='Select Image',
                                                  filetypes=(('AVI Files','*.avi'),('All files', '*.*')),
                                                  initialdir="/áéá")

        if fileName != "":
            if not fileName.endswith(".avi"):
                fileName = fileName + ".avi"
            PathFileControl.deleteFile(fileName)
            PathFileControl.rename(tempPath, fileName)
    def save_feature(self):
        return

    def disconnect(self):
        if not self.ready:
            return
        if self.mainWindow.workingThread.runningFlag:
            if not self.mainWindow.runningTab.clickBtnStart():
                return
        if self.parameter.interface == CameraInterface.gigEInterFace.value and self.parameter.brand == CameraBrand.csr.value:
            self.csrGigEDisconnect()
        elif self.parameter.brand == CameraBrand.hikVision.value:
            self.hikGigEDisconnect()
        elif self.parameter.brand == CameraBrand.basler.value:
            self.baslerGigEDisconnect()
        elif self.parameter.interface == CameraInterface.usb3InterFace.value and self.parameter.brand == CameraBrand.pointGrey.value:
            self.pgUsbDisconnect()
        elif self.parameter.brand == CameraBrand.wc_dshow.value or self.parameter.brand == CameraBrand.wc_default.value:
            self.usb3Disconnect()
        elif self.parameter.interface == CameraInterface.usb3InterFace.value and self.parameter.brand == CameraBrand.imageSource.value:
            self.ISCameraDisconnect()

        self.mainWindow.runningTab.setCameraStatus(ConnectionStatus.disconnected)
        self.ready = False
        if self.mainWindow.workingThread.runningFlag:
            self.mainWindow.runningTab.clickBtnStart()

    def ISCameraDisconnect(self):
        try:
            self.ready = False
            self.imagingSourceCamera.disconnect()
        except:
            pass

    def pgUsbDisconnect(self):
        try:
            self.ready = False
            self.pgCamera.disconnect()
        except:
            pass

    def hikGigEDisconnect(self):
        self.ready = False
        self.hikCamera.disconnect()

    def baslerGigEDisconnect(self):

        try:
            self.ready = False
            self.baslerGigECamera.StopGrabbing()
            self.baslerGigECamera.Close()
        except:
            pass

    def csrGigEDisconnect(self):
        # close device
        try:
            self.ready = False
            self.cam.close_device()
        except:
            pass

    def usb3Disconnect(self):
        if self.ready:
            try:
                self.cap.release()
            except Exception as error:
                self.mainWindow.runningTab.insertLog("ERROR Camera Connection: {}".format(error))
                messagebox.showerror("Camera Connection", "{}".format(error))

    def reconnect(self):
        self.disconnect()
        TimeControl.sleep(1000)
        self.connect()

    def changeInfo(self, parameter: CameraParameter):
        if self.ready:
            if self.parameter.id != parameter.id or self.parameter.interface != parameter.interface or self.parameter.brand != parameter.brand:
                self.disconnect()
                TimeControl.sleep(500)
                self.parameter = parameter
                self.connect()

        self.parameter = parameter
    # def reconnect(self):
    #     try:
    #         self.cap = cv.VideoCapture(self.parameter.id + cv.CAP_DSHOW)
    #         if self.cap.isOpened():
    #             self.ready = True
    #             return True
    #     except:
    #         pass
    #     return False

    def reconnectThread(self):
        self.reconnectFlag = True
        while self.reconnectFlag:
            self.mainWindow.runningTab.setCameraStatus(ConnectionStatus.reconnecting)
            if self.reconnect():
                self.reconnectFlag = False
                self.mainWindow.runningTab.setCameraStatus(ConnectionStatus.connected)
                self.mainWindow.runningTab.insertLog("Camera is reconnected")
            cv.waitKey(5)
        self.reconnectFlag = False

    def takePicture(self, cali=True):
        time = TimeControl.time()
        ret = False
        image = None
        if not self.ready:
            if not self.connect():
                text = "Cannot connect to the camera!"
                self.mainWindow.runningTab.insertLog("Cannot connect to the camera!")
                self.mainWindow.showError(text=text)
                return ret, image

        if self.parameter.interface == CameraInterface.gigEInterFace.value and self.parameter.brand == CameraBrand.csr.value:
            ret, image = self.csrGigETakePicture()
        elif self.parameter.brand == CameraBrand.basler.value:
            ret, image = self.baslerGigETakePicture()
        elif self.parameter.brand == CameraBrand.hikVision.value:
            ret, image = self.hikGigETakePicture()
        elif self.parameter.interface == CameraInterface.usb3InterFace.value and self.parameter.brand == CameraBrand.pointGrey.value:
            ret, image = self.pgUsbTakePicture()
        elif self.parameter.brand == CameraBrand.wc_dshow.value or self.parameter.brand == CameraBrand.wc_default.value:
            ret, image = self.usb3TakePicture()
        elif self.parameter.interface == CameraInterface.usb3InterFace.value and self.parameter.brand == CameraBrand.imageSource.value:
            ret, image = self.ISCameraTakePicture()
        # print(f"take pic time: {TimeControl.time() - time}")

        # cv.imshow("image", image)
        if ret:
            if cali:
                try:
                    mtx = np.loadtxt(self.caliPath + f"/{self.parameter.name}/cameraMatrix.txt")
                    dist = np.loadtxt(self.caliPath + f"/{self.parameter.name}/distortionCoefficient.txt")
                    h, w = image.shape[:2]
                    new_camera_mtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
                    # undistort
                    image = cv.undistort(image, mtx, dist, None, new_camera_mtx)
                except:
                    pass
            # print(f"take pic time: {TimeControl.time() - time}")

            image = self.flipImage(image)
            image = self.rotateImage(image)

        self.mainWindow.runningTab.insertLog(f"take pic time: {TimeControl.time() - time}")
        return ret, image

    # def rotateImage(self, image):


    def flipImage(self, image):
        if self.parameter.flip == CameraFlip.vertically.value:
            return ImageProcess.flipVertical(image)
        elif self.parameter.flip == CameraFlip.horizontally.value:
            return ImageProcess.flipHorizontal(image)
        elif self.parameter.flip == CameraFlip.both.value:
            return ImageProcess.flipBoth(image)
        else:
            return image

    def rotateImage(self, image):
        if self.parameter.rotate == CameraRotate._90ClockWise.value:
            return ImageProcess.rotateImage90Clockwise(image)
        elif self.parameter.rotate == CameraRotate._90CounterClockWise.value:
            return ImageProcess.rotateImage90CounterClockwise(image)
        elif self.parameter.rotate == CameraRotate._180degrees.value:
            return ImageProcess.rotateImage180Clockwise(image)
        else:
            return image

    def ISCameraTakePicture(self):
        return self.imagingSourceCamera.takePicture()

    def hikGigETakePicture(self):
        return self.hikCamera.takePic()

    def hikCaptureVideo(self, command=None):
        if not self.connect():
            return

        return self.hikCamera.captureVideo(command=command)

    def hikStopCaptureVideo(self):
        return self.hikCamera.stopCaptureVideo()

    def pgUsbTakePicture(self):
        try:
            self.pgCamera.startCapture()
            time = TimeControl.time()

            imageBuff = self.pgCamera.retrieveBuffer()
            cv_image = np.array(imageBuff.getData(), dtype="uint8").reshape((imageBuff.getRows(), imageBuff.getCols()))
            cv_image = cv.cvtColor(cv_image, cv.COLOR_BAYER_BG2BGR)
            self.pgCamera.stopCapture()
            print(TimeControl.time() - time)
            return True, cv_image.copy()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR point grey take picture : {}".format(error))
            return False, None

    def baslerGigETakePicture(self):
        image = None
        try:
            # self.baslerGigECamera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
            # while self.baslerGigECamera.IsGrabbing():
            grabResult = self.baslerGigECamera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                # Access the image data
                img = self.converter.Convert(grabResult)
                image = img.GetArray()
            grabResult.Release()
            # self.baslerGigECamera.StopGrabbing()
            return True, image
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Basler take picture : {}".format(error))
            return False, None

    def baslerGigECaptureVideo(self, captureFlag, process_cmd=None):
        if captureFlag:
            captureVideoThread = threading.Thread(target=self.captureVideoThread, args=(process_cmd,))
            captureVideoThread.start()
        else:
            self.captureVideoFlag = False

    def captureVideoThread(self, process_cmd=None):
        self.captureVideoFlag = True
        image = None
        try:
            if not self.connect():
                return False, None
            # self.baslerGigECamera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
            while self.baslerGigECamera.IsGrabbing() and self.captureVideoFlag:
                time = TimeControl.time()
                grabResult = self.baslerGigECamera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

                if grabResult.GrabSucceeded():
                    # Access the image data
                    img = self.converter.Convert(grabResult)
                    image = img.GetArray()

                    image = self.flipImage(image)
                    image = self.rotateImage(image)
                    print(f"take pic time = {TimeControl.time() - time}")
                    if process_cmd is None:
                        self.mainWindow.showImage(image, original=True)
                    else:
                        process_cmd(image)

                grabResult.Release()
            # self.baslerGigECamera.StopGrabbing()
            self.captureVideoFlag = False
            return True, image
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Basler take picture : {}".format(error))
            return False, None

    def csrGigETakePicture(self):
        # start data acquisition
        try:
            self.cam.stream_on()
            raw_image = self.cam.data_stream[0].get_image()
            if raw_image is None:
                print("Getting image failed.")
                return False, ()
            # create numpy array with data from raw image
            numpy_image = raw_image.get_numpy_array()

            self.cam.stream_off()

            return True, numpy_image
        except:
            # messagebox.showerror("Take Image", "Cannot take image!")
            return False, ()

    def usb3TakePicture(self):
        image = np.zeros((1, 1))
        ret = False

        if not self.ready:
            # messagebox.showerror("Camera Connection", "You still not connect to the camera!")
            return ret, image.copy()

        if self.ready and self.cap.isOpened():
            try:
                ret, image = self.cap.read()
                return ret, image.copy()
            except:
                # messagebox.showerror("Camera Connect", "Lost of camera connection!")
                return False, ()

    def recordVideo(self):
        if self.mainWindow.workingThread.cameraManager.isRecording:
            self.mainWindow.showBottomMiddleText("Only can record in one camera")
            return
        self.mainWindow.workingThread.cameraManager.isRecording = True
        if self.ready:
            ret, image = self.takePicture()
            if not ret:
                self.mainWindow.showError("Cannot take the picture\nPLease check the camera or connection!")
                return
            fileName = filedialog.asksaveasfilename(title='Record Video', filetypes=(
                                                    ('AVI Files', '*.avi'), ('All files', '*.*')),
                                                    initialdir="/áéá")

            out = cv.VideoWriter(fileName, ".avi", self.frameRate, (image.shape[0], image.shape[1]))
            while self.mainWindow.workingThread.cameraManager.isRecording:
                ret, image = self.takePicture()
                if ret:
                    out.write(image)
                    self.mainWindow.showImage(image=image, original=True)
                else:
                    self.mainWindow.showError("Cannot take the picture\nPLease check the camera or connection!")

                TimeControl.sleep(3)
        else:
            self.mainWindow.showError("Camera still not ready to recode!")

    def baslerHardwareTrigger(self, process_cmd=None):
        triggerThread = threading.Thread(target=self.baslerHardwareTriggerThread, args=(process_cmd,))
        triggerThread.start()

    def baslerHardwareTriggerThread(self, process_cmd=None):
        if not self.ready:
            if not self.connect():
                return
        self.baslerGigECamera.Open()
        self.trigger = True
        print("DeviceClass: ", self.baslerGigECamera.GetDeviceInfo().GetDeviceClass())
        print("DeviceFactory: ", self.baslerGigECamera.GetDeviceInfo().GetDeviceFactory())
        print("ModelName: ", self.baslerGigECamera.GetDeviceInfo().GetModelName())

        ############################################################
        Hardware_Trigger = True

        if Hardware_Trigger:
            # reset registration
            self.baslerGigECamera.RegisterConfiguration(pylon.ConfigurationEventHandler(), pylon.RegistrationMode_ReplaceAll,
                                         pylon.Cleanup_Delete)

        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        self.baslerGigECamera.MaxNumBuffer = 5

        # set exposure time
        # camera.ExposureTimeRaw.SetValue(100)

        # Select the Frame Start trigger
        self.baslerGigECamera.TriggerSelector.SetValue('FrameStart')
        # Acquisition mode
        self.baslerGigECamera.AcquisitionMode.SetValue('Continuous')
        # Enable triggered image acquisition for the Frame Start trigger
        self.baslerGigECamera.TriggerMode.SetValue('On')
        # Set the trigger source to Line 1
        self.baslerGigECamera.TriggerSource.SetValue('Line1')
        # Set the trigger activation mode to rising edge
        self.baslerGigECamera.TriggerActivation.SetValue('RisingEdge')
        # Set the delay for the frame start trigger to 300 µs
        # camera.TriggerDelayAbs.SetValue(300.0)
        # Pixel format
        # camera.PixelFormat.SetValue('Mono8')

        ##############################################################

        self.baslerGigECamera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        converter = pylon.ImageFormatConverter()

        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        count_trigger = 1
        count_image = 1

        PathFileControl.generatePath("./save_images")

        def saveImageThread(count_image, img):
            cv.imencode(".png", img)[1].tofile('./save_images/%06d.png' % count_image)
            # cv.imwrite('./save_images/%06d.png' % count_image, img)
        grabResult = None
        while self.baslerGigECamera.IsGrabbing() and self.trigger:
            print("count_trigger: ", count_trigger)
            count_trigger += 1
            try:
                grabResult = self.baslerGigECamera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)

                if grabResult.GrabSucceeded():
                    print("grabResult is succeeded!")
                    # Access the image data
                    image = converter.Convert(grabResult)
                    img = image.GetArray()
                    if process_cmd is not None:
                        process_cmd(img)
                    else:
                        self.mainWindow.showImage(image, original=True)
                    # img = cv.resize(img,(100, 200))
                    # cv.imshow("qqqimage", img)
                    # thread = threading.Thread(target=saveImageThread, args=(count_image, img))
                    # thread.start()
                    # cv2.imwrite('./save_images/%06d.png'%count_image, img)
                    # print("%06d.png saved"%count_image)
                    count_image += 1

                grabResult.Release()
            except:
                if grabResult is not None:
                    grabResult.Release()
                count_trigger -= 1
                continue

            cv.waitKey(1)

        self.baslerGigECamera.StopGrabbing()
        # # reset registration
        # self.baslerGigECamera.RegisterConfiguration(pylon.ConfigurationEventHandler(),
        #                                             pylon.RegistrationMode_ReplaceAll,
        #                                             pylon.Cleanup_Delete)
        # Enable triggered image acquisition for the Frame Start trigger
        self.baslerGigECamera.TriggerMode.SetValue('Off')
        print("end")
class CameraManager:

    cameraList: [Camera] = []
    currentCamera: Camera
    isRecording = False
    isPause = False
    isCapturing = False

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow
        self.initCamera()
        self.getInfo()


    def initCamera(self):
        self.cameraList = []
        for name in CameraNameList:
            camera = Camera(self.mainWindow)
            parameter = CameraParameter()
            parameter.name = name.value
            camera.parameter = copy.deepcopy(parameter)
            self.cameraList.append(camera)

        self.currentCamera = self.cameraList[self.mainWindow.commonSettingManager.settingParm.currentCamera]

    def getInfo(self):
        folderPath = "./config"
        dataFilePath = "./config/camera.json"
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

        try:
            file = JsonFile(dataFilePath)
            dataList = file.readFile()
            index = 0
            for data in dataList:
                cameraParameter = CameraParameter()
                cameraParameter = jsonpickle.decode(data)
                self.cameraList[index].changeInfo(cameraParameter)
                index += 1

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Camera get info: {}".format(error))
            print("Camera get info: {}".format(error))

    def save(self, parameterList=None):
        folderPath = "./config"
        dataFilePath = "./config/camera.json"
        data = []

        if parameterList is None:
            parameterList = []
            for camera in self.cameraList:
                parameterList.append(camera.parameter)

        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        try:
            for cameraInfo in parameterList:
                data.append(jsonpickle.encode(cameraInfo))
            file = JsonFile(dataFilePath)
            file.data = data
            file.saveFile()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Camera save parameter: {}".format(error))

    def changeCamera(self, index):
        try:
            self.currentCamera = self.cameraList[index]
            self.mainWindow.commonSettingManager.settingParm.currentCamera = index
            self.mainWindow.commonSettingManager.save()
            self.mainWindow.runningTab.resultTab.commonSettingFrame.updateInfo()
            if self.mainWindow.chessboardCalibration is None:
                self.mainWindow.init_chessboard_cali_frame()
            self.mainWindow.chessboardCalibration.cameraCombo.setPosValue(index)
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Change Camera: {}".format(error))

    def disconnectAllCamera(self):
        for camera in self.cameraList:
            camera.disconnect()

    def setting(self):
        from View.Camera.CameraSettingWindow import CameraSettingWindow
        settingWindow = CameraSettingWindow(self.mainWindow, self)

    def load_new_feature(self):
        if self.currentCamera.parameter.brand == CameraBrand.basler.value:
            feature_path = filedialog.askopenfilename(title='Camera Feature Path',
                                                        filetypes=(('PFS File','*.pfs'),('All files', '*.*')),
                                                        initialdir="/áéá")
            if feature_path == "":
                return
            else:
                self.currentCamera.parameter.feature_path = feature_path
                self.save()
        self.currentCamera.load_feature()

    def load_available_feature(self):
        self.currentCamera.load_feature()

    def start_record_camera(self):
        self.currentCamera.start_record()

    def pause_record_camera(self):
        self.currentCamera.pause_record()

    def stop_record_camera(self):
        self.currentCamera.stop_record()