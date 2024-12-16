import threading
from Modules.ModelSetting.ModelParameter import ModelParameter
import cv2 as cv
from CommonAssit import TimeControl
import numpy as np
from ImageProcess.Algorithm.MethodList import MethodList
from tkinter import messagebox
from ImageProcess import ImageProcess
from ImageProcess.Algorithm.Algorithm import Algorithm, AlgorithmResult

class FPC_Inspection:
    currentModel: ModelParameter
    rotate_algorithm: Algorithm = None
    translation_algorithm: Algorithm = None
    inspection_algorithm: Algorithm = None
    position_detect_algorithm: Algorithm = None
    position_camera = None
    inspection_camera = None
    reference_binary_roi = None

    fpc_location_list = []

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow

    def updateModel(self):
        self.currentModel = self.mainWindow.modelSettingTab.modelManager.getCurrentModel()
        self.rotate_algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName(self.currentModel.fi_rotate_algorithm)
        self.translation_algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName(self.currentModel.fi_translation_algorithm)
        self.inspection_algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName(self.currentModel.fi_inspection_algorithm)
        self.position_detect_algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName(self.currentModel.fi_position_detect_algorithm)
        self.position_camera = self.mainWindow.workingThread.cameraManager.cameraList[self.currentModel.fi_position_camera]
        self.inspection_camera = self.mainWindow.workingThread.cameraManager.cameraList[self.currentModel.fi_inspection_camera]
        reference_roi = cv.imdecode(np.fromfile(self.currentModel.fi_base_roi_path, dtype=np.uint8), cv.IMREAD_COLOR)

        if reference_roi is None:
            self.reference_binary_roi = None
        else:
            ret, self.reference_binary_roi = ImageProcess.processThreshold(reference_roi, 100, 255, cv.THRESH_BINARY)

    def checkReady(self):
        self.updateModel()
        if not self.inspection_camera.connect():
            messagebox.showerror("Camera connection", "Please check the Inspection CAMERA connection!")
            return False
        if not self.inspection_camera.connect():
            messagebox.showerror("Camera connection", "Please check the Position CAMERA connection!")
            return False
        if self.rotate_algorithm is None:
            messagebox.showerror("Algorithm setting", "Please choose ROTATE ALGORITHM for model!")
            return False

        if self.translation_algorithm is None:
            messagebox.showerror("Algorithm setting", "Please choose TRANSLATION ALGORITHM for model!")
            return False

        if self.inspection_algorithm is None:
            messagebox.showerror("Algorithm setting", "Please choose INSPECTION ALGORITHM for model!")
            return False

        if self.position_detect_algorithm is None:
            messagebox.showerror("Algorithm setting", "Please choose POSITION ALGORITHM for model!")
            return False

        if self.reference_binary_roi is None:
            messagebox.showerror("Algorithm setting", "Please Get reference parameter first!")
            return False
        return True

    def start(self):
        return

    def imageProcess(self, image):
        processThread = threading.Thread(target=self.imageProcessThread, args=(image, 0))
        processThread.start()

    def detect_fpc_position(self):
        self.fpc_location_list = []
        ret, image = self.position_camera.takePicture()
        if ret:
            ret, result_list, text = self.position_detect_algorithm.executeAlgorithm(image)
            result: AlgorithmResult
            if ret:
                for result in result_list:
                    if result.methodName == MethodList.getMinAreaRect.value:
                        for center, rotation in zip(result.pointList, result.rotationList):
                            self.fpc_location_list.append((center, rotation))

    def get_pattern_position(self):
        return

    def imageProcessThread(self, sourceImage, imageId, isSetting= False):
        time = TimeControl.time()
        if sourceImage is None:
            messagebox.showwarning("Source Image", "Please choose the image first!")
            return
        # self.mainWindow.showImage(image)
        rectSize = 39
        rectInfoList = []
        baseAreaDetectList = []
        original_reference_roi = None
        reference_roi = None

        nNG = 0
        current_roi = None
        try:
            vertical_line = []
            horizontal_line = []
            base_point = []


            ret, rotateResultList, text = self.rotate_algorithm.executeAlgorithm(image=sourceImage)
            if not ret:
                self.mainWindow.runningTab.insertLog(text)
                return
            rotate_roi = None
            point_vertical_1 = None
            point_vertical_2 = None
            point_horizontal_1 = None
            point_horizontal_2 = None
            top_point_in_reference_point = None

            for result in rotateResultList:
                if result.methodName == MethodList.erode.value and result.stepId > 5:

                    if isSetting:
                        original_reference_roi = self.rotate_algorithm.imageList[result.stepId][base_point[1]: base_point[3],
                                        base_point[0]: base_point[2]]

                    else:
                        current_roi = sourceImage[base_point[1]: base_point[3], base_point[0]: base_point[2]]

                if result.methodName == MethodList.getExtreme.value:
                    # rotate_roi = (0, max(result.extreme[1] - 50, 0), sourceImage.shape[1], result.extreme[1] + self.currentModel.fi_height_checking + 50 )
                    rotate_roi = self.rotate_algorithm.imageList[result.stepId][max(result.point[1] - 50, 0):result.point[1] + self.currentModel.fi_height_checking + 50,
                                                                                0:sourceImage.shape[1]]
                    # lấy base point ( chiều x lấy toàn bộ ảnh, chiều y lấy từ điểm 0 hoặc từ 50 đổ lên của điểm max roi tới chiều dài cần check + 50)
                    base_point = (0, max(result.point[1] - 50, 0), sourceImage.shape[1], result.point[1] + self.currentModel.fi_height_checking + 50)
                    if result.point[1] - 50 > 0:
                        top_point_in_reference_point = 50
                    else:
                        top_point_in_reference_point = result.point[1]

                    height_check_up = top_point_in_reference_point + self.currentModel.fi_top_vertical_y
                    base_left_point_x = 0
                    for x_value in range(rotate_roi.shape[1]):
                        if rotate_roi[height_check_up, x_value][0] == 255:
                            base_left_point_x = x_value
                            break

                    # Lấy đường thẳng chiều ngang
                    fi_left_horizontal_x = self.currentModel.fi_left_horizontal_x + base_left_point_x
                    fi_right_horizontal_x = self.currentModel.fi_right_horizontal_x + base_left_point_x

                    point_horizontal_list = [None, None, None, None, None, None, None, None, None, None]
                    point_x_value_list = [fi_left_horizontal_x,
                                          fi_left_horizontal_x + 5,
                                          fi_left_horizontal_x + 10,
                                          fi_left_horizontal_x + 15,
                                          fi_left_horizontal_x + 20,
                                          fi_right_horizontal_x,
                                          fi_right_horizontal_x + 5,
                                          fi_right_horizontal_x + 10,
                                          fi_right_horizontal_x + 15,
                                          fi_right_horizontal_x + 20]
                    for y_value in range(rotate_roi.shape[0]):
                        for i, (point_horizontal, x_value)in enumerate(zip(point_horizontal_list, point_x_value_list)):
                            if point_horizontal is None and rotate_roi[y_value, x_value][0] == 255:
                                point_horizontal_list[i] = (x_value, y_value)
                        if None not in point_horizontal_list:
                            break

                    point_horizontal_1 = (int(sum([point_horizontal_list[i][0] for i in range(5)]) / 5),
                                    int(sum([point_horizontal_list[i][1] for i in range(5)]) / 5))

                    point_horizontal_2 = (int(sum([point_horizontal_list[i][0] for i in range(5, 10)]) / 5),
                                    int(sum([point_horizontal_list[i][1] for i in range(5, 10)]) / 5))

                    horizontal_line = (point_horizontal_1, point_horizontal_2)

                    # imShow = rotate_roi.copy()
                    # if len(imShow.shape) < 3:
                    #     imShow = ImageProcess.processCvtColor(imShow, cv.COLOR_GRAY2BGR)
                    # cv.line(imShow, point_horizontal_1, point_horizontal_2, (0, 255, 0), 10, cv.LINE_AA)
                    # self.mainWindow.workingThread.fpc_inspection_run_window.showImage(imShow)
                    # messagebox.showinfo("", "")

                    # # lấy đường thẳng chiều dọc
                    # height_check_down = self.currentModel.fi_height_checking
                    # height_check_up = 350
                    # point_vertical_list = [None, None, None, None, None, None, None, None, None, None]
                    # point_y_value_list = [height_check_up,
                    #                       height_check_up + 5,
                    #                       height_check_up + 10,
                    #                       height_check_up + 15,
                    #                       height_check_up + 20,
                    #                       height_check_down,
                    #                       height_check_down - 5,
                    #                       height_check_down - 10,
                    #                       height_check_down - 15,
                    #                       height_check_down - 20]
                    #
                    # for x_value in range(rotate_roi.shape[1]):
                    #     for i, (point_vertical, y_value) in enumerate(zip(point_vertical_list, point_y_value_list)):
                    #         if point_vertical is None and rotate_roi[y_value, x_value][0] == 255:
                    #             point_vertical_list[i] = (x_value, y_value)
                    #     if None not in point_vertical_list:
                    #         break
                    #
                    # point_vertical_1 = (int(sum([point_vertical_list[i][0] for i in range(5)]) / 5),
                    #                     int(sum([point_vertical_list[i][1] for i in range(5)]) / 5))
                    #
                    # point_vertical_2 = (int(sum([point_vertical_list[i][0] for i in range(5, 10)]) / 5),
                    #                     int(sum([point_vertical_list[i][1] for i in range(5, 10)]) / 5))
                    #
                    # vertical_line = (point_vertical_1, point_vertical_2)


                    # angle = ImageProcess.findAngleByLine(vertical_line, horizontal_line)
                    # self.mainWindow.runningTab.insertLog(f"angle = {angle}")
                if result.methodName == MethodList.getImageInsideContour.value:
                    ret, resultList, text = self.translation_algorithm.executeAlgorithm(image=self.rotate_algorithm.imageList[result.stepId])
                    for result in resultList:
                        if result.methodName == MethodList.dilate.value:
                            reference_roi = self.translation_algorithm.imageList[result.stepId][
                                            base_point[1]: base_point[3],
                                            base_point[0]: base_point[2]]
                            if isSetting:
                                height_check_up = top_point_in_reference_point + self.currentModel.fi_top_vertical_y
                                height_check_down = top_point_in_reference_point + self.currentModel.fi_bottom_vertical_y

                                point_vertical_list = [None, None, None, None, None, None, None, None, None, None]
                                x_value_old_list = [None, None, None, None, None, None, None, None, None, None]
                                point_y_value_list = [height_check_up,
                                                      height_check_up + 5,
                                                      height_check_up + 10,
                                                      height_check_up + 15,
                                                      height_check_up + 20,
                                                      height_check_down,
                                                      height_check_down - 5,
                                                      height_check_down - 10,
                                                      height_check_down - 15,
                                                      height_check_down - 20]

                                for x_value in range(reference_roi.shape[1]):
                                    for i, (point_vertical, y_value) in enumerate(zip(point_vertical_list, point_y_value_list)):
                                        if reference_roi[y_value, x_value] == 255:
                                            if point_vertical is None:
                                                point_vertical_list[i] = (0, 0)
                                                x_value_old_list[i] = x_value
                                            elif point_vertical == (0, 0):
                                                if x_value - x_value_old_list[i] > self.currentModel.fi_rear_distance:
                                                    point_vertical_list[i] = (x_value, y_value)

                                    if None not in point_vertical_list and (0, 0) not in point_vertical_list:
                                        break

                                point_vertical_1 = (int(sum([point_vertical_list[i][0] for i in range(5)]) / 5),
                                                    int(sum([point_vertical_list[i][1] for i in range(5)]) / 5))

                                point_vertical_2 = (int(sum([point_vertical_list[i][0] for i in range(5, 10)]) / 5),
                                                    int(sum([point_vertical_list[i][1] for i in range(5, 10)]) / 5))

                                vertical_line = (point_vertical_1, point_vertical_2)
                            else:
                                current_roi = sourceImage[base_point[1]: base_point[3], base_point[0]: base_point[2]]

            if isSetting:
                cv.line(rotate_roi, point_vertical_1, point_vertical_2, (0, 255, 0), 10, cv.LINE_AA)
                cv.line(rotate_roi, point_horizontal_1, point_horizontal_2, (0, 255, 0), 10, cv.LINE_AA)
                self.mainWindow.showImage(rotate_roi)
                return vertical_line, horizontal_line, base_point, original_reference_roi

            else:
                current_roi = sourceImage[base_point[1]: base_point[3], base_point[0]: base_point[2]]
                # Trong trường hợp chạy
                # Tìm góc lệch giữa ảnh master và ảnh hiện tại thông qua cạnh ngang
                angle = ImageProcess.findAngleByLine(self.currentModel.fi_reference_line_horizontal, horizontal_line)
                self.mainWindow.runningTab.insertLog("angle: {}".format(angle))
                # tìm điểm chính giữa của đường thẳng ngang của ảnh master
                horizontal_base_point = (int((horizontal_line[0][0] + horizontal_line[1][0]) / 2),
                                         int((horizontal_line[0][1] + horizontal_line[1][1]) / 2))
                #
                #
                # # Xoay ảnh hiện tại về góc của ảnh master
                ret, preProcessImage, text = ImageProcess.rotateImage(sourceImage=sourceImage,
                                                                      angle=angle,
                                                                      centerPoint=horizontal_base_point)

                # Tìm cạnh dọc
                # Get vertical line
                #xoay roi về góc của master.
                ret, reference_roi, text = ImageProcess.rotateImage(sourceImage=reference_roi,
                                                                      angle=angle,
                                                                      centerPoint=horizontal_base_point)
                ret, current_roi, text = ImageProcess.rotateImage(sourceImage=current_roi,
                                                                    angle=angle,
                                                                    centerPoint=horizontal_base_point)
                #
                # self.mainWindow.showImage(reference_roi)
                # messagebox.showinfo("", "")


                # tìm 2 điểm trên cạnh dọc
                height_check_up = top_point_in_reference_point + self.currentModel.fi_top_vertical_y
                height_check_down = top_point_in_reference_point + self.currentModel.fi_bottom_vertical_y
                point_vertical_list = [None, None, None, None, None, None, None, None, None, None]
                x_value_old_list = [None, None, None, None, None, None, None, None, None, None]
                point_y_value_list = [height_check_up,
                                      height_check_up + 5,
                                      height_check_up + 10,
                                      height_check_up + 15,
                                      height_check_up + 20,
                                      height_check_down,
                                      height_check_down - 5,
                                      height_check_down - 10,
                                      height_check_down - 15,
                                      height_check_down - 20]

                for x_value in range(reference_roi.shape[1]):
                    for i, (point_vertical, y_value) in enumerate(zip(point_vertical_list, point_y_value_list)):
                        if reference_roi[y_value, x_value] == 255:
                            if point_vertical is None:
                                point_vertical_list[i] = (0, 0)
                                x_value_old_list[i] = x_value
                            elif point_vertical == (0, 0):
                                if x_value - x_value_old_list[i] > self.currentModel.fi_rear_distance:
                                    point_vertical_list[i] = (x_value, y_value)

                    if None not in point_vertical_list and (0, 0) not in point_vertical_list:
                        break
                point_vertical_1 = (int(sum([point_vertical_list[i][0] for i in range(5)]) / 5),
                                    int(sum([point_vertical_list[i][1] for i in range(5)]) / 5))

                point_vertical_2 = (int(sum([point_vertical_list[i][0] for i in range(5, 10)]) / 5),
                                    int(sum([point_vertical_list[i][1] for i in range(5, 10)]) / 5))

                # ghép 2 điểm dọc lại thành cạnh dọc
                vertical_line = (point_vertical_1, point_vertical_2)

                # lấy trung điểm của cạnh dọc
                vertical_base_point = (int((vertical_line[0][0] + vertical_line[1][0]) / 2),
                                       int((vertical_line[0][1] + vertical_line[1][1]) / 2))

                # imShow = reference_roi.copy()
                # if len(imShow.shape) < 3:
                #     imShow = ImageProcess.processCvtColor(imShow, cv.COLOR_GRAY2BGR)
                # cv.line(img=imShow,pt1=point_vertical_1, pt2=point_vertical_2, color=(0, 255, 0), thickness=5, lineType=cv.LINE_AA)
                # self.mainWindow.workingThread.fpc_inspection_run_window.showImage(imShow)
                # messagebox.showinfo("", "")

                # quay trung điểm của cạnh dọc theo chiều quay của ảnh master.
                # ret, horizontal_base_point_rotate, text = ImageProcess.rotatePoint((0, 0), horizontal_base_point, angle)
                # ret, vertical_base_point_rotate, text = ImageProcess.rotatePoint(origin=horizontal_base_point,point=vertical_base_point, angle=angle)


                # Tính ra độ lệch x và độ lệch y
                x_distance_change = 0
                y_distance_change = 0
                y_distance_change = int((self.currentModel.fi_reference_line_horizontal[0][1]
                                         + self.currentModel.fi_reference_line_horizontal[1][1]) / 2
                                        + self.currentModel.fi_reference_base_point[1]
                                        - (horizontal_base_point[1] + base_point[1]))

                x_distance_change = int((self.currentModel.fi_reference_line_vertical[0][0]
                                         + self.currentModel.fi_reference_line_vertical[1][0]) / 2
                                        - vertical_base_point[0])


                ret, preProcessImage, text = ImageProcess.processTransMoveImage(preProcessImage,
                                                                                move_x=x_distance_change,
                                                                                move_y=y_distance_change)

                y_distance_change_1 = int((self.currentModel.fi_reference_line_horizontal[0][1]
                                         + self.currentModel.fi_reference_line_horizontal[1][1]) / 2
                                        - horizontal_base_point[1])
                # ret, reference_roi, text = ImageProcess.processTransMoveImage(reference_roi,
                #                                                                 move_x=x_distance_change,
                #                                                               move_y=y_distance_change_1)
                ret, current_roi, text = ImageProcess.processTransMoveImage(current_roi,
                                                                              move_x=x_distance_change,
                                                                              move_y=y_distance_change_1)
                # self.mainWindow.showImage(reference_roi)
                # messagebox.showinfo("", "")
                #
                # reference_roi = ImageProcess.processBitwise_xor(self.reference_binary_roi, reference_roi)
                # self.mainWindow.showImage(reference_roi)
                # messagebox.showinfo("", "")

                imshow = preProcessImage.copy()
                # current_roi = preProcessImage[self.currentModel.fi_reference_base_point[1]:
                #                               self.currentModel.fi_reference_base_point[3],
                #                             self.currentModel.fi_reference_base_point[0]:
                #                             self.currentModel.fi_reference_base_point[2]]
                preProcessImage = ImageProcess.processBitwise_and(current_roi, current_roi, self.reference_binary_roi)
                # self.mainWindow.workingThread.fpc_inspection_run_window.showImage(preProcessImage)
                # self.mainWindow.showImage(preProcessImage, True)
                # messagebox.showinfo("", "")

                if self.currentModel.fi_fpc_type == 4:
                    preProcessImage = ImageProcess.processCvtColor(preProcessImage, cv.COLOR_BGR2GRAY)
                    averageColor = cv.mean(preProcessImage, mask=self.reference_binary_roi)
                    self.mainWindow.showBottomMiddleText(f"Mean color: {averageColor}")
                    preProcessImage[preProcessImage == 0] = averageColor[0]
                    # self.mainWindow.showImage(preProcessImage)
                    # messagebox.showinfo("", "")
                    preProcessImage_1 = None
                    preProcessImage_2 = None
                    if self.currentModel.fi_brightness_reflection_1 > 0:
                        ret, preProcessImage_1 = ImageProcess.processThreshold(preProcessImage, int(averageColor[0] + self.currentModel.fi_brightness_reflection_1), maxval=255, type=cv.THRESH_BINARY)
                    elif self.currentModel.fi_brightness_reflection_1 < 0:
                        ret, preProcessImage_1 = ImageProcess.processThreshold(preProcessImage, int(averageColor[0] + self.currentModel.fi_brightness_reflection_1), maxval=255, type=cv.THRESH_BINARY_INV)

                    if self.currentModel.fi_brightness_reflection_2 > 0:
                        ret, preProcessImage_2 = ImageProcess.processThreshold(preProcessImage, int(averageColor[0] + self.currentModel.fi_brightness_reflection_2), maxval=255, type=cv.THRESH_BINARY)
                    elif self.currentModel.fi_brightness_reflection_2 < 0:
                        ret, preProcessImage_2 = ImageProcess.processThreshold(preProcessImage, int(averageColor[0] + self.currentModel.fi_brightness_reflection_2), maxval=255, type=cv.THRESH_BINARY_INV)


                    if preProcessImage_1 is None and preProcessImage_2 is not None:
                        preProcessImage = preProcessImage_1
                    elif preProcessImage_1 is not None and preProcessImage_2 is None:
                        preProcessImage = preProcessImage_2
                    elif preProcessImage_1 is not None and preProcessImage_2 is not None:
                        preProcessImage = ImageProcess.processBitwise_or(preProcessImage_1, preProcessImage_2)
                # self.mainWindow.showImage(preProcessImage)
                # return
                # self.mainWindow.showImage(preProcessImage)
                if ret:
                    ret, inspectionResults, text = self.inspection_algorithm.executeAlgorithm(image=preProcessImage)
                    if ret:
                        ret = False
                        if self.currentModel is not None:
                            for inspectionResult in inspectionResults:
                                if inspectionResult.methodName == MethodList.findContour.value:
                                    if inspectionResult.passed:
                                        basePoint = inspectionResult.basePoint
                                        workingArea = inspectionResult.workingArea
                                        basePoint = (basePoint[0] + workingArea[0], basePoint[1] + workingArea[1])
                                        areaDetectList = inspectionResult.detectAreaList
                                        for areaDetect in areaDetectList:
                                            baseAreaDetectList.append((areaDetect[0] + inspectionResult.basePoint[0] + self.currentModel.fi_reference_base_point[0],
                                                                       areaDetect[1] + inspectionResult.basePoint[1]+ self.currentModel.fi_reference_base_point[1],
                                                                       areaDetect[2] + inspectionResult.basePoint[0]+ self.currentModel.fi_reference_base_point[0],
                                                                       areaDetect[3] + inspectionResult.basePoint[1]+ self.currentModel.fi_reference_base_point[1]))
                        baseAreaDetectList.sort(key=self.sortStartX)
                        for areaDetect in baseAreaDetectList:
                            if len(rectInfoList) < 1:
                                # khi chưa có nhóm nào thì khởi tạo nhóm đầu tiên
                                rectInfoList.append(RectInfo(baseRect=areaDetect, betweenDist=rectSize * 2))
                            else:
                                # khi đã có nhóm rồi thì cho check từng nhóm một
                                ret = False
                                for rectInfo in rectInfoList:
                                    # Duyệt từng nhóm một xem đường tròn có thỏa mãn hay không
                                    ret = rectInfo.checkRect(rect=areaDetect)
                                    if ret:
                                        break
                                if not ret:
                                    # nếu đường tròn không thuộc nhóm nào thì thêm 1 nhóm mới
                                    rectInfoList.append(RectInfo(baseRect=areaDetect, betweenDist=rectSize * 2))
                        for areaDetect in rectInfoList:
                            cv.rectangle(img=imshow,
                                         pt1=(areaDetect.finalRect[0] - rectSize, areaDetect.finalRect[1] - rectSize),
                                         pt2=(areaDetect.finalRect[2] + rectSize, areaDetect.finalRect[3] + rectSize),
                                         color=(255, 255, 0),
                                         thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                         lineType=cv.LINE_AA)
                            nNG += 1
                else:
                    self.mainWindow.runningTab.insertLog(text)
                self.mainWindow.showImage(imshow)
                # if self.mainWindow.workingThread.runningFlag:
                if nNG == 0:
                    self.mainWindow.workingThread.fpc_inspection_run_window.showImage(imshow)
                else:
                    self.mainWindow.workingThread.fpc_inspection_run_window.showImage(imshow, False)

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR FPC inspection. Detail: {}".format(error))

    def sortStartX(self, e):
        return e[0]

class RectInfo:
    finalRect = (0, 0, 0, 0)
    betweenDist = 0
    def __init__(self, baseRect = (0, 0, 0, 0), betweenDist=100):
        self.betweenDist = betweenDist
        self.finalRect = baseRect
        self.checkRect(rect=baseRect)


    def checkRect(self, rect):
        startX = rect[0]
        startY = rect[1]
        if ImageProcess.calculateDistanceBy2Points((startX, startY), (self.finalRect[0], self.finalRect[1])) < self.betweenDist \
                or ImageProcess.calculateDistanceBy2Points((rect[2], rect[3]), (self.finalRect[2], self.finalRect[3])) < self.betweenDist \
                or ImageProcess.calculateDistanceBy2Points((rect[0], rect[1]), (self.finalRect[2], self.finalRect[3])) < self.betweenDist\
                or ImageProcess.calculateDistanceBy2Points((rect[2], rect[3]), (self.finalRect[0], self.finalRect[1])) < self.betweenDist\
                or (self.finalRect[0] < rect[0] < self.finalRect[2] and self.finalRect[1] < rect[1] < self.finalRect[3])\
                or (self.finalRect[0] < rect[2] < self.finalRect[2] and self.finalRect[1] < rect[3] < self.finalRect[3])\
                or (self.finalRect[0] < rect[0] < self.finalRect[2] and self.finalRect[1] < rect[3] < self.finalRect[3]) \
                or (self.finalRect[0] < rect[2] < self.finalRect[2] and self.finalRect[1] < rect[1] < self.finalRect[3]):

            # Nếu đường tròn thỏa mãn điều kiện gần nhau
            self.finalRect = (min(self.finalRect[0], rect[0]),
                              min(self.finalRect[1], rect[1]),
                              max(self.finalRect[2], rect[2]),
                              max(self.finalRect[3], rect[3]))
            return True
        else:
            # khi không thỏa mãn điều kiện gần nhau
            return False
