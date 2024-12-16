from View.Common.VisionUI import *

class Classify_Result_Frame(ResultFrame):
    resultOKLabel: VisionLabel
    resultNGLabel: VisionLabel
    def __init__(self, master):
        ResultFrame.__init__(self, master=master)
        self.setupView()

    def setupView(self):
        self.resultOKLabel = VisionLabel(self, text="Loại 1", fg=Color.okColor(), bg=Color.resultBg(), font=VisionFont.boldFont(45))
        self.resultOKLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.resultNGLabel = VisionLabel(self, text="Loại 2", fg=Color.winBlue(), bg=Color.resultBg(),
                                         font=VisionFont.boldFont(45))
        # self.resultNGLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    def setOK(self):
        self.resultNGLabel.place_forget()
        self.resultOKLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
    def setNG(self):
        self.resultOKLabel.place_forget()
        self.resultNGLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
