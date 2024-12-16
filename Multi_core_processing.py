import os
from CommonAssit import TimeControl
from CommonAssit import PathFileControl
import cv2 as cv
print("import cv")
import numpy as np
print("import np")
from Modules.Camera.MvImport.MvCameraControl_class import *
print("import mv")
from multiprocessing import Process, Value, Queue, freeze_support
from ImageProcess.Algorithm.AlgorithmParameter import AlgorithmParameter
from ImageProcess import ImageProcess
from CommonAssit.FileManager import *
from ImageProcess.Algorithm.StepParamter import StepParameter
from ImageProcess.Algorithm.MethodList import MethodList
from ImageProcess.Algorithm.AlgorithmResult import AlgorithmResultKey, AlgorithmResult
import jsonpickle
import queue

from Modules.ObjectTracking.CentroidTracker import CentroidTracker
from Modules.ObjectTracking.Trackable_Object import Trackable_Object
from Modules.Camera.CameraParameter import CameraBrand
from imutils.object_detection import non_max_suppression
from Modules.ModelSetting.ModelManager import ModelManager
from Modules.ModelSetting.ModelParameter import ModelParameter

camera = None
data_buf = None
nPayloadSize = 0
def connect_camera():
    global camera
    global data_buf
    global nPayloadSize
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

        camera = MvCamera()
        # ch:选择设备并创建句柄 | en:Select device and create handle
        stDeviceList = cast(deviceList.pDeviceInfo[0], POINTER(MV_CC_DEVICE_INFO)).contents

        ret = camera.MV_CC_CreateHandle(stDeviceList)
        if ret != 0:
            print("create handle fail! ret[0x%x]" % ret)
            return False
        # ch:打开设备 | en:Open device
        ret = camera.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        if ret != 0:
            print("open device fail! ret[0x%x]" % ret)
            return False

        # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
        if stDeviceList.nTLayerType == MV_GIGE_DEVICE:
            nPacketSize = camera.MV_CC_GetOptimalPacketSize()
            if int(nPacketSize) > 0:
                ret = camera.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
                if ret != 0:
                    print("Warning: Set Packet Size fail! ret[0x%x]" % ret)
            else:
                print("Warning: Get Packet Size fail! ret[0x%x]" % nPacketSize)

        stBool = c_bool(False)
        ret = camera.MV_CC_GetBoolValue("AcquisitionFrameRateEnable", byref(stBool))
        if ret != 0:
            print("get AcquisitionFrameRateEnable fail! ret[0x%x]" % ret)
            return False

        # ch:设置触发模式为off | en:Set trigger mode as off
        ret = camera.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
        if ret != 0:
            print("set trigger mode fail! ret[0x%x]" % ret)
            return False

        # ch:获取图像像素 | en:Get the pixelFormat of the image
        stEnumValue = MVCC_ENUMVALUE()
        memset(byref(stEnumValue), 0, sizeof(MVCC_ENUMVALUE))
        ret = camera.MV_CC_GetEnumValue("PixelFormat", stEnumValue)
        if ret != 0:
            print("get PixelFormat fail! nRet [0x%x]" % ret)
            return False

        # ch:获取数据包大小 | en:Get payload size
        stParam = MVCC_INTVALUE()
        memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))

        ret = camera.MV_CC_GetIntValue("PayloadSize", stParam)
        if ret != 0:
            print("get payload size fail! ret[0x%x]" % ret)
            return False
        nPayloadSize = stParam.nCurValue

        if None == data_buf:
            data_buf = (c_ubyte * nPayloadSize)()

        return camera
    except Exception as error:
        print("ERROR Hikvision camera connection: {}".format(error))
    return False

def disconnect_camera():
    return

def image_processing_thread(image_queue, rect_queue, image_index_value):
    algorithm = Algorithm()
    while True:
        time = TimeControl.time()
        try:
            image_index, sourceImage  = image_queue.get_nowait()
        except queue.Empty:
            cv.waitKey(1)
            continue
        else:
            rects = []
            temp_count = 0
            # show_image(sourceImage)
            algorithm_results = algorithm.execute(sourceImage=sourceImage)

            image_show = algorithm.imageList[0]

            for result in algorithm_results:
                if result.methodName == MethodList.findContour.value:
                    if result.passed:
                        temp_count = len(result.contourList)
                        rects = rects + result.detectAreaList
                elif result.methodName == MethodList.matchingTemplate.value:
                    if result.passed:
                        rects = rects + result.detectAreaList
                        shape = (rects[0][2] - rects[0][0], rects[0][3] - rects[0][1])

            print(f"temp_count = {temp_count}")
            while True:
                with image_index_value.get_lock():
                    if image_index_value.value == image_index:
                        rect_queue.put((rects, image_show))
                        image_index_value.value += 1
                        print(image_index)
                        break
                    cv.waitKey(2)
            # image_show_queue.put(image_show)
            print(f"Algorithm execute time = {TimeControl.time() - time}")
            cv.waitKey(1)

def counting_thread(rect_queue):
    cv.namedWindow(str("Image 1"), 0)
    cv.resizeWindow(str("Image 1"), 500, 500)

    object_list = []
    count = 0
    bip_count = 0
    mark = False
    shape = (20, 20)
    image_show = None

    currentModel: ModelParameter = get_current_model()

    ct = CentroidTracker(maxDisappeared=currentModel.cic_max_disappeared, maxDistance=currentModel.cic_max_distance)

    def check_object_existed(object_id):
        for _object in object_list:
            if object_id == _object.object_id:
                return _object

        return None

    while True:
        time = TimeControl.time()
        count = check_running(count=count)
        if count < 0:
            exit_app()
        try:
            rects, image_show = rect_queue.get_nowait()
            # image_show = image_show_queue.get_nowait()
        except queue.Empty:
            cv.waitKey(1)
            continue
        else:
            rects = non_max_suppression(np.array(rects))
            objects = ct.update(rects)

            mark = not mark
            # loop over the tracked objects

            if len(image_show.shape) < 3:
                image_show = ImageProcess.processCvtColor(image_show, cv.COLOR_GRAY2BGR)

            cv.line(image_show, pt1=(currentModel.cic_counting_boundary, 0),
                    pt2=(currentModel.cic_counting_boundary, image_show.shape[1]),
                    color=(0, 255, 0),
                    thickness=2,
                    lineType=cv.LINE_AA)
            cv.line(image_show, pt1=(currentModel.cic_out_boundary, 0),
                    pt2=(currentModel.cic_out_boundary, image_show.shape[1]),
                    color=(0, 0, 255),
                    thickness=2,
                    lineType=cv.LINE_AA)

            for (objectID, centroid) in objects.items():
                # draw both the ID of the object and the centroid of the
                # object on the output frame
                text = "{}".format(objectID)
                cv.putText(image_show, text, (centroid[0] - 10, centroid[1] - 10),
                           cv.FONT_HERSHEY_SIMPLEX,
                           fontScale=0.3,
                           color=(0, 255, 0),
                           thickness=1,
                           lineType=cv.LINE_AA)
                # cv.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
                cv.rectangle(image_show, pt1=(int(centroid[0] - shape[0] / 2), int(centroid[1] - shape[1] / 2)),
                             pt2=(int(centroid[0] + shape[0] / 2), int(centroid[1] + shape[1] / 2)),
                             color=(0, 255, 0),
                             thickness=1,
                             lineType=cv.LINE_AA)

                object_existed = check_object_existed(objectID)
                if object_existed is None:
                    object_existed = Trackable_Object(objectID, centroid,
                                                      currentModel.cic_in_boundary,
                                                      currentModel.cic_counting_boundary,
                                                      out_boundary=currentModel.cic_out_boundary,
                                                      mark=mark)

                if object_existed.updateCenter(center=centroid, mark=mark):
                    count += 1

                    bip_count += 1

                    if bip_count >= abs(currentModel.cic_bip) and currentModel.cic_bip != 0:
                        if currentModel.cic_bip > 0:
                            count += 1
                        else:
                            count -= 1
                        bip_count = 0

                object_list.append(object_existed)
            object_list = [_object for _object in object_list if _object.mark == mark]

        cv.putText(image_show, f"Count = {count}", (5, image_show.shape[0] - 5),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)
        show_image(image_show)
        print(f"Counting Time = {TimeControl.time() - time}")
        cv.waitKey(1)

def get_current_model():
    modelManager = ModelManager()
    return modelManager.getCurrentModel()


def take_pic_thread(image_queue):
    global camera
    global nPayloadSize
    global data_buf
    algorithm = Algorithm()
    image_index = 0
    time = TimeControl.time()
    # ch:开始取流 | en:Start grab image
    camera = connect_camera()
    ret = camera.MV_CC_StartGrabbing()
    if ret != 0:
        print("start grabbing fail! ret[0x%x]" % ret)
        return
    data_buf = (c_ubyte * nPayloadSize)()
    numArray = None
    img_buff = None
    try:
        stFrameInfo = MV_FRAME_OUT_INFO_EX()
        memset(byref(stFrameInfo), 0, sizeof(stFrameInfo))
        while True:
            time = TimeControl.time()
            ret = camera.MV_CC_GetOneFrameTimeout(byref(data_buf), nPayloadSize, stFrameInfo, 1000)

            if ret == 0:
                n_save_image_size = stFrameInfo.nWidth * stFrameInfo.nHeight * 3 + 2048
                if img_buff is None:
                    img_buff = (c_ubyte * n_save_image_size)()

                # Convert pixel structure assignment
                stConvertParam = MV_CC_PIXEL_CONVERT_PARAM()
                memset(byref(stConvertParam), 0, sizeof(stConvertParam))
                stConvertParam.nWidth = stFrameInfo.nWidth
                stConvertParam.nHeight = stFrameInfo.nHeight
                stConvertParam.pSrcData = data_buf
                stConvertParam.nSrcDataLen = stFrameInfo.nFrameLen
                stConvertParam.enSrcPixelType = stFrameInfo.enPixelType

                if PixelType_Gvsp_Mono8 == stFrameInfo.enPixelType:
                    numArray = mono_numpy(data_buf, stFrameInfo.nWidth,
                                                    stFrameInfo.nHeight)

                # RGB直接显示
                elif PixelType_Gvsp_RGB8_Packed == stFrameInfo.enPixelType:
                    numArray = color_numpy(data_buf, stFrameInfo.nWidth,
                                                     stFrameInfo.nHeight)
                # If it is black and white and non-Mono8, convert to Mono8
                elif is_mono_data(stFrameInfo.enPixelType):
                    nConvertSize = stFrameInfo.nWidth * stFrameInfo.nHeight
                    stConvertParam.enDstPixelType = PixelType_Gvsp_Mono8
                    stConvertParam.pDstBuffer = (c_ubyte * nConvertSize)()
                    stConvertParam.nDstBufferSize = nConvertSize
                    ret = camera.MV_CC_ConvertPixelType(stConvertParam)
                    if ret != 0:
                        # mainWindow.runningTab.insertLog('ERROR HIK convert pixel fail!')
                        camera.MV_CC_StopGrabbing()
                        return False, None
                    cdll.msvcrt.memcpy(byref(img_buff), stConvertParam.pDstBuffer, nConvertSize)
                    numArray = mono_numpy(img_buff, stFrameInfo.nWidth,
                                                    stFrameInfo.nHeight)

                elif is_color_data(stFrameInfo.enPixelType):
                    nConvertSize = stFrameInfo.nWidth * stFrameInfo.nHeight * 3
                    stConvertParam.enDstPixelType = PixelType_Gvsp_RGB8_Packed
                    stConvertParam.pDstBuffer = (c_ubyte * nConvertSize)()
                    stConvertParam.nDstBufferSize = nConvertSize
                    ret = camera.MV_CC_ConvertPixelType(stConvertParam)
                    if ret != 0:
                        # mainWindow.runningTab.insertLog('ERROR HIK convert pixel fail!')
                        camera.MV_CC_StopGrabbing()
                        return False, None
                    cdll.msvcrt.memcpy(byref(img_buff), stConvertParam.pDstBuffer, nConvertSize)
                    numArray = color_numpy(img_buff, stFrameInfo.nWidth,
                                                     stFrameInfo.nHeight)

            image_queue.put((image_index, numArray))
            cv.waitKey(1)
            print("hik take pic time: {}".format(TimeControl.time() - time))
            image_index += 1
    except Exception as error:
        # mainWindow.runningTab.insertLog("ERROR Hik Vision Take pic: {}".format(error))
        print("error: unable to start thread")
        # ch:停止取流 | en:Stop grab image
        ret = camera.MV_CC_StopGrabbing()
        if ret != 0:
            print("stop grabbing fail! ret[0x%x]" % ret)
            del data_buf
        return

    # mainWindow.runningTab.insertLog("hik take pic time: {}".format(TimeControl.time() - time))
    # ch:停止取流 | en:Stop grab image
    ret = camera.MV_CC_StopGrabbing()
    if ret != 0:
        print("stop grabbing fail! ret[0x%x]" % ret)
        del data_buf
    return


def show_image(source_image):
    cv.resizeWindow(str("Image 1"), 500, 500)
    cv.imshow(str("Image 1"), source_image)
    cv.waitKey(1)


def counting_execute():
    return

def is_color_data(enGvspPixelType):
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

def is_mono_data(enGvspPixelType):
    if PixelType_Gvsp_Mono8 == enGvspPixelType or PixelType_Gvsp_Mono10 == enGvspPixelType \
        or PixelType_Gvsp_Mono10_Packed == enGvspPixelType or PixelType_Gvsp_Mono12 == enGvspPixelType \
        or PixelType_Gvsp_Mono12_Packed == enGvspPixelType:
        return True
    else:
        return False


def color_numpy(data, nWidth, nHeight):
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

def mono_numpy(data, nWidth, nHeight):
    data_ = np.frombuffer(data, count=int(nWidth * nHeight), dtype=np.uint8, offset=0)
    data_mono_arr = data_.reshape(nHeight, nWidth)
    numArray = np.zeros([nHeight, nWidth, 1],"uint8")
    numArray[:, :, 0] = data_mono_arr
    return numArray


class Algorithm:
    imageList = []
    filePath = "./config/Algorithm"
    # currentName = ""
    # try:
    #     name_filePath = filePath + "/index.txt"
    #     file = TextFile(name_filePath)
    #     file.readFile()
    #     currentName = file.dataList[0]
    # except:
    #     pass
    # filePath = f"{filePath}/{currentName}"

    currentModel:ModelParameter = get_current_model()
    filePath = f"{filePath}/{currentModel.cic_find_object_algorithm}"

    def __init__(self):
        self.maxStep = 30
        self.algorithmParameter = AlgorithmParameter()
        self.get()
    def get(self):
        dataFilePath = self.filePath + "/data.json"
        dataFile = JsonFile(dataFilePath)
        jsonData = dataFile.readFile()

        if jsonData is None:
            return
        try:
            self.algorithmParameter = jsonpickle.decode(jsonData)
            self.algorithmParameter.steps = []
            for jsonStep in self.algorithmParameter.jsonSteps:
                step: StepParameter = jsonpickle.decode(jsonStep)
                step.makeStandard()
                self.algorithmParameter.steps.append(step)

            for index in range(self.maxStep):
                self.imageList.append(None)
            print(len(self.algorithmParameter.steps))
        except Exception as error:
            PathFileControl.deleteFolder(self.filePath)
            print("ERROR Get Algorithm parameter: {}".format(error))

    def execute(self, sourceImage):
        resultList = []
        for index in range(self.maxStep + 1):
            step: StepParameter = self.algorithmParameter.steps[index]

            if not step.activeFlag:
                continue

            if step.workingArea is None:
                workingArea = (0, 0, sourceImage.shape[1], sourceImage.shape[0])
            else:
                workingArea = step.workingArea
            basePoint = [0, 0]
            # Resize
            if step.stepAlgorithmName == MethodList.resize.value:
                try:
                    if step.rs_ratio:
                        resizeImage = cv.resize(sourceImage, dsize=(0, 0), fx=step.rs_fX, fy=step.rs_fY)
                    else:
                        resizeImage = cv.resize(sourceImage, dsize=(step.rs_sizeX, step.rs_sizeY))
                    self.imageList[index] = resizeImage.copy()
                except Exception as error:
                    text = f"ERROR Algorithm {self.algorithmParameter.name}. Step {step.stepId} Check the parameter Detail: {error}"
            elif step.stepAlgorithmName == MethodList.matchingTemplate.value:
                sourceImage = self.imageList[step.resourceIndex[0]]
                templatePath = f"{self.filePath}/imageTemplate_{step.templateName}.png"
                template = cv.imdecode(np.fromfile(templatePath, dtype=np.uint8), cv.IMREAD_GRAYSCALE)

                matchingResultList = ImageProcess.processTemplateMatching(sourceImage, template=template,
                                                                          minMatchingValue=float(step.minMatchingValue),
                                                                          multiMatchingFlag=step.multiMatchingFlag)
                imageShow = sourceImage.copy()
                for result in matchingResultList:
                    resultList.append(AlgorithmResult(stepId=index,
                                                      methodName=step.stepAlgorithmName,
                                                      workingArea=workingArea, basePoint=basePoint,
                                                      point=(int((result[0] + result[2]) / 2),
                                                             int((result[1] + result[3]) / 2)),
                                                      detectAreaList=[
                                                          (workingArea[0] + result[0], workingArea[1] + result[1],
                                                           workingArea[0] + result[2], workingArea[1] + result[3])],
                                                      passed=True,
                                                      drawImage=imageShow,
                                                      value=result[4]))

                if len(matchingResultList) < 1:

                    resultList.append(AlgorithmResult(methodName=step.stepAlgorithmName, stepId=index,
                                                      workingArea=workingArea, basePoint=basePoint,
                                                      passed=False, drawImage=imageShow))
                else:
                    imageResult = sourceImage[matchingResultList[0][1]: matchingResultList[0][3],
                                  matchingResultList[0][0]: matchingResultList[0][2]]
                    self.imageList[index] = imageResult.copy()

        return resultList

def check_running(count):
    file = TextFile("./resource/control.txt")
    file.readFile()
    try:
        control = file.dataList[0]
        if control == "on":
            return count
        elif control == "reset":
            save_count(count)
            file.dataList = ["on"]
            file.saveFile()
            return 0
        else:
            save_count(count)
            return -1
    except:
        return -1

def save_count(count):
    date_path = f"data/Coconut_counting/{TimeControl.y_m_dFormat()}.csv"
    file_path = CsvFile(date_path)
    data = [f"{TimeControl.ymd_HMSFormat()}", f"{count}"]
    file_path.appendData(data)

def exit_app():
    cv.destroyAllWindows()
    sys.exit(0)

if __name__ == '__main__':
    # connect_camera()
    freeze_support()
    imageQueue = Queue(maxsize=10)
    rectQueue = Queue(maxsize=10)
    imageShowQueue = Queue(maxsize=10)
    image_index_value = Value("i", 0)
    process_list = [Process(target=take_pic_thread, args=(imageQueue,)),
                    Process(target=image_processing_thread, args=(imageQueue, rectQueue, image_index_value)),
                    Process(target=image_processing_thread, args=(imageQueue, rectQueue, image_index_value)),
                    Process(target=image_processing_thread, args=(imageQueue, rectQueue, image_index_value)),
                    Process(target=counting_thread, args=(rectQueue,))]

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()
    cv.destroyAllWindows()

