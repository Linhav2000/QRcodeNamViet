from View.Common.VisionUI import *
from View.Common.LogoView import LogoView

class StartingFrame(VisionFrame):

    def __init__(self, master = None, **kw):
        VisionFrame.__init__(self, master=master, **kw)

        self.logoView = LogoView(self, imagePath="./resource/logo.png")
        self.logoView.place(relx=0.41, rely=0.80, relwidth=0.58,relheight=0.19)