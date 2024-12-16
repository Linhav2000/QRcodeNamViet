from View.Common.VisionUI import *
from View.Common.ImageView import ImageView
import threading
import cv2 as cv
import numpy as np

class FPC_Verify_Window(VisionTopLevel):
    ccd_view: ImageView
    scan_image_view: ImageView
    total_image_view: ImageView

    parameterFrame: VisionLabelFrame
    live = False


    def __init__(self, mainWindow):
        VisionTopLevel.__init__(self)
        self.mainWindow = mainWindow
        self.setupWindow()
        self.setupView()

    def setupWindow(self):
        width = 1240
        height = 665
        self.title(self.mainWindow.languageManager.localized("version"))
        iconPath = "./resource/appIcon.ico"
        self.iconbitmap(iconPath)
        self.geometry("{}x{}+{}+{}".format(width, height, int
        (self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width() / 2 - width / 2),
                                           int
                                               (
                                               self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height() / 2 - height / 2)))
        self.state("zoomed")
        # self.mainFrame.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.exit)

    def setupView(self):
        self.ccd_view = ImageView(self, self.mainWindow)
        self.ccd_view.place(relx=0.01, rely=0.01, relwidth=0.65,relheight=0.98)
        self.scan_image_view = ImageView(self, self.mainWindow)
        self.scan_image_view.place(relx=0.68, rely=0.01, relwidth=0.31,relheight=0.31)
        self.total_image_view = ImageView(self, self.mainWindow)
        self.total_image_view.place(relx=0.68, rely=0.33, relwidth=0.31,relheight=0.31)

        self.parameterFrame = VisionLabelFrame(self, text="Information")
        self.parameterFrame.place(relx=0.68, rely=0.65, relwidth=0.31,relheight=0.34)


        image = cv.imdecode(np.fromfile(r'D:\Duc\Document\Project\TSB\FPCB_Inspection\report\ccd_image.png', dtype=np.uint8), cv.IMREAD_COLOR)
        self.ccd_view.showImage(image)
        image = cv.imdecode(np.fromfile(r'D:\Duc\Document\Project\TSB\FPCB_Inspection\report\scan_image.png', dtype=np.uint8), cv.IMREAD_COLOR)
        self.scan_image_view.showImage(image)
        image = cv.imdecode(np.fromfile(r'D:\Duc\Document\Project\TSB\FPCB_Inspection\report\total_image.png', dtype=np.uint8), cv.IMREAD_COLOR)
        self.total_image_view.showImage(image)

    def show(self):
        self.update()
        self.deiconify()
        self.state("zoomed")

        # return
        self.live = True
        ccd_thread = threading.Thread(target=self.ccd_live_threading, args=())
        ccd_thread.start()

    def hide(self):
        self.live = False
        self.mainWindow.show()
        self.withdraw()

    def exit(self):
        self.hide()

    def ccd_live_threading(self):
        while self.live:
            ret, image = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
            if ret:
                self.ccd_view.showImage(image)

