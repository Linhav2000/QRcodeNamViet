from View.Common.VisionUI import *
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue
from View.Common.CommonStepFrame import InputParamFrame
from View.Common.CommonStepFrame import CheckboxStepParamFrame
from tkinter import filedialog
from View.Calibration.CalibrationParm import CalibrationParm
import jsonpickle
from CommonAssit import PathFileControl
from CommonAssit.FileManager import JsonFile
import glob
import cv2 as cv
import numpy as np
import threading
from ImageProcess import ImageProcess

class ChessboardCalibrationFrame(VisionLabelFrame):
    caliPath = "./config/Calibration"
    yDistance = 30
    xDistance = 150

    cameraCombo: ComboForFlexibleValue
    OkButton: OkButton
    liveCalibration: CheckboxStepParamFrame
    caliImagePath: InputParamFrame
    cbc_sizeX: InputParamFrame
    cbc_sizeY: InputParamFrame
    max_picture: InputParamFrame
    btnSelectImagePath: VisionButton
    btnStart: VisionButton
    btnStop: VisionButton

    isCalibrating = False

    def __init__(self, master, mainWindow):
        from MainWindow import MainWindow
        VisionLabelFrame.__init__(self, master=master, text="Camera Calibration")
        self.calibrationParm = CalibrationParm()
        self.mainWindow: MainWindow = mainWindow
        self.setupView()
        self.getParm()

    def setupView(self):
        cameraList = []
        for i in range(10):
            cameraList.append(f"Camera {i}")
        self.cameraCombo = ComboForFlexibleValue(self, lblText="chosen Camera: ", yPos=5 + 0 * self.yDistance,
                                                 height=self.yDistance, valueList=cameraList)

        self.liveCalibration = CheckboxStepParamFrame(self, lblText="Live Calibration: ", yPos= 5 + 1*self.yDistance,
                                                height=self.yDistance, command=self.clickLiveCalibration)

        self.caliImagePath = InputParamFrame(self, lblText="Cali Image path: ", yPos= 5 + 2*self.yDistance,
                                                height=self.yDistance, width=150)

        self.btnSelectImagePath = VisionButton(self, text="Select Path", command=self.clickBtnSelectImagePath)
        self.btnSelectImagePath.place(x=320, y=5 + 2*self.yDistance, width=80, height=22)

        self.cbc_sizeX = InputParamFrame(self, "size X(corners) :",
                                         yPos=3 * self.yDistance + 5, height=self.yDistance)
        self.cbc_sizeY = InputParamFrame(self, "size Y(corners) :",
                                         yPos=4 * self.yDistance + 5, height=self.yDistance)

        self.max_picture = InputParamFrame(self, "Max pictures",
                                           yPos=5 * self.yDistance + 5, height=self.yDistance)

        self.btnStart = VisionButton(self, text="Start", command=self.clickBtnStart)
        self.btnStart.place(relx=0.2, y=5 + 7 * self.yDistance, width=80, height=22)

        self.btnStop = VisionButton(self, text="Stop", command=self.clickBtnStop)
        self.btnStop.place(relx=0.6, y=5 + 7 * self.yDistance, width=80, height=22)

        self.OkButton = OkButton(self, command=self.clickBtnOK)
        self.OkButton.place(relx=0.265, rely=0.935, relwidth=0.225, relheight=0.05)


    def clickBtnStart(self):
        self.isCalibrating = True
        self.saveValue()
        if self.calibrationParm.liveCalibration:
            thread = threading.Thread(target=self.calibrateLive, args=())
            thread.start()
            # thread.join()
        else:
            self.calibrateOffline()


    def clickBtnStop(self):
        self.isCalibrating = False

    def cameraSelectChange(self, cameraId):
        self.mainWindow.workingThread.cameraManager.changeCamera(cameraId)

    def clickLiveCalibration(self, parm):
        self.btnStop.config(state='normal' if  parm else "disable")

    def clickBtnSelectImagePath(self):
        folder_selected = filedialog.askdirectory(title="Select Image Path")
        self.caliImagePath.setValue(folder_selected)

    def clickBtnOK(self):
        self.saveValue()
        self.saveParm()
        self.place_forget()

    def updateValue(self):
        self.cameraCombo.setPosValue(self.mainWindow.commonSettingManager.settingParm.currentCamera)
        self.liveCalibration.setValue(self.calibrationParm.liveCalibration)
        self.caliImagePath.setValue(self.calibrationParm.caliImagePath)
        self.cbc_sizeX.setValue(self.calibrationParm.sizeX)
        self.cbc_sizeY.setValue(self.calibrationParm.sizeY)
        self.clickLiveCalibration(self.liveCalibration.getValue())
        self.max_picture.setValue(self.calibrationParm.maxPictures)

    def saveValue(self):
        self.calibrationParm.liveCalibration = self.liveCalibration.getValue()
        self.calibrationParm.caliImagePath = self.caliImagePath.getValue()
        self.calibrationParm.sizeX = self.cbc_sizeX.getIntValue()
        self.calibrationParm.sizeY = self.cbc_sizeY.getIntValue()
        self.calibrationParm.maxPictures = self.max_picture.getIntValue()

    def getParm(self):
        PathFileControl.generatePath("./config")
        PathFileControl.generatePath("./config/Calibration")

        jsonFile = JsonFile(self.caliPath + "/parm.json")
        data = jsonFile.readFile()
        if data != '':
            self.calibrationParm = jsonpickle.decode(data)

    def saveParm(self):
        jsonFile = JsonFile(self.caliPath + "/parm.json")
        jsonFile.data = jsonpickle.encode(self.calibrationParm)
        jsonFile.saveFile()

    def calibrateLive(self):
        self.mainWindow.runningTab.insertLog("Start calibration camera")
        PathFileControl.deleteFile(self.caliPath + f"/{self.cameraCombo.getValue()}/cameraMatrix.txt")
        PathFileControl.deleteFile(self.caliPath + f"/{self.cameraCombo.getValue()}/distortionCoefficient.txt")

        checkerboard = (self.calibrationParm.sizeX, self.calibrationParm.sizeY)
        # images = glob.glob(self.calibrationParm.caliImagePath + '/*.jpg')

        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        object_point = np.zeros((checkerboard[1] * checkerboard[0], 3), np.float32)
        object_point[:, :2] = np.mgrid[0:checkerboard[0], 0:checkerboard[1]].T.reshape(-1, 2)
        # Arrays to store object points and image points from all the images.
        object_point_list = []  # 3d point in real world space
        image_points = []  # 2d points in image plane.

        n_picture = 0
        while self.isCalibrating and n_picture < self.calibrationParm.maxPictures:
            ret, img = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture(cali=False)

            if ret:
                ret, gray = ImageProcess.processThreshold(img,0,255, cv.THRESH_BINARY + cv.THRESH_OTSU)
                gray = cv.GaussianBlur(gray, (3, 3), 1)
                # gray = cv.resize(gray, (0, 0), fx=0.2, fy=0.2)
                # gray = cv.GaussianBlur(gray, (5, 5), 3)
                # Find the chess board corners
                # corners = cv.goodFeaturesToTrack(gray, 25, 0.01, 10)
                # ret, corners = cv.findChessboardCorners(gray, self.chekerboard, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FILTER_QUADS);
                ret, corners = cv.findChessboardCorners(gray, checkerboard,
                                                        cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)

                # If found, add object points, image points (after refining them)
                if ret:
                    object_point_list.append(object_point)
                    corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                    image_points.append(corners2)

                    # Draw and display the corners
                    img = cv.drawChessboardCorners(img, checkerboard, corners2, ret)
                    self.mainWindow.showImage(img)
                    n_picture += 1
                else:
                    self.mainWindow.showImage(gray)

            else:
                self.isCalibrating = False
                text = f"ERROR Take Picture. Please check the camera connection!"
                self.mainWindow.runningTab.insertLog(text)
                return

            cv.waitKey(3)
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(object_point_list, image_points, gray.shape[::-1], None, None)
        # saveMatrixThread = threading.Thread(target=self.saveMatrix, args=(mtx, dist))
        # saveMatrixThread.start()
        PathFileControl.generatePath(self.caliPath + f"/{self.cameraCombo.getValue()}")

        np.savetxt(self.caliPath + f"/{self.cameraCombo.getValue()}/cameraMatrix.txt", mtx)
        cv.waitKey(100)
        np.savetxt(self.caliPath + f"/{self.cameraCombo.getValue()}/distortionCoefficient.txt", dist)
        cv.waitKey(100)
        # print(mtx)
        # print(dist)
        # Check the min mean_error

        # print(objpoints.shape[0])
        # print(len(objpoints))
        total_error = 0
        for i in range(len(object_point_list)):
            imgpoints2, _ = cv.projectPoints(object_point_list[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv.norm(image_points[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
            total_error += error
        mean_error = total_error / len(object_point_list)
        print("total error: ", mean_error)
        self.mainWindow.runningTab.insertLog("End calibration camera")
        self.isCalibrating = False

    def saveMatrix(self, mtx, dist):
        PathFileControl.generatePath(self.caliPath + f"/{self.cameraCombo.getValue()}")

        np.savetxt(self.caliPath + f"/{self.cameraCombo.getValue()}/cameraMatrix.txt", mtx)
        cv.waitKey(5)
        np.savetxt(self.caliPath + f"/{self.cameraCombo.getValue()}/distortionCoefficient.txt", dist)

    def calibrateOffline(self):
        self.mainWindow.runningTab.insertLog("Start calibration camera")
        checkerboard = (self.calibrationParm.sizeX, self.calibrationParm.sizeY)
        images = glob.glob(self.calibrationParm.caliImagePath + '/*.jpg')
        images += glob.glob(self.calibrationParm.caliImagePath + '/*.png')
        images += glob.glob(self.calibrationParm.caliImagePath + '/*.bmp')
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        object_point = np.zeros((checkerboard[1] * checkerboard[0], 3), np.float32)
        object_point[:, :2] = np.mgrid[0:checkerboard[0], 0:checkerboard[1]].T.reshape(-1, 2)
        # Arrays to store object points and image points from all the images.
        object_point_list = []  # 3d point in real world space
        image_points = []  # 2d points in image plane.

        for file_name in images:
            img = cv.imdecode(np.fromfile(file_name, dtype=np.uint8), cv.IMREAD_COLOR)
            ret, gray = ImageProcess.processThreshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
            # gray = cv.resize(gray, (0, 0), fx=0.2, fy=0.2)
            gray = cv.GaussianBlur(gray, (3, 3), 1)
            # Find the chess board corners
            # corners = cv.goodFeaturesToTrack(gray, 25, 0.01, 10)
            # ret, corners = cv.findChessboardCorners(gray, self.chekerboard, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FILTER_QUADS);
            ret, corners = cv.findChessboardCorners(gray, checkerboard,
                                                    cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)

            # If found, add object points, image points (after refining them)
            if ret:
                object_point_list.append(object_point)
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                image_points.append(corners2)

                # Draw and display the corners
                img = cv.drawChessboardCorners(img,checkerboard, corners2, ret)
                self.mainWindow.showImage(img)
            else:
                PathFileControl.deleteFile(file_name)
                self.mainWindow.showImage(img)

                # img = cv.resize(img, (800, 600))
                # cv.imshow('img', img)
            cv.waitKey(100)
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(object_point_list, image_points, gray.shape[::-1], None, None)
        PathFileControl.generatePath(self.caliPath + f"/{self.cameraCombo.getValue()}")

        np.savetxt(self.caliPath + f"/{self.cameraCombo.getValue()}/cameraMatrix.txt", mtx)
        np.savetxt(self.caliPath + f"/{self.cameraCombo.getValue()}/distortionCoefficient.txt", dist)
        # print(mtx)
        # print(dist)
        # Check the min mean_error

        # print(objpoints.shape[0])
        # print(len(objpoints))
        total_error = 0
        for i in range(len(object_point_list)):
            imgpoints2, _ = cv.projectPoints(object_point_list[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv.norm(image_points[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
            total_error += error
        mean_error = total_error / len(object_point_list)
        print("total error: ", mean_error)

        self.isCalibrating = False
        self.mainWindow.runningTab.insertLog("End calibration camera")
