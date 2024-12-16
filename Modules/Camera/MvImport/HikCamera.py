from Modules.Camera.MvImport.MvCameraControl_class import *
from CommonAssit import TimeControl
import cv2 as cv
import numpy as np
import threading

class HikCamera:
    camera = None
    data_buf = None
    nPayloadSize = None
    stEnumValue = None
    stFrameInfo = None
    n_save_image_size = None
    isCaptureVideo = False
    buf_cache = None

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def connect(self, cameraId):
        try:
            deviceList = MV_CC_DEVICE_INFO_LIST()
            tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE

            # ch:枚举设备 | en:Enum device
            ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
            if ret != 0:
                print("enum devices fail! ret[0x%x]" % ret)
                return False

            if deviceList.nDeviceNum == 0:
                print("find no device!")
                return False

            print("Find %d devices!" % deviceList.nDeviceNum)

            self.camera = MvCamera()
            # ch:选择设备并创建句柄 | en:Select device and create handle
            stDeviceList = cast(deviceList.pDeviceInfo[int(cameraId)], POINTER(MV_CC_DEVICE_INFO)).contents

            ret = self.camera.MV_CC_CreateHandle(stDeviceList)
            if ret != 0:
                print("create handle fail! ret[0x%x]" % ret)
                return False
            # ch:打开设备 | en:Open device
            ret = self.camera.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
            if ret != 0:
                print("open device fail! ret[0x%x]" % ret)
                return False

            # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
            if stDeviceList.nTLayerType == MV_GIGE_DEVICE:
                nPacketSize = self.camera.MV_CC_GetOptimalPacketSize()
                if int(nPacketSize) > 0:
                    ret = self.camera.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
                    if ret != 0:
                        print("Warning: Set Packet Size fail! ret[0x%x]" % ret)
                else:
                    print("Warning: Get Packet Size fail! ret[0x%x]" % nPacketSize)

            stBool = c_bool(False)
            ret = self.camera.MV_CC_GetBoolValue("AcquisitionFrameRateEnable", byref(stBool))
            if ret != 0:
                print("get AcquisitionFrameRateEnable fail! ret[0x%x]" % ret)
                return False

            # ch:设置触发模式为off | en:Set trigger mode as off
            ret = self.camera.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
            if ret != 0:
                print("set trigger mode fail! ret[0x%x]" % ret)
                return  False

            # ch:获取图像像素 | en:Get the pixelFormat of the image
            self.stEnumValue = MVCC_ENUMVALUE()
            memset(byref(self.stEnumValue), 0, sizeof(MVCC_ENUMVALUE))
            ret = self.camera.MV_CC_GetEnumValue("PixelFormat", self.stEnumValue)
            if ret != 0:
                print("get PixelFormat fail! nRet [0x%x]" % ret)
                return False

            # ch:获取数据包大小 | en:Get payload size
            stParam = MVCC_INTVALUE()
            memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))

            ret = self.camera.MV_CC_GetIntValue("PayloadSize", stParam)
            if ret != 0:
                print("get payload size fail! ret[0x%x]" % ret)
                return False
            self.nPayloadSize = stParam.nCurValue

            if None == self.data_buf:
                self.data_buf = (c_ubyte * self.nPayloadSize)()

            return True
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Hikvision camera connection: {}".format(error))
        return False

    def disconnect(self):
        try:
            # ch:关闭设备 | Close device
            ret = self.camera.MV_CC_CloseDevice()
            if ret != 0:
                print("close deivce fail! ret[0x%x]" % ret)
                del self.data_buf

            # ch:销毁句柄 | Destroy handle
            ret = self.camera.MV_CC_DestroyHandle()
            if ret != 0:
                print("destroy handle fail! ret[0x%x]" % ret)
                del self.data_buf

            del self.data_buf

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Hik Vision camera disconnect: {}".format(error))

    def takePic(self):
        time = TimeControl.time()
        # ch:开始取流 | en:Start grab image
        ret = self.camera.MV_CC_StartGrabbing()
        if ret != 0:
            print("start grabbing fail! ret[0x%x]" % ret)
            return False, None
        data_buf = (c_ubyte * self.nPayloadSize)()
        numArray = None
        img_buff = None
        try:
            self.stFrameInfo = MV_FRAME_OUT_INFO_EX()
            memset(byref(self.stFrameInfo), 0, sizeof(self.stFrameInfo))
            ret = self.camera.MV_CC_GetOneFrameTimeout(byref(self.data_buf), self.nPayloadSize, self.stFrameInfo, 1000)

            print(TimeControl.time() - time)
            if ret == 0:

                self.n_save_image_size = self.stFrameInfo.nWidth * self.stFrameInfo.nHeight * 3 + 2048
                if img_buff is None:
                    img_buff = (c_ubyte * self.n_save_image_size)()

                data = np.frombuffer(self.data_buf, count=int(self.stFrameInfo.nFrameLen), dtype=np.uint8, offset=0)
                numArray = self.convert_type(data=data, code=self.stFrameInfo.enPixelType)

        except Exception as error:
            # self.mainWindow.runningTab.insertLog("ERROR Hik Vision Take pic: {}".format(error))
            print("error: unable to start thread")
            ret = self.camera.MV_CC_StopGrabbing()
            return False, None
        # self.mainWindow.runningTab.insertLog("hik take pic time: {}".format(TimeControl.time() - time))
        # ch:停止取流 | en:Stop grab image
        ret = self.camera.MV_CC_StopGrabbing()

        if ret != 0:
            print("stop grabbing fail! ret[0x%x]" % ret)
            del data_buf
            return False, None
        if numArray is None:
            return False, numArray
        else:
            return True,  numArray

    def captureVideo(self, command=None):
        if self.isCaptureVideo:
            return
        else:
            self.isCaptureVideo = True
        captureVideoThread = threading.Thread(target=self.captureVideoThread, args=(command,))
        captureVideoThread.start()

    def stopCaptureVideo(self):
        self.isCaptureVideo = False

    def captureVideoThread(self, command=None):

        time = TimeControl.time()
        # ch:开始取流 | en:Start grab image
        ret = self.camera.MV_CC_StartGrabbing()
        if ret != 0:
            print("start grabbing fail! ret[0x%x]" % ret)
            return
        data_buf = (c_ubyte * self.nPayloadSize)()
        numArray = None
        img_buff = None
        try:
            self.stFrameInfo = MV_FRAME_OUT_INFO_EX()
            memset(byref(self.stFrameInfo), 0, sizeof(self.stFrameInfo))
            while self.isCaptureVideo:
                time = TimeControl.time()
                ret = self.camera.MV_CC_GetOneFrameTimeout(byref(self.data_buf), self.nPayloadSize, self.stFrameInfo, 1000)

                if ret == 0:

                    self.n_save_image_size = self.stFrameInfo.nWidth * self.stFrameInfo.nHeight * 3 + 2048
                    if img_buff is None:
                        img_buff = (c_ubyte * self.n_save_image_size)()

                    data = np.frombuffer(self.data_buf, count=int(self.stFrameInfo.nFrameLen), dtype=np.uint8, offset=0)

                    numArray = self.convert_type(data=data, code=self.stFrameInfo.enPixelType)
                print(f"Capture time {TimeControl.time() - time}")
                if command is None:
                    self.mainWindow.showImage(numArray, original=True)
                else:
                    command(numArray)
                TimeControl.sleep(1)
                # self.mainWindow.runningTab.insertLog("hik take pic time: {}".format(TimeControl.time() - time))
        except Exception as error:
            # self.mainWindow.runningTab.insertLog("ERROR Hik Vision Take pic: {}".format(error))
            print("error: unable to start thread")
            # ch:停止取流 | en:Stop grab image
            ret = self.camera.MV_CC_StopGrabbing()
            if ret != 0:
                print("stop grabbing fail! ret[0x%x]" % ret)
                del data_buf
            return

        # self.mainWindow.runningTab.insertLog("hik take pic time: {}".format(TimeControl.time() - time))
        # ch:停止取流 | en:Stop grab image
        ret = self.camera.MV_CC_StopGrabbing()
        if ret != 0:
            print("stop grabbing fail! ret[0x%x]" % ret)
            del data_buf
    def convert_type(self, data, code):
        numArray = None
        # Mono 8
        if code == PixelType_Gvsp_Mono8:
            numArray = data.reshape(self.stFrameInfo.nHeight, self.stFrameInfo.nWidth)
        # bayerGB 8
        elif code == PixelType_Gvsp_BayerBG8:
            data = data.reshape(self.stFrameInfo.nHeight, self.stFrameInfo.nWidth, -1)
            numArray = cv.cvtColor(data, cv.COLOR_BAYER_BG2RGB)
        elif code == PixelType_Gvsp_BayerGB8:
            data = data.reshape(self.stFrameInfo.nHeight, self.stFrameInfo.nWidth, -1)
            numArray = cv.cvtColor(data, cv.COLOR_BAYER_GB2RGB)
        elif code == PixelType_Gvsp_BayerRG8:
            data = data.reshape(self.stFrameInfo.nHeight, self.stFrameInfo.nWidth, -1)
            numArray = cv.cvtColor(data, cv.COLOR_BAYER_RG2RGB)
        # RGB 8
        elif code == PixelType_Gvsp_RGB8_Packed:
            data = data.reshape(self.stFrameInfo.nHeight, self.stFrameInfo.nWidth, -1)
            numArray = cv.cvtColor(data, cv.COLOR_RGB2BGR)
        # BGR 8
        elif code == PixelType_Gvsp_BGR8_Packed:
            numArray = data.reshape(self.stFrameInfo.nHeight, self.stFrameInfo.nWidth, -1)

        return numArray

    def is_color_data(self, enGvspPixelType):
        if PixelType_Gvsp_BayerGR8 == enGvspPixelType or PixelType_Gvsp_BayerRG8 == enGvspPixelType \
            or PixelType_Gvsp_BayerGB8 == enGvspPixelType or PixelType_Gvsp_BayerBG8 == enGvspPixelType \
            or PixelType_Gvsp_BayerGR10 == enGvspPixelType or PixelType_Gvsp_BayerRG10 == enGvspPixelType \
            or PixelType_Gvsp_BayerGB10 == enGvspPixelType or PixelType_Gvsp_BayerBG10 == enGvspPixelType \
            or PixelType_Gvsp_BayerGR12 == enGvspPixelType or PixelType_Gvsp_BayerRG12 == enGvspPixelType \
            or PixelType_Gvsp_BayerGB12 == enGvspPixelType or PixelType_Gvsp_BayerBG12 == enGvspPixelType \
            or PixelType_Gvsp_BayerGR10_Packed == enGvspPixelType or PixelType_Gvsp_BayerRG10_Packed == enGvspPixelType \
            or PixelType_Gvsp_BayerGB10_Packed == enGvspPixelType or PixelType_Gvsp_BayerBG10_Packed == enGvspPixelType \
            or PixelType_Gvsp_BayerGR12_Packed == enGvspPixelType or PixelType_Gvsp_BayerRG12_Packed== enGvspPixelType \
            or PixelType_Gvsp_BayerGB12_Packed == enGvspPixelType or PixelType_Gvsp_BayerBG12_Packed == enGvspPixelType \
            or PixelType_Gvsp_YUV422_Packed == enGvspPixelType or PixelType_Gvsp_YUV422_YUYV_Packed == enGvspPixelType:
            return True
        else:
            return False

    def is_mono_data(self, enGvspPixelType):
        if PixelType_Gvsp_Mono8 == enGvspPixelType or PixelType_Gvsp_Mono10 == enGvspPixelType \
            or PixelType_Gvsp_Mono10_Packed == enGvspPixelType or PixelType_Gvsp_Mono12 == enGvspPixelType \
            or PixelType_Gvsp_Mono12_Packed == enGvspPixelType:
            return True
        else:
            return False


    def color_numpy(self, data, nWidth, nHeight):
        data_ = np.frombuffer(data, count=int(nWidth*nHeight*3), dtype=np.uint8, offset=0)
        data_r = data_[0:nWidth*nHeight*3:3]
        data_g = data_[1:nWidth*nHeight*3:3]
        data_b = data_[2:nWidth*nHeight*3:3]

        data_r_arr = data_r.reshape(nHeight, nWidth)
        data_g_arr = data_g.reshape(nHeight, nWidth)
        data_b_arr = data_b.reshape(nHeight, nWidth)
        numArray = np.zeros([nHeight, nWidth, 3],"uint8")

        numArray[:, :, 2] = data_r_arr
        numArray[:, :, 1] = data_g_arr
        numArray[:, :, 0] = data_b_arr
        return numArray

    def mono_numpy(self, data, nWidth, nHeight):
        data_ = np.frombuffer(data, count=int(nWidth * nHeight), dtype=np.uint8, offset=0)
        data_mono_arr = data_.reshape(nHeight, nWidth)
        numArray = np.zeros([nHeight, nWidth, 1],"uint8")
        numArray[:, :, 0] = data_mono_arr
        return numArray