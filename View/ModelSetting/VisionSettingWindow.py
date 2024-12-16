import tkinter.messagebox as messagebox
import CommonAssit.CommonAssit as CommonAssit
from View.Common.VisionUI import *


class VisionSettingWindow(VisionTopLevel):

    btnUp: Button
    btnDown: Button

    btnSave: Button
    btnCancel: Button
    screwRecognizeAlgorithmComboBox: ttk.Combobox
    ringRecognizeAlgorithmComboBox: ttk.Combobox
    centerHoleAlgorithmCmb: ttk.Combobox

    algorithmList = ["Contours", "Hough circles"]

    screwRecognizeAlgorithm = "Contours"
    ringRecognizeAlgorithm = "Contours"
    centerHoleAlgorithm = "Contours"

    saveFlag = False

    def __init__(self, mainWindow, model):
        from MainWindow import MainWindow
        from Modules.ModelSetting.ModelParameter import ModelParameter
        self.mainWindow: MainWindow = mainWindow
        VisionTopLevel.__init__(self)
        self.windowSetting()
        self.model: ModelParameter = model
        self.createView()
        self.showLastSetting()

    def windowSetting(self):
        width = 436
        height = 333
        self.title("Vision Setting")
        self.iconbitmap(CommonAssit.resource_path('resource\\appIcon.ico'))
        self.geometry("{}x{}+{}+{}".format(width, height, int
            (self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width( ) /2 - width /2),
                                           int
                                               (self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height( ) /2 - height /2)))
        self.resizable(0, 0)
        self.grab_set()
        # self.protocol("WM_DELETE_WINDOW", self.close)

    def createView(self):
        self.setupButton()
        self.setupAlgorithmChoosing()


    def setupButton(self):
        self.btnSave = SaveButton(self, command=self.clickBtnSave)
        self.btnSave.place(relx = 0.2, rely = 0.8, width=120, height=40)

        self.btnCancel = CancelButton(self, command=self.clickBtnCancel)
        self.btnCancel.place(relx=0.6, rely=0.8, width=120, height=40)

    def setupAlgorithmChoosing(self):
        self.algorithmList = []
        for algorithm in self.mainWindow.algorithmManager.algorithmList:
            self.algorithmList.append(algorithm.algorithmParameter.name)

        label = VisionLabel(self, text="Algorithm for screw recognize : ")
        label.place(x= 10, y= 10)
        self.screwRecognizeAlgorithmComboBox = ttk.Combobox(self, value=self.algorithmList, state="readonly", cursor="hand2")
        self.screwRecognizeAlgorithmComboBox.bind("<<ComboboxSelected>>", self.screwAlgorithmSelected)
        self.screwRecognizeAlgorithmComboBox.place(x=200, y = 10)

        label = VisionLabel(self, text="Algorithm for ring recognize : ")
        label.place(x=10, y=40)
        self.ringRecognizeAlgorithmComboBox = ttk.Combobox(self, value=self.algorithmList, state="readonly", cursor="hand2")
        self.ringRecognizeAlgorithmComboBox.place(x=200, y=40)

        label = VisionLabel(self, text="Algorithm for hole center : ")
        label.place(x=10, y=70)
        self.centerHoleAlgorithmCmb = ttk.Combobox(self, value=self.algorithmList, state="readonly", cursor="hand2")
        self.centerHoleAlgorithmCmb.place(x=200, y=70)


    def screwAlgorithmSelected(self, event):
        self.screwRecognizeAlgorithm = self.screwRecognizeAlgorithmComboBox.get()

    def clickBtnSave(self):
        try:
            self.screwRecognizeAlgorithm = self.screwRecognizeAlgorithmComboBox.get()
            self.ringRecognizeAlgorithm = self.ringRecognizeAlgorithmComboBox.get()
            self.centerHoleAlgorithm = self.centerHoleAlgorithmCmb.get()
            self.saveFlag = True
            self.destroy()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Vision Setting: {}".format(error))
            messagebox.showerror("Save Vision Setting", "Please check the setting values!\nDetail: {}".format(error))
            return

    def clickBtnCancel(self):
        self.destroy()

    def showLastSetting(self):
        try:
            self.screwRecognizeAlgorithmComboBox.current(self.algorithmList.index(self.model.screwRecognizeAlgorithm))
            self.ringRecognizeAlgorithmComboBox.current(self.algorithmList.index(self.model.ringRecognizeAlgorithm))
            self.centerHoleAlgorithmCmb.current(self.algorithmList.index(self.model.centerHoleAlgorithm))
        except:
            pass