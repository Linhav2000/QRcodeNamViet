import threading
from Modules.ModelSetting.ModelParameter import ModelParameter
from CommonAssit import Color
from tkinter import messagebox
import cv2 as cv
from ImageProcess.Algorithm.MethodList import MethodList
from ImageProcess import ImageProcess
from View.Running.SYC_Phone_Result_Frame import SYC_Phone_Result_Parameter
from ImageProcess.Algorithm.AlgorithmResult import AlgorithmResult
from CommonAssit.FileManager import *
from CommonAssit import TimeControl, PathFileControl

class SYC_Inspection:
    currentModel: ModelParameter
    algorithm_list = [None, None, None,None,None]
    syc_result_parameter = SYC_Phone_Result_Parameter()

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow

    def checkReady(self):
        self.updateModel()
        if not self.mainWindow.workingThread.cameraManager.currentCamera.ready:
            messagebox.showerror("Camera connection", "Please check the CAMERA connection!")
            if not self.mainWindow.workingThread.cameraManager.currentCamera.connect():
                return False

        for algorithm in self.algorithm_list:
            if algorithm is None:
                messagebox.showwarning("Algorithm config", "Please choose the algorithm for model!")
                return False

        return True

    def updateModel(self):
        self.mainWindow.workingThread.cameraManager.currentCamera.connect()
        self.currentModel: ModelParameter = self.mainWindow.runningTab.modelManager.getCurrentModel()
        if self.currentModel is None:
            return
        self.algorithm_list = [None, None, None, None, None]
        for i, algorithm_name in enumerate(self.currentModel.syc_algorithm_list):
            self.algorithm_list[i] = self.mainWindow.algorithmManager.getAlgorithmWithName(algorithm_name)

    def execute(self, image):
        doProcessThread = threading.Thread(target=self.doProcess, args=(image,True))
        doProcessThread.start()

    def doProcess(self, image=None, isRunningFlag = False):
        # ret, image = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
        # image = self.mainWindow.originalImage
        self.syc_result_parameter = self.mainWindow.runningTab.resultTab.syc_phone_result.syc_result_parameter
        if image is None:
            messagebox.showwarning("SYC Inspection", "Please take image first")
            return

        color = Color.cvGreen()
        imageShow = image.copy()
        self.updateModel()
        okFlag = True
        ngCount = 0

        if imageShow is not None:
            print("nhan dc tin hieu")
            try:
                imageWidth = image.shape[1]
                size = int(imageWidth / 250)

                for algorithm in self.algorithm_list:
                    ret, resultList, text = algorithm.executeAlgorithm(image=image)
                    ignore_area_list1 = []
                    matching_template_list1 = []
                    result: AlgorithmResult

                    for result in resultList:
                        if result.methodName == MethodList.ignore_areas.value:
                            ignore_area_list1 = result.ignore_area_list

                    for result in resultList:
                        if result.methodName == MethodList.matchingTemplate.value:
                            matching_template_list1 += result.detectAreaList

                    for result in resultList:
                        if result.methodName == MethodList.countContour.value or result.methodName == MethodList.findContour.value:
                            if result.contourList is None:
                                print("None")

                            else:
                                for contour_location in result.detectAreaList:
                                    check_ignore_OK = True
                                    if not self.check_ignore(ignore_area_list=ignore_area_list1,
                                                             location=[contour_location[0] + result.basePoint[0] + result.workingArea[0],
                                                                       contour_location[1] + result.basePoint[1] + result.workingArea[1],
                                                                       contour_location[2] + result.basePoint[0] + result.workingArea[0],
                                                                       contour_location[3] + result.basePoint[1] + result.workingArea[1]]):
                                        check_ignore_OK=False
                                # for contour_location in result.detectAreaList:
                                    check_matching_OK = True
                                    if not self.check_matching(matching_template=matching_template_list1,
                                                               location_matching=[contour_location[0] + result.basePoint[0] + result.workingArea[0],
                                                                       contour_location[1] + result.basePoint[1] + result.workingArea[1],
                                                                       contour_location[2] + result.basePoint[0] + result.workingArea[0],
                                                                       contour_location[3] + result.basePoint[1] + result.workingArea[1]]):
                                        color = Color.cvGreen()
                                #         # text = "Result = {}".format(len(result.contourList))
                                        ngCount = ngCount + len(contour_location)
                                        check_matching_OK = False

                                    if not check_ignore_OK and not check_matching_OK:
                                        cv.rectangle(img=imageShow,
                                                     pt1=(contour_location[0] - 30 + result.basePoint[0] + result.workingArea[0],
                                                          contour_location[1] - 20 + result.basePoint[1] + result.workingArea[1]),
                                                     pt2=(contour_location[2] + 30 + result.basePoint[0] + result.workingArea[0],
                                                          contour_location[3] + 20 + result.basePoint[1] + result.workingArea[1]),
                                                     color=(0, 255, 255),
                                                     thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                                     lineType=cv.LINE_AA)

                                        okFlag = False
                if okFlag:
                    print("OK")
                    if isRunningFlag:
                        self.mainWindow.runningTab.resultTab.syc_phone_result.update_label_ok()
                        self.syc_result_parameter.total_OK += 1
                        cv.putText(imageShow, text="Photo ID: {}".format(str(self.syc_result_parameter.total_OK)),
                                   org=(size, imageShow.shape[0] - 2 * size),
                                   fontFace=cv.FONT_HERSHEY_COMPLEX,
                                   fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                                   color=color,
                                   thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                   lineType=cv.LINE_AA)
                        if self.currentModel.syc_save_OK_image[0]:
                            self.save_image(original_image=image, showImage=imageShow, isOKImage=True)


                else:
                    print("NG")
                    if isRunningFlag:
                        self.mainWindow.runningTab.resultTab.syc_phone_result.update_label_ng()
                        self.syc_result_parameter.total_NG += 1
                        cv.putText(imageShow, text="Photo ID: {}".format(str(self.syc_result_parameter.total_NG)),
                                   org=(size, imageShow.shape[0] - 2 * size),
                                   fontFace=cv.FONT_HERSHEY_COMPLEX,
                                   fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                                   color=color,
                                   thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                   lineType=cv.LINE_AA)
                        if self.currentModel.syc_save_NG_image[0]:
                            self.save_image(original_image=image, showImage=imageShow, isOKImage=False)

            except Exception as error:
                messagebox.showwarning("Phone Check ERROR", "Cannot count\nDetail: {}".format(error))
                self.mainWindow.runningTab.insertLog("Error Phone check Cannot count: {}".format(error))

        self.mainWindow.showImage(imageShow)
        self.mainWindow.runningTab.resultTab.syc_phone_result.update_value(self.syc_result_parameter)

    def save_image(self, original_image, showImage, isOKImage):
        name = TimeControl.y_m_d_H_M_S_format()
        if isOKImage and self.currentModel.syc_save_OK_image[0]:
            try:
                datePath = f"{self.currentModel.syc_save_OK_image[2]}/{TimeControl.y_m_dFormat()}"
                PathFileControl.generatePath(datePath)
                image_path = f"{datePath}/{name}.{self.currentModel.syc_save_OK_image[1]}"
                if self.currentModel.syc_save_OK_image[3] == "Draw":
                    cv.imencode(f".{self.currentModel.syc_save_OK_image[1]}", showImage)[1].tofile(image_path)
                    # cv.imwrite(image_path, showImage)
                else:
                    cv.imencode(f".{self.currentModel.syc_save_OK_image[1]}", original_image)[1].tofile(image_path)
            except Exception as error:
                self.mainWindow.runningTab.insertLog(f"ERROR save DDK image {error}")
        elif not isOKImage and self.currentModel.syc_save_NG_image[0]:
            try:
                datePath = f"{self.currentModel.syc_save_NG_image[2]}/{TimeControl.y_m_dFormat()}"
                PathFileControl.generatePath(datePath)
                image_path = f"{datePath}/{name}.{self.currentModel.syc_save_NG_image[1]}"
                if self.currentModel.syc_save_NG_image[3] == "Draw":
                    cv.imencode(f".{self.currentModel.syc_save_NG_image[1]}", showImage)[1].tofile(image_path)
                    # cv.imwrite(image_path, showImage)
                else:
                    cv.imencode(f".{self.currentModel.syc_save_NG_image[1]}", original_image)[1].tofile(image_path)
                    # cv.imwrite(image_path, original_image)
            except Exception as error:
                self.mainWindow.runningTab.insertLog(f"ERROR save DDK image {error}")

    def check_ignore(self, ignore_area_list, location):
        if len(location) > 2:
            center = (int((location[0] + location[2]) / 2), int((location[1] + location[3]) / 2))
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

    def check_matching(self,matching_template,location_matching):
        if len(location_matching) >2:
            center1=location_matching
        else:
            center1 = (int((location_matching[0] + location_matching[2])/2),int((location_matching[1] + location_matching[3])/2))
        for matching_template in matching_template:
            if matching_template[0] < center1[0] < matching_template[2] and matching_template[1] < center1[1] < matching_template[3]:
                return True

        return False

