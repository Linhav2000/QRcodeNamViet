from View.Common.VisionUI import *
from View.Common.ImageView import ImageView
from View.FPC_Inspection.Show_Result_Frame import Show_Result_Frame
class FPC_Inspection_Run_Window(VisionTopLevel):

    mainImageView: ImageView
    stateLabel: Label
    listImages = []
    listSmallImageView = []
    totalFrame: Show_Result_Frame
    okFrame: Show_Result_Frame
    ngFrame: Show_Result_Frame
    num_OK = 0
    num_NG = 0
    num_total = 0

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        VisionTopLevel.__init__(self)
        self.mainWindow: MainWindow = mainWindow
        self.setupWindow()

    def setupWindow(self):
        self.setupMainWindow()
        self.setupView()
        self.hide()

    def setupMainWindow(self):
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
        relHeight = 0.1
        relWidth = 0.08
        self.mainImageView = ImageView(self, self.mainWindow)
        self.mainImageView.place(relx=0, rely=0, relwidth=0.77, relheight=1)

        self.stateLabel = Label(self, font=VisionFont.boldFont(36), bg="#F8C471", text="OK", fg="#00FF00")
        self.stateLabel.place(relx=0, rely=0.91,relheight=0.09, width=200)

        for i in range(10):
            self.listSmallImageView.append(ImageView(self, self.mainWindow, leftMousePressCmd=self.smallImageViewClick, imageId=i))

        for i in range(10):
            self.listSmallImageView[i].place(relx=0.77, rely=i * relHeight, relwidth=relWidth, relheight=relHeight)
            self.listImages.append(None)

        self.totalFrame = Show_Result_Frame(self, color="#000000", text="Total")
        self.totalFrame.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.23)

        self.okFrame = Show_Result_Frame(self, color="#00FF00", text="OK")
        self.okFrame.place(relx=0.85, rely= 1 * 0.23, relwidth=0.15, relheight=0.23)

        self.ngFrame = Show_Result_Frame(self, color="#FF0000", text="NG")
        self.ngFrame.place(relx=0.85, rely= 2 * 0.23, relwidth=0.15, relheight=0.23)

        self.totalFrame.setValue(0)
        self.okFrame.setValue(0)
        self.ngFrame.setValue(0)

    def smallImageViewClick(self, id):
        self.mainImageView.showImage(self.listSmallImageView[id].currentImage)

    def showImage(self, image, state=True):
        if state:
            self.num_OK += 1
            self.stateLabel.config(text="OK", fg="#00FF00")
        else:
            self.num_NG += 1
            self.stateLabel.config(text="NG", fg="#FF0000")

        self.num_total += 1
        self.show_parameter()
        self.mainImageView.showImage(image)
        self.listImages.pop()
        self.listImages.insert(0, image)

        for i in range(len(self.listImages)):
            if self.listImages[i] is not None:
                self.listSmallImageView[i].showImage(self.listImages[i])

    def show_parameter(self):
        self.okFrame.setValue(self.num_OK)
        self.ngFrame.setValue(self.num_NG)
        self.totalFrame.setValue(self.num_total)

    def show(self):
        self.update()
        self.deiconify()
        self.state("zoomed")

    def hide(self):
        self.mainWindow.show()
        self.withdraw()

    def exit(self):
        self.mainWindow.workingThread.cameraManager.currentCamera.trigger = False
        self.hide()