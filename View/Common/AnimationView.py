from tkinter import *

import cv2
from PIL import Image, ImageTk
import copy
from View.Common.VisionUI import *

class AnimationView(Canvas):
    imageShow = None
    imagePath = None
    frames = []
    loadingFlag = True
    delay = 100
    index = 0
    def __init__(self, master, imagePath=None):
        Canvas.__init__(self, master=master, borderwidth=0, highlightthickness=0, bg=Color.visionBg())
        self.bind("<Configure>", self.onResize)
        if imagePath is not None:
            self.imagePath = imagePath
            self.createFrame()
        self._play()

    def createFrame(self):
        self.frames = []
        imageGif = Image.open(self.imagePath)
        seq = []
        try:
            while 1:
                seq.append(imageGif.copy())
                imageGif.seek(len(seq))  # skip to next frame
        except EOFError:
            pass  # we're done

        try:
            self.delay = imageGif.info['duration']
        except KeyError:
            self.delay = 100

        for image in seq:
            resizeImage = self.resizeImage(image)
            self.frames.append(copy.deepcopy(resizeImage))

    def resizeImage(self, image):
        realWidth = self.winfo_width()
        realHeight = self.winfo_height()

        imageResize = image.resize((realWidth, realHeight))
        return imageResize

    def play(self):
        if len(self.frames) < 1:
            self.cancel = self.after(self.delay, self.play)
            return

        if self.index >= (len(self.frames) - 2):
            self.index = 0
        else:
            self.index += 1
        imageShow = self.frames[self.index]

        self.showImage(image=imageShow)

        self.cancel = self.after(self.delay, self.play)
    def _play(self):
        self.loadingFlag = True
        while self.loadingFlag:
            if len(self.frames) < 1:
                cv2.waitKey(self.delay)
                continue
            if self.index >= (len(self.frames) - 2):
                self.index = 0
            else:
                self.index += 1
            imageShow = self.frames[self.index]

            self.showImage(image=imageShow)
            cv2.waitKey(self.delay)

    def stop(self):
        self.loadingFlag = False
        # self.after_cancel(self.cancel)

    def onResize(self, event):
        self.createFrame()

    def setImage(self, filePath):
        self.imagePath = filePath
        self.createFrame()

    def showImage(self, image):
        self.imageShow = ImageTk.PhotoImage(image.copy())
        self.create_image(0, 0, anchor=NW, image=self.imageShow)
        self.image = self.imageShow