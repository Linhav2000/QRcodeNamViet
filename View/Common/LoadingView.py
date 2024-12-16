from View.Common.VisionUI import *
from View.Common.AnimationView import AnimationView
from multiprocessing import process

class LoadingView(VisionTopLevel):
    isLoading = False
    loadingLbl: VisionLabel
    loadingFrame: VisionFrame
    animationView: AnimationView
    def __init__(self, parent=None, mainWindow=None, text=""):
        VisionTopLevel.__init__(self)
        self.mainWindow = mainWindow
        self.parent = parent
        self.text = text
        self.setupWindow()
        self.setupView()
        # _thread.start_new_thread(self.loadingThread, ())

    def setupWindow(self):
        self.title("Loading")
        width = 389
        height = 389
        try:
            self.iconbitmap('./resource/appIcon.ico')
        except:
            pass
        self.overrideredirect(True)
        if self.parent is not None:
            self.geometry("{}x{}+{}+{}".format(width, height,
                                               int(self.parent.winfo_x() + self.parent.winfo_width() / 2 - width / 2),
                                               int(self.parent.winfo_y() + self.parent.winfo_height() / 2 - height / 2)))
        else:
            self.geometry("{}x{}".format(width, height))
        self.resizable(0, 0)
        self.grab_set()

    def setupView(self):
        self.loadingLbl = VisionLabel(self, text=self.text, font=VisionFont.boldFont(20), fg=Color.winWhite())
        self.loadingLbl.place(relx=0, rely=0.75, relwidth=1, relheight=0.23)

        self.animationView = AnimationView(self, imagePath="./resource/loading.gif")
        self.animationView.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.6)

    def done(self):
        self.isLoading = False
        self.animationView.stop()
        self.destroy()

