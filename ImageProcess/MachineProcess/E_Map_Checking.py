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

class E_Map_Checking:
    currentModel: ModelParameter = None
    resultMatrix = None
    ng_find_algorithm: Algorithm = None
    code_reading_algorithm: Algorithm = None

    code_reading_camera: Camera = None
    ng_finding_camera: Camera = None

    data_dir = "./data/E_Map"

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def updateModel(self):
        self.currentModel = self.mainWindow.modelSettingTab.modelManager.getCurrentModel()
        self.ng_find_algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName(self.currentModel.emap_ng_finding_algorithm)
        self.code_reading_algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName(self.currentModel.emap_code_reading_algorithm)
        self.code_reading_camera = self.mainWindow.workingThread.cameraManager.cameraList[self.currentModel.emap_code_reading_camera_id]
        self.ng_finding_camera = self.mainWindow.workingThread.cameraManager.cameraList[self.currentModel.emap_ng_finding_camera_id]

    def checkReady(self):
        self.updateModel()
        ret = True
        if self.ng_find_algorithm is None:
            messagebox.showerror("Algorithm setting", "Please choose NG algorithm for model!")
            ret = False
        if self.code_reading_algorithm is None:
            messagebox.showerror("Algorithm setting", "Please choose Code Reading algorithm for model!")
            ret = False

        if not self.code_reading_camera.connect():
            messagebox.showerror("Camera connection", "Please check the CODE READING CAMERA connection!")
            ret = False

        if not self.ng_finding_camera.connect():
            messagebox.showerror("Camera connection", "Please check the NG FINDING CAMERA connection!")
            ret = False

        return ret

    def do_process(self):
        code = ""
        ret, matrix = self.getMatrixOfNG()
        if ret:
            ret, code = self.readCode()
        if ret:
            ret = self.save_data_to_file(code=code, matrix=matrix)

        return ret

    def getMatrixOfNG(self, ng_finding_image=None):
        if ng_finding_image is None:
            ret, ng_finding_image = self.ng_finding_camera.takePicture()
            if not ret:
                messagebox.showerror("Camera connection", "Please check the NG FINDING CAMERA connection!")
                self.mainWindow.runningTab.insertLog("ERROR NG FINDING CAMERA connection!")
                return ret, []

        # self.resultMatrix = np.zeros((self.currentModel.emap_rows, self.currentModel.emap_cols),dtype=np.int8)
        self.resultMatrix = np.zeros((9, 12),dtype=np.int8)
        for row in range(self.currentModel.emap_rows):
            for column in range(self.currentModel.emap_cols):
                point1 = (self.currentModel.emap_start_point[0] + self.currentModel.emap_distanceX * column,
                          self.currentModel.emap_start_point[1] + self.currentModel.emap_distanceY * row)
                point2 = (point1[0] + self.currentModel.emap_size_rect[0],
                          point1[1] + self.currentModel.emap_size_rect[1])

                roi_process = ng_finding_image[point1[1]: point2[1], point1[0]: point2[0]]
                ret, resultList, text = self.ng_find_algorithm.executeAlgorithm(image=roi_process)
                if ret:
                    cv.rectangle(ng_finding_image, pt1=point1, pt2=point2, color=(0, 255, 0), thickness=5,
                                 lineType=cv.LINE_AA)

                    for result in resultList:
                        if not result.passed:
                            self.resultMatrix[row][column] = 1
                            cv.rectangle(ng_finding_image, pt1=point1, pt2=point2, color=(0, 0, 255), thickness=5, lineType=cv.LINE_AA)
                            break

                else:
                    self.resultMatrix[row][column] = 1
                # cv.rectangle(sourceImage, pt1=point1, pt2=point2, color=(0, 255, 255), thickness=3, lineType=cv.LINE_AA)

        self.mainWindow.showImage(ng_finding_image)
        return True, self.resultMatrix
    def readCode(self, codeImage=None):
        code = ""
        if codeImage is None:
            ret, codeImage = self.code_reading_camera.takePicture()
            if not ret:
                messagebox.showerror("Camera connection", "Please check the CODE READING CAMERA connection!")
                self.mainWindow.runningTab.insertLog("ERROR CODE READING CAMERA connection!")
                return ret, ""
        ret, resultList, text = self.code_reading_algorithm.executeAlgorithm(image=codeImage)
        if not ret:
            self.mainWindow.runningTab.insertLog(text)
            return ret, ""

        for result in resultList:
            if result.methodName == MethodList.dataMatrixReader.value:
                if len(result.barcodeList) > 0:
                    code = result.barcodeList[0][0][0]

        return True, code

    def save_data_to_file(self, code, matrix):
        model_dir = self.data_dir + "/" + self.currentModel.emap_model_code
        PathFileControl.generatePath(model_dir)

        date = TimeControl.y_m_dFormat()
        date_dir = model_dir + "/" + date
        PathFileControl.generatePath(date_dir)

        txt_file_path = f"{date_dir}/{code}.txt"
        csv_file_path = f"{date_dir}/{self.currentModel.emap_model_code}_{date}.csv"

        textFile = TextFile(txt_file_path)
        str_matrix = []
        str_matrix.append("  A B C D E F G H I J K L")
        for row in range(9):
            str_row_matrix = f"{9 - row}"
            for col in range(12):
                str_row_matrix += f" {matrix[row][col]}"
            str_matrix.append(str_row_matrix)
        textFile.dataList = str_matrix
        textFile.saveFile()

        csvFile = CsvFile(csv_file_path)
        csvFile.appendData([txt_file_path])

        return True