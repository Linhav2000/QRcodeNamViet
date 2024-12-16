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
import imutils
from imutils.video import VideoStream
from Modules.ObjectTracking.CentroidTracker import CentroidTracker
from Modules.ObjectTracking.Trackable_Object import Trackable_Object
from Modules.Camera.CameraParameter import CameraBrand
from imutils.object_detection import non_max_suppression
import threading
import os

class Counting_In_Conveyor:
    currentModel: ModelParameter = None
    finding_object_algorithm: Algorithm = None
    # lock = False
    count = 0
    bip_count = 0
    mark = False

    # initialize our centroid tracker and frame dimensions
    ct = CentroidTracker(maxDisappeared=2)
    (H, W) = (None, None)
    # load our serialized model from disk
    print("[INFO] loading model...")
    # net = cv.dnn.readNetFromCaffe(args["prototxt"], args["model"])
    # initialize the video stream and allow the camera sensor to warmup
    print("[INFO] starting video stream...")
    # vs = VideoStream(src=0).start()
    TimeControl.sleep(2)

    object_list = []

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow
        self.generate_file_data()
        self.lock = threading.Lock()

    def generate_file_data(self):
        data_path = "./data"
        machine_path = f"{data_path}/Coconut_counting"
        date_path = f"{machine_path}/{TimeControl.y_m_dFormat()}"

        PathFileControl.generatePath(data_path)
        PathFileControl.generatePath(machine_path)
        PathFileControl.generatePath(date_path)


    def updateModel(self):
        self.currentModel = self.mainWindow.modelSettingTab.modelManager.getCurrentModel()
        self.finding_object_algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName(self.currentModel.cic_find_object_algorithm)
        self.ct = CentroidTracker(maxDisappeared=self.currentModel.cic_max_disappeared, maxDistance=self.currentModel.cic_max_distance)

    def checkReady(self):
        self.updateModel()
        ret = True
        if self.finding_object_algorithm is None:
            messagebox.showerror("Algorithm setting", "Please choose find object algorithm for model!")
        self.mainWindow.showStateLabel()

        # if not self.mainWindow.workingThread.cameraManager.currentCamera.connect():
        #     messagebox.showerror("Camera connection", "Please check the CAMERA connection!")
        #     ret = False
        return ret

    def do_process(self, sourceImage=None):
        if sourceImage is None:
            # if self.mainWindow.workingThread.cameraManager.currentCamera.parameter.brand == CameraBrand.basler:
            #     self.mainWindow.workingThread.cameraManager.currentCamera.baslerGigECaptureVideo(True, process_cmd=self.count_coconut_thread)
            read_image_and_process_thread = threading.Thread(target=self.count_coconut_thread, args=())
            read_image_and_process_thread.start()
        #
        # if sourceImage is None:
        #     ret, sourceImage = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
        #     if not ret:
        #         messagebox.showerror("Camera connection", "Please check the camera connection!")
        #         self.mainWindow.runningTab.insertLog("ERROR Cannot take picture from camera!")
        #         return
        # if sourceImage is None:
        #     messagebox.showerror("Source image", "Please take image first!")
        #     return
        # self.count_coconut(sourceImage)
        # self.mainWindow.showImage(sourceImage)


    def count_coconut_thread(self, sourceImage):
        time = TimeControl.time()
        ret, resultList, text = self.finding_object_algorithm.executeAlgorithm(sourceImage)
        frame = self.finding_object_algorithm.imageList[0]
        temp_count = 0
        rects = []
        shape=(0, 0)
        for result in resultList:
            if result.methodName == MethodList.findContour.value:
                if result.passed:
                    temp_count = len(result.contourList)
                    rects = rects + result.detectAreaList
            elif result.methodName == MethodList.matchingTemplate.value:
                if result.passed:
                    rects = rects + result.detectAreaList
                    shape = (rects[0][2] - rects[0][0], rects[0][3] - rects[0][1])

        rects = non_max_suppression(np.array(rects))
        self.mainWindow.runningTab.insertLog(f"Alogrithm Done = {TimeControl.time() - time}")

        objects = self.ct.update(rects)

        self.mainWindow.runningTab.insertLog(f"Update tracking Done = {TimeControl.time() - time}")

        self.mark = not self.mark
        # loop over the tracked objects
        cv.line(frame, pt1=(self.currentModel.cic_counting_boundary, 0),
                pt2=(self.currentModel.cic_counting_boundary, frame.shape[1]),
                color=(0, 255, 0),
                thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                lineType=cv.LINE_AA)
        cv.line(frame, pt1=(self.currentModel.cic_out_boundary, 0),
                pt2=(self.currentModel.cic_out_boundary, frame.shape[1]),
                color=(0, 0, 255),
                thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                lineType=cv.LINE_AA)

        self.mainWindow.runningTab.insertLog(f"Draw Done = {TimeControl.time() - time}")

        for (objectID, centroid) in objects.items():
            # draw both the ID of the object and the centroid of the
            # object on the output frame
            text = "{}".format(objectID)
            cv.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                       cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                       color=(0, 255, 0),
                       thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                       lineType=cv.LINE_AA)
            # cv.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
            cv.rectangle(frame, pt1=(int(centroid[0] - shape[0]/2), int(centroid[1] - shape[1]/2)),
                         pt2=(int(centroid[0] + shape[0]/2), int(centroid[1] + shape[1]/2)),
                         color=(0, 255, 0),
                         thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                         lineType=cv.LINE_AA)

            object_existed = self.object_existed(objectID)
            if object_existed is None:
                object_existed = Trackable_Object(objectID, centroid,
                                                  self.currentModel.cic_in_boundary,
                                                  self.currentModel.cic_counting_boundary,
                                                  out_boundary=self.currentModel.cic_out_boundary,
                                                  mark=self.mark)

            if  object_existed.updateCenter(center=centroid, mark=self.mark):
                self.count += 1

                self.bip_count += 1

                if self.bip_count >= abs(self.currentModel.cic_bip) and self.currentModel.cic_bip != 0:
                    if self.currentModel.cic_bip > 0:
                        self.count += 1
                    else:
                        self.count -= 1
                    self.bip_count = 0


            self.object_list.append(object_existed)
        self.object_list = [_object for _object in self.object_list if _object.mark == self.mark]

        self.mainWindow.runningTab.insertLog(f"Update count done = {TimeControl.time() - time}")

        self.mainWindow.stateLabel.config(text=f"Count= {self.count}")
        self.mainWindow.runningTab.resultTab.counting_in_conveyor_result_frame.showResult(self.count)
        self.mainWindow.showImage(frame)

        self.mainWindow.runningTab.insertLog(f"Show result Done = {TimeControl.time() - time}")

    def read_image_and_process_thread(self):
        while self.mainWindow.workingThread.runningFlag:
            sourceImage = None
            time = TimeControl.time()
            for topdir, dirs, files in os.walk("./process_images", topdown=True, onerror=None, followlinks=False):
                if len(files) > 0:
                    image_file_name = f"{topdir}/{files[0]}"
                    sourceImage = cv.imdecode(np.fromfile(image_file_name, dtype=np.uint8), cv.IMREAD_COLOR)
                    PathFileControl.deleteFile(image_file_name)
                break

            if sourceImage is not None:
                self.count_coconut_thread(sourceImage)
            self.mainWindow.runningTab.insertLog(f"total image process = {TimeControl.time() - time}")
            TimeControl.sleep(1)

    def object_existed(self, object_id):
        for _object in self.object_list:
            if object_id == _object.object_id:
                return _object

        return None

    def save(self):
        date_path = f"data/Coconut_counting/{TimeControl.y_m_dFormat()}.csv"
        file_path = CsvFile(date_path)
        data = [f"{TimeControl.ymd_HMSFormat()}", f"{self.count}"]
        file_path.appendData(data)
        self.count = 0
        self.mainWindow.runningTab.resultTab.counting_in_conveyor_result_frame.showResult(self.count)
