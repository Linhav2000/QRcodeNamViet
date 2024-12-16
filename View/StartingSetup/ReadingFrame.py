from Modules.MachineSetting.MachineList import MachineList
from View.Common.VisionUI import *
from View.StartingSetup.StartingFrame import StartingFrame

class ReadingFrame(StartingFrame):
    btn_hik_barcode_demo: StartSetupButton
    btn_reading_weighing: StartSetupButton
    btnBack: ImageButton

    def __init__(self, master, mainWindow):
        from Vision import StartingWindow
        StartingFrame.__init__(self, master)
        self.mainWindow = mainWindow
        self.startingWindow: StartingWindow = master
        self.setupView()


    def setupView(self):

        self.btnBack = ImageButton(self, imagePath="./resource/back_button.png", command=self.clickBtnBack)
        self.btnBack.place(relx=0.005, rely=0.89, relwidth=0.15, relheight=0.1)

        self.btn_hik_barcode_demo = StartSetupButton(self, text="Hik Barcode demo",
                                                     command=lambda: self.startingWindow.startMachine(MachineList.hik_barcode_demo))
        self.btn_hik_barcode_demo.place(relx=0.1, rely=0.07, relwidth=0.2, relheight=0.2)

        self.btn_reading_weighing = StartSetupButton(self, text="Reading Weighing",
                                                     command=lambda: self.startingWindow.startMachine(
                                                         MachineList.reading_weighing))
        self.btn_reading_weighing.place(relx=0.4, rely=0.07, relwidth=0.2, relheight=0.2)


    def clickBtnBack(self):
        self.hide()
        self.startingWindow.showTypeMachineFrame()

    def hide(self):
        self.place_forget()