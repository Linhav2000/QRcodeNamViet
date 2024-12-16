from tkinter import *
from CommonAssit import CommonAssit
from CommonAssit import Color
import cv2 as cv
import numpy as np

class ImageView(Canvas):
    currentImage = None
    widthCoef = 1
    heightCoef = 1
    leftMousePressCmd = None
    imageId = None

    def __init__(self, master, mainWindow, leftMousePressCmd=None, imageId=None):
        Canvas.__init__(self, master, highlightbackground="#005500", highlightthickness=2, bg=Color.resultBg())
        self.mainWindow = mainWindow
        self.leftMousePressCmd = leftMousePressCmd
        self.imageId = imageId
        self.setupEvent()
        photo = cv.imdecode(np.fromfile("./resource/photo.png", dtype=np.uint8), cv.IMREAD_COLOR)
        self.showImage(image=photo)

    def setupEvent(self):
        self.bind("<Configure>", self.onImageViewResize)
        self.bind("<Button-1>", self.mouseEvent)

    def showImage(self, image=None):
        if image is None:
            photo = cv.imdecode(np.fromfile("./resource/photo.png", dtype=np.uint8), cv.IMREAD_COLOR)
            self.showImage(image=photo)
            return

        self.currentImage = image.copy()
        CommonAssit.showArrayImage(image, self)

        shape = self.currentImage.shape
        self.widthCoef = shape[1] / self.winfo_width()
        self.heightCoef = shape[0] / self.winfo_height()

    def onImageViewResize(self, event):
        if hasattr(self, "currentImage") and self.currentImage is not None:
            self.showImage(self.currentImage)

    def mouseEvent(self, event):

        if event.type == EventType.ButtonPress and event.num == 1:
            # left button press
            if self.leftMousePressCmd is not None:
                if self.imageId is None:
                    self.leftMousePressCmd()
                else:
                    self.leftMousePressCmd(self.imageId)