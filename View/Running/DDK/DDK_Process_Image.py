import numpy
from View.Common.VisionUI import *
from View.Common.ImageView import ImageView
import threading

class DDK_Process_Image(VisionFrame):
    listSmallImageView: [ImageView] = []
    listImages = []
    rec_frame_list = []
    label_list = []
    stateList = 0
    last_id = 0
    row = 4
    column = 6
    def __init__(self, master, mainWindow):
        from MainWindow import MainWindow
        VisionFrame.__init__(self, master=master)
        self.mainWindow: MainWindow = mainWindow
        self.setupView()

    def setupView(self):

        rec_align = 0.002
        imageView_align = 0.03
        imageViewHeight = 0.8
        labelHeight = 1 - imageViewHeight - 2*imageView_align
        relHeight = 1/self.row - rec_align*2
        relWidth = 1/self.column - rec_align*2
        self.rec_frame_list = []
        self.listSmallImageView = []
        self.label_list = []
        self.stateList = numpy.zeros(shape=self.row * self.column, dtype=numpy.int_)
        for i in range(self.row * self.column):
            self.rec_frame_list.append(VisionFrame(self, bg=Color.winSaddleBrown()))
            self.rec_frame_list[i].place(relx=(i%self.column)/self.column + rec_align, rely=int(i/self.column)/self.row+rec_align, relwidth=relWidth, relheight=relHeight)
            self.listSmallImageView.append(ImageView(self.rec_frame_list[i], self.mainWindow, leftMousePressCmd=self.smallImageViewClick, imageId=i))
            self.listSmallImageView[i].place(relx=imageView_align, rely=imageView_align, relwidth=1-2*imageView_align, relheight=imageViewHeight)
            #
            self.label_list.append(VisionLabel(self.rec_frame_list[i], text=f"Step {i + 1}", fg=Color.winSaddleBrown()))
            self.label_list[i].place(relx=imageView_align, rely=imageViewHeight+imageView_align, relwidth=1-2*imageView_align, relheight=labelHeight)


    def smallImageViewClick(self, id):
        self.mainWindow.showImage(self.listSmallImageView[id].currentImage, title=f"Step {id + 1}")
        self.rec_frame_list[id].config(bg=Color.winMagenta())

        if self.last_id != id:
            if self.stateList[self.last_id] == 1:
                self.rec_frame_list[self.last_id].config(bg=Color.winLame())
            elif self.stateList[self.last_id] == 2:
                self.rec_frame_list[self.last_id].config(bg=Color.winRed())
            else:
                self.rec_frame_list[self.last_id].config(bg=Color.winSaddleBrown())

            self.last_id = id

    def add_step_image(self, step, image, state):
        print(f"step = {step}")
        add_step_image_thread = threading.Thread(target=self.add_step_image_thread, args=(step, image, state))
        add_step_image_thread.start()

    def add_step_image_thread(self,step, image, state):
        self.stateList[step - 1] = state
        self.listSmallImageView[step - 1].showImage(image.copy())
        if state == 1:
            self.label_list[step - 1].config(fg=Color.winLame())
        elif state == 2:
            self.label_list[step - 1].config(fg=Color.winRed())
        self.smallImageViewClick(step - 1)

    def reset_product_circle(self):
        self.stateList = numpy.zeros(shape=self.row * self.column, dtype=numpy.int)
        for i in range(self.row * self.column):
            self.listSmallImageView[i].showImage()
            self.rec_frame_list[i].config(bg=Color.winSaddleBrown())
            self.label_list[i].config(fg=Color.winSaddleBrown())


