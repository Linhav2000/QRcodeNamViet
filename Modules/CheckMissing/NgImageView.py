from View.Common.ImageView import ImageView
import cv2 as cv
import numpy as np

class NgImageView:
    imageLeft = None
    imageRight = None
    imageLeftView: ImageView = None
    imageRightView: ImageView = None
    cvPhoto = cv.imdecode(np.fromfile("./resource/photo.png", dtype=np.uint8), cv.IMREAD_COLOR)

    def __init__(self, mainWindow, imageLeftView, imageRightView):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow
        self.imageLeftView = imageLeftView
        self.imageRightView = imageRightView
        self.imageLeftView.leftMousePressCmd = self.showLeftImage
        self.imageRightView.leftMousePressCmd = self.showRightImage

    def setImage(self, leftImage, rightImage):
        self.setLeftImage(leftImage)
        self.setRightImage(rightImage)

    def setLeftImage(self, image):
        if image is not None:
            self.imageLeft = image.copy()
        else:
            self.imageLeft = self.cvPhoto.copy()

        self.imageLeftView.showImage(self.imageLeft)

    def setRightImage(self, image):
        if image is not None:
            self.imageRight = image.copy()
        else:
            self.imageRight = self.cvPhoto.copy()
        self.imageRightView.showImage(self.imageRight)


    def showLeftImage(self):
        self.mainWindow.checkMissingWindow.leftFrame.showImage(self.imageLeft)

    def showRightImage(self):
        self.mainWindow.checkMissingWindow.rightFrame.showImage(self.imageRight)
