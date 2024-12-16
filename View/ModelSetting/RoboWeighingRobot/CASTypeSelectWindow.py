from tkinter import messagebox
import CommonAssit.CommonAssit as CommonAssit
from View.Common.VisionUI import *
from View.Common.ImageView import ImageView
from Modules.ModelSetting.CAS_Type import CAS_Type
import cv2 as cv
import numpy as np

class CASTypeSelectWindow(VisionTopLevel):
    robot_x_pos_y_pos: ImageView
    robot_x_y_exchanged: ImageView
    robot_x_inv_y_pos: ImageView
    robot_x_y_exchanged_y_inv: ImageView

    cas_type: CAS_Type  = None
    isChanged = False

    def __init__(self, mainWindow):
        VisionTopLevel.__init__(self)
        self.mainWindow = mainWindow
        self.setupWindow()
        self.setupView()

    def setupView(self):
        self.robot_x_pos_y_pos = ImageView(self, self.mainWindow, leftMousePressCmd=lambda : self.select(CAS_Type.robot_x_pos_y_pos))
        self.robot_x_pos_y_pos.place(relx=0.05, rely=0.05, relwidth=0.425, relheight=0.425)
        robot_x_pos_y_pos_image = cv.imdecode(np.fromfile("./resource/robot_x-pos_y-pos.png", dtype=np.uint8), cv.IMREAD_COLOR)
        self.robot_x_pos_y_pos.showImage(image=robot_x_pos_y_pos_image)

        self.robot_x_y_exchanged = ImageView(self, self.mainWindow, leftMousePressCmd=lambda : self.select(CAS_Type.robot_x_y_exchanged))
        self.robot_x_y_exchanged.place(relx=0.525, rely=0.05, relwidth=0.425, relheight=0.425)
        robot_x_y_exchanged_image = cv.imdecode(np.fromfile("./resource/robot_x-y-exchanged.png", dtype=np.uint8), cv.IMREAD_COLOR)
        self.robot_x_y_exchanged.showImage(image=robot_x_y_exchanged_image)

        self.robot_x_inv_y_pos = ImageView(self, self.mainWindow, leftMousePressCmd=lambda : self.select(CAS_Type.robot_x_inv_y_pos))
        self.robot_x_inv_y_pos.place(relx=0.05, rely=0.525, relwidth=0.425, relheight=0.425)
        robot_x_inv_y_pos_image = cv.imdecode(np.fromfile("./resource/robot_x-inv_y-pos.png", dtype=np.uint8), cv.IMREAD_COLOR)
        self.robot_x_inv_y_pos.showImage(image=robot_x_inv_y_pos_image)

        self.robot_x_y_exchanged_y_inv = ImageView(self, self.mainWindow, leftMousePressCmd=lambda : self.select(CAS_Type.robot_x_y_exchanged_y_inv))
        self.robot_x_y_exchanged_y_inv.place(relx=0.525, rely=0.525, relwidth=0.425, relheight=0.425)
        robot_x_y_exchanged_y_inv_image = cv.imdecode(np.fromfile("./resource/robot_x-y-exchanged_y-inv.png", dtype=np.uint8), cv.IMREAD_COLOR)
        self.robot_x_y_exchanged_y_inv.showImage(image=robot_x_y_exchanged_y_inv_image)

    def select(self, type):
        self.cas_type = type
        self.isChanged = True
        self.destroy()

    def setupWindow(self):
        width = 636
        height = 399
        self.title("Select Coordinates Axis System Type")
        self.iconbitmap('./resource/appIcon.ico')
        self.geometry("{}x{}+{}+{}".format(width, height,
                                           int(
                                               self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width() / 2 - width / 2),
                                           int(
                                               self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height() / 2 - height / 2)))
        self.resizable(0, 0)
        self.grab_set()