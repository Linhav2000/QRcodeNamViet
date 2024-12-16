import CommonAssit.CommonAssit as CommonAssit
from View.Common.VisionUI import *

class ReferencePositionSelectWindow(VisionTopLevel):

    listPositions = []

    listPosComboBox: ttk.Combobox
    posChosen = 0

    btnClose: CloseButton
    btnOk: Button

    isChosenFlag = False
    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        VisionTopLevel.__init__(self)
        self.mainWindow: MainWindow = mainWindow
        self.windowSetting()
        self.createView()

    def windowSetting(self):
        self.title("Position Selection")
        width = 260
        height = 150
        self.iconbitmap(CommonAssit.resource_path('resource\\appIcon.ico'))
        self.geometry("{}x{}+{}+{}".format(width,
                                           height,
                                           int(self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width() / 2 - width / 2),
                                           int(self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height() / 2 - height / 2)))
        self.resizable(0, 0)
        self.grab_set()

    def createView(self):
        self.listPositions = []
        for idx in range(len(self.mainWindow.workingThread.adjustingScrewPos.pixelDesignPoints)):
            self.listPositions.append("Position {}".format(idx))


        posLabel = VisionLabel(self, text="Position: ")
        posLabel.place(relx=0.05, rely=0.2)
        self.listPosComboBox = ttk.Combobox(self, value=self.listPositions, state='readonly', cursor="hand2")
        self.listPosComboBox.bind("<<ComboboxSelected>>", self.camSelected)
        self.listPosComboBox.place(relx=0.3, rely=0.2)
        self.listPosComboBox.current(0)

        self.btnOk = OkButton(self, command=self.clickBtnOk)
        self.btnOk.place(relx=0.35,rely=0.7, width=80, height=28)

        # self.btnClose = Button(self, text="Close", command=self.destroy)
        # self.btnClose.place(relx=0.55, rely=0.7, width=80)


    def clickBtnOk(self):
        self.isChosenFlag = True
        self.destroy()

    def camSelected(self, event):
        value = self.listPosComboBox.get()
        self.posChosen = int(value[9 : len(value)])
