import threading
from Modules.ModelSetting.ModelParameter import ModelParameter
from ImageProcess.Algorithm.Algorithm import Algorithm, AlgorithmResult
import cv2 as cv
import numpy as np
from ImageProcess.Algorithm.MethodList import MethodList
from tkinter import messagebox
from ImageProcess import ImageProcess
from Connection.Camera import Camera
from CommonAssit import TimeControl, PathFileControl, Color
from CommonAssit.DDK_CONSTANT import *
import glob
import os
import threading
import enum
from  CommonAssit.CommunicationReceiveAnalyze import DDK_parameter
from View.Running.DDK.DDK_Result_Frame import DDK_Result_Parameter

# from multiprocessing import shared_memory
# import numpy as np

class DDK_Analysis_State(enum.Enum):
    trigger_busy = "trigger_busy"
    trigger_ready = "trigger_ready"
    image_ready = "image_ready"
    image_not_ready = "image_not_ready"
    image_again = "image_again"
    image_failed = "image_failed"
    processing = "processing"
    process_done = "process_done"
    request_reset = "request_reset"
    request_moving = "request_moving"

class Message_List(enum.Enum):
    go_to = 0
    reset_process = 1
    reset_done = 2
    motion_ready = 3
    trigger_busy = 4
    trigger_ready = 5
    trigger = 6
    image_not_ready = 7
    image_false = 8
    image_ready = 9
    get_result = 10
    processing = 11
    process_done = 12
    request_moving = 13
    moving_done = 14

class Error_Code_List(enum.Enum):
    unknown_error = 0

class DDK_Inspection:

    step_algorithm_list: [Algorithm] = []
    currentModel: ModelParameter = None
    camera: Camera = None

    analysis_state = DDK_Analysis_State.trigger_ready
    ddk_parameter: DDK_parameter = None
    take_picture_flag = False
    hard_trigger_mode = False
    mode_running = "sw_trigger"
    ddk_result_parameter = DDK_Result_Parameter()
    current_step = 0
    sharedImage = None
    existing_shm = None
    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow
        self.ddk_parameter = DDK_parameter()
        for i in range(20):
            self.step_algorithm_list.append(None)


    def updateModel(self):
        try:
            self.currentModel = self.mainWindow.modelSettingTab.modelManager.getCurrentModel()
            for i, algorithmName in enumerate(self.currentModel.ddk_algorithm_list):
                self.step_algorithm_list[i] = self.mainWindow.algorithmManager.getAlgorithmWithName(algorithmName)
            self.camera = self.mainWindow.workingThread.cameraManager.currentCamera
            if not self.camera.connect():
                return False

            if not self.mainWindow.workingThread.connectionManager.connect():
                return False
            image = cv.imdecode(np.fromfile(r"./resource/cancel_button.png", dtype=np.uint8), cv.IMREAD_COLOR)
            self.workingThread(image)
            return True
        except Exception as error:
            self.mainWindow.showError(f"ERROR update model {error}")
            return False

    def start(self):
        if self.updateModel():
            # self.workingThread(None)
            if self.mode_running == "test":
                self.test_threading()
            elif self.mode_running == "hard_trigger":
            # if self.hard_trigger_mode:
                self.camera.baslerHardwareTrigger(process_cmd=self.workingThread)
            # self.test_threading()
            return True
        else:
            return False

    def start_trigger_mode_if_needed(self):
        self.start_trigger_mode_if_needed_thread()

    def start_trigger_mode_if_needed_thread(self):
        TimeControl.sleep(20)
        self.ddk_parameter.client_capture_result = NOT_YET
        self.ddk_parameter.client_vision_ready_flag = NOT_YET

        if self.mode_running == "sw_trigger":
            ret, image = self.camera.takePicture(False)
            if ret:
                self.ddk_parameter.client_capture_result = CAPTURE_PASSED
                image_process_thread = threading.Thread(target=self.image_process_thread, args=(image,))
                image_process_thread.start()
            else:
                self.ddk_parameter.client_capture_result = CAPTURE_FAILED
                self.ddk_parameter.client_vision_ready_flag = READY
                self.ddk_parameter.client_step_finish = FINISH

    def set_current_step(self, current_station, current_step):
        self.ddk_parameter.client_process_result = PASSED
        self.ddk_parameter.station = current_station
        self.ddk_parameter.step = current_step

    def request_moving(self, step):
        self.ddk_parameter.client_manual_go = step
        # self.analysis_state = DDK_Analysis_State.request_moving
        self.ddk_parameter.client_auto_request = MANUAL
        self.ddk_parameter.client_vision_ready_flag = READY

    def request_reset(self):
        self.current_step = 0
        self.ddk_parameter.step = 1
        self.ddk_parameter.client_vision_ready_flag = READY
        self.ddk_parameter.client_capture_result = NOT_YET
        self.ddk_parameter.client_process_result = FAILED
        self.ddk_parameter.client_step_tact_time = 0
        self.ddk_parameter.client_sw_error_code = NONE
        self.ddk_parameter.client_image_error_code = NONE
        self.ddk_parameter.client_request_reset = REQUEST
        self.ddk_parameter.client_auto_request = NONE
        self.ddk_parameter.client_step_finish = NOT_YET
        self.ddk_parameter.client_manual_go = AUTO

    def workingThread(self, image):
        image_process_thread = threading.Thread(target=self.image_process_thread, args=(image,))
        image_process_thread.start()

    def test_threading(self):
        image_process_thread = threading.Thread(target=self.test_thresh, args=())
        image_process_thread.start()

    def test_thresh(self):
        folder_paths = [os.path.join(r"D:\Duc\Code\Vision\dist\save_images", name) for name in os.listdir(r"D:\Duc\Code\Vision\dist\save_images") if os.path.isdir(os.path.join(r"D:\Duc\Code\Vision\dist\save_images", name))]
        image_paths = []
        for folder_path in folder_paths:
            image_paths += glob.glob(f"{folder_path}\\*png")
        # image_paths += glob.glob("D:\\Duc\Code\\tensorflow1\models\\research\\object_detection\\images\\DDK_Station1_06062021\\test\\*jpg")

        image_paths = glob.glob(r"D:\Duc\Code\Vision\dist\save_images\Station_1\block break 2\\*png")
        idx = 0
        while self.mainWindow.workingThread.runningFlag:
            if self.take_picture_flag:
                self.take_picture_flag = False
                image = cv.imdecode(np.fromfile(image_paths[idx], dtype=np.uint8), cv.IMREAD_COLOR)
                self.ddk_parameter.step = idx+1
                self.image_process_thread(image)

                if idx >= len(image_paths) - 1:
                    idx = 0
                else:
                    idx+=1
            TimeControl.sleep(1)
        # self.current_step = -1
        # for step, image_path in enumerate(image_paths):
        #     image = cv.imread(image_path)
        #     if self.current_step < 16:
        #         self.current_step +=1
        #     else:
        #         self.current_step = 0
        #     if image is None or not self.mainWindow.workingThread.runningFlag:
        #         break
        #     else:
        #         self.image_process_thread(image)
        #
        #     TimeControl.sleep(10)

    def image_process_thread(self, image):
        # self.analysis_state = DDK_Analysis_State.image_ready
        self.ddk_parameter.client_process_result = PASSED
        if image is None:
            return
        image = ImageProcess.rotateImage90Clockwise(image)
        if self.ddk_parameter.step == 1:
            self.reset_result_value()
            self.mainWindow.runningTab.ddk_process_image_frame.reset_product_circle()
        tact_time_start = TimeControl.time()
        showImage = image.copy()
        try:
            ret, result_list, text = self.step_algorithm_list[self.ddk_parameter.step-1].executeAlgorithm(image)
            ignore_area_list = []
            result: AlgorithmResult
            if ret:
                distance_flag = False
                for result in result_list:
                    if result.methodName == MethodList.distance_point_to_point.value or\
                        result.methodName == MethodList.distance_point_to_line.value or\
                            result.methodName == MethodList.angle_from_2_lines.value:
                        distance_flag = True

                    if result.methodName == MethodList.ignore_areas.value:
                        ignore_area_list = result.ignore_area_list
                    elif result.methodName == MethodList.reference_edge_corner.value:
                        showImage = self.step_algorithm_list[self.ddk_parameter.step-1].imageList[result.stepId]

                for result in result_list:
                    if result.methodName == MethodList.ddk_scratch_dl.value:
                        cv.rectangle(showImage, pt1=(result.workingArea[0] + result.basePoint[0],
                                                     result.workingArea[1] + result.basePoint[1]),
                                     pt2=(result.workingArea[2] + result.basePoint[0],
                                          result.workingArea[3] + result.basePoint[1]),
                                     color=Color.bgrMagenta(),
                                     thickness=5,
                                     lineType=cv.LINE_AA)
                        if not result.passed:
                            for detectArea in result.detectAreaList:
                                if not self.check_ignore(ignore_area_list,
                                                         (detectArea[0]+result.workingArea[0] + result.basePoint[0],
                                                                 detectArea[1]+result.workingArea[1] + result.basePoint[1],
                                                          detectArea[2]+result.workingArea[0] + result.basePoint[0],
                                                      detectArea[3]+result.workingArea[1] + result.basePoint[1])):
                                    cv.rectangle(showImage, pt1=(detectArea[0]+result.workingArea[0] + result.basePoint[0],
                                                                 detectArea[1]+result.workingArea[1] + result.basePoint[1]),
                                                 pt2=(detectArea[2]+result.workingArea[0] + result.basePoint[0],
                                                      detectArea[3]+result.workingArea[1] + result.basePoint[1]),
                                                 color=(0, 0, 255),
                                                 thickness=5,
                                                 lineType=cv.LINE_AA)
                                    self.ddk_parameter.client_process_result = FAILED

                    if result.methodName == MethodList.findContour.value:
                        if not distance_flag:
                            color = (0, 255, 0) if result.passed else (0, 0, 255)
                            cv.rectangle(showImage, pt1=(result.workingArea[0] + result.basePoint[0], result.workingArea[1] + result.basePoint[1]),
                                         pt2=(result.workingArea[2]+ result.basePoint[0], result.workingArea[3] + result.basePoint[1]), color=color,
                                         thickness= self.camera.parameter.textThickness, lineType=cv.LINE_AA)
                            if not result.passed: self.ddk_parameter.client_process_result = FAILED

                    if result.methodName == MethodList.distance_point_to_point.value:
                        if not result.passed:
                            self.ddk_parameter.client_process_result = FAILED
                            color = (0, 0, 255)
                            real_point1, real_point2 = result.pointList
                            cv.circle(showImage, center=real_point1, radius=self.camera.parameter.textThickness * 5,
                                      color=(255, 255, 0), thickness=-1, lineType=cv.LINE_AA)
                            cv.circle(showImage, center=real_point2, radius=self.camera.parameter.textThickness * 5,
                                      color=(255, 255, 0), thickness=-1, lineType=cv.LINE_AA)
                            cv.line(showImage, real_point1, real_point2, color=color,
                                    thickness=self.camera.parameter.textThickness, lineType=cv.LINE_AA)
                        else:
                            color = (0, 255, 0)

                    if result.methodName == MethodList.threshold.value:
                        cv.rectangle(showImage, pt1=(result.workingArea[0] + result.basePoint[0],
                                                     result.workingArea[1] + result.basePoint[1]),
                                     pt2=(result.workingArea[2] + result.basePoint[0],
                                          result.workingArea[3] + result.basePoint[1]),
                                     color=Color.bgrMagenta(),
                                     thickness=5,
                                     lineType=cv.LINE_AA)
                    if result.methodName == MethodList.distance_point_to_line.value:
                        if not result.passed:
                            self.ddk_parameter.client_process_result = FAILED
                            color = (0, 0, 255)
                            point, project_point = result.pointList
                            line_point1, line_point2 = result.line
                            # draw line
                            cv.circle(showImage, center=point, radius=self.camera.parameter.textThickness * 5,
                                      color=(255, 255, 0), thickness=-1, lineType=cv.LINE_AA)
                            cv.circle(showImage, center=line_point1, radius=self.camera.parameter.textThickness * 5,
                                      color=(255, 255, 0), thickness=-1, lineType=cv.LINE_AA)
                            cv.circle(showImage, center=line_point2, radius=self.camera.parameter.textThickness * 5,
                                      color=(255, 255, 0), thickness=-1, lineType=cv.LINE_AA)
                            cv.line(showImage, line_point1, line_point2, color=color,
                                    thickness=self.camera.parameter.textThickness, lineType=cv.LINE_AA)

                            cv.line(showImage, point, project_point, color=color,
                                    thickness=self.camera.parameter.textThickness, lineType=cv.LINE_AA)
                        else:
                            color = (0, 255, 0)

                    if result.methodName == MethodList.angle_from_2_lines.value:
                        if not result.passed:
                            self.ddk_parameter.client_process_result = FAILED
                            color = (0, 0, 255)
                            line1, line2 = result.lineList
                            if result.angle != 0 and result.angle != 360:
                                intersection_point = ImageProcess.get_intersect_from_2_lines(line1=line1, line2=line2)
                                intersection_point = (int(intersection_point[0]), int(intersection_point[1]))
                                cv.line(showImage, line1[0], intersection_point, color=color,
                                        thickness=self.camera.parameter.textThickness, lineType=cv.LINE_AA)
                                cv.line(showImage, line2[0], intersection_point, color=color,
                                        thickness=self.camera.parameter.textThickness, lineType=cv.LINE_AA)
                            else:
                                cv.line(showImage, line1[0], line1[1], color=color,
                                        thickness=self.camera.parameter.textThickness, lineType=cv.LINE_AA)
                                cv.line(showImage, line2[0], line2[1], color=color,
                                        thickness=self.camera.parameter.textThickness, lineType=cv.LINE_AA)
                        else:
                            color = (0, 255, 0)


            else:
                self.ddk_parameter.client_process_result = FAILED
        except Exception as error:
            self.mainWindow.runningTab.insertLog(f"ERROR {error}")
            self.ddk_parameter.client_process_result = FAILED

        # Add image to the list and show
        print(f"process step = {self.ddk_parameter.step}")
        self.mainWindow.runningTab.ddk_process_image_frame.add_step_image(step=self.ddk_parameter.step,
                                                                          image=showImage,
                                                                          state=STATE_OK if self.ddk_parameter.client_process_result else STATE_NG)


        # setup parameter to show in frame
        if self.ddk_parameter.client_process_result == PASSED:
            self.ddk_result_parameter.step_passed = True
            self.mainWindow.showImageOKLabel()
        else:
            self.ddk_result_parameter.step_passed = False
            self.ddk_result_parameter.product_passed = False
            self.mainWindow.showImageNGLabel()

        self.ddk_result_parameter.current_station = self.ddk_parameter.station
        self.ddk_result_parameter.current_step = self.ddk_parameter.step
        self.ddk_result_parameter.step_process_time = self.ddk_parameter.client_step_tact_time
        self.ddk_result_parameter.product_process_time += self.ddk_parameter.client_step_tact_time
        self.mainWindow.runningTab.resultTab.ddk_result_frame.setValue(self.ddk_result_parameter)

        # setup parameter to send to server
        self.ddk_parameter.client_step_tact_time = TimeControl.time() - tact_time_start
        self.ddk_parameter.client_step_finish = FINISH
        self.ddk_parameter.client_vision_ready_flag = READY

        # self.mainWindow.showImage(showImage, title=f"Camera of DDK Station {self.ddk_parameter.station}")
        self.save_ddk_image(original_image=image, showImage=showImage,
                            name=self.ddk_parameter.real_time, type=self.ddk_parameter.client_process_result)


    def check_ignore(self, ignore_area_list, location):
        if len(location) > 2:
            center = (int((location[0] + location[2])/2), int((location[1] + location[3])/2))
        else:
            center = location

        for area_id, (ignore_area, area_type) in enumerate(ignore_area_list):
            if area_type == "rectangle":
                if ignore_area[0] < center[0] < ignore_area[2] and ignore_area[1] < center[1] < ignore_area[3]:
                    return True
            elif area_type == "circle":
                if ImageProcess.calculateDistanceBy2Points(ignore_area[0], center) <= ignore_area[1]:
                    return True
        return False

    def reset_result_value(self):
        if self.ddk_result_parameter.product_passed:
            self.ddk_result_parameter.total_passed += 1
        else:
            self.ddk_result_parameter.total_NG += 1
        self.ddk_result_parameter.total += 1
        self.ddk_result_parameter.step_passed = True
        self.ddk_result_parameter.product_passed = True
        self.ddk_result_parameter.step_process_time = 0
        self.ddk_result_parameter.product_process_time = 0


    def save_ddk_image(self, original_image, showImage, name, type):
        if type == PASSED and self.currentModel.save_ok_image[0]:
            try:
                datePath = f"{self.currentModel.save_ok_image[2]}/{TimeControl.y_m_dFormat()}"
                PathFileControl.generatePath(datePath)
                image_path = f"{datePath}/{name}.{self.currentModel.save_ok_image[1]}"
                if self.currentModel.save_ok_image[3] == "Draw":
                    cv.imencode(f".{self.currentModel.save_ok_image[1]}", showImage)[1].tofile(image_path)
                    # cv.imwrite(image_path, showImage)
                else:
                    cv.imencode(f".{self.currentModel.save_ok_image[1]}", original_image)[1].tofile(image_path)
                    # cv.imwrite(image_path, original_image)
            except Exception as error:
                self.mainWindow.runningTab.insertLog(f"ERROR save DDK image {error}")
        elif type == FAILED and self.currentModel.save_ng_image[0]:
            try:
                datePath = f"{self.currentModel.save_ng_image[2]}/{TimeControl.y_m_dFormat()}"
                PathFileControl.generatePath(datePath)
                image_path = f"{datePath}/{name}.{self.currentModel.save_ng_image[1]}"
                if self.currentModel.save_ng_image[3] == "Draw":
                    cv.imencode(f".{self.currentModel.save_ng_image[1]}", showImage)[1].tofile(image_path)
                    # cv.imwrite(image_path, showImage)
                else:
                    cv.imencode(f".{self.currentModel.save_ng_image[1]}", original_image)[1].tofile(image_path)
                    # cv.imwrite(image_path, original_image)
            except Exception as error:
                self.mainWindow.runningTab.insertLog(f"ERROR save DDK image {error}")


