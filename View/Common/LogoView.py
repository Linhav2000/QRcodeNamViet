from tkinter import *
from PIL import ImageTk, Image
from CommonAssit import Color

class LogoView(Canvas):

    imageShow = None
    originalImage = None
    def __init__(self, master, image=None, imagePath=None):
        Canvas.__init__(self, master=master, borderwidth=0, highlightthickness=0, bg=Color.visionBg())
        self.bind("<Configure>", self.onResize)
        if image is not None:
            self.originalImage = image.copy()
            self.showImage()
        if imagePath is not None:
            try:
                self.originalImage = Image.open(imagePath)
                self.showImage()
            except:
                pass

    def onResize(self, event):
        # self.showArrayImage(self.originalImage)
        self.showImage()

    def setImage(self, image):
        self.originalImage = image.copy()
        self.showImage()

    def setImagePath(self, imagePath):
        try:
            self.originalImage = Image.open(imagePath)
            self.showImage()
        except:
            pass

    def showImage(self):
        if self.originalImage is None:
            return

        realWidth = self.winfo_width()
        realHeight = self.winfo_height()

        image = self.originalImage.resize((realWidth, realHeight))

        self.imageShow = ImageTk.PhotoImage(image)
        self.create_image(0, 0, anchor=NW, image=self.imageShow)
        self.image = self.imageShow


