from Modules.MachineSetting.MachineList import MachineList
from View.Common.VisionUI import *
from View.StartingSetup.StartingFrame import StartingFrame

class RobotFrame(StartingFrame):

    def __init__(self, master, mainWindow):
        from Vision import StartingWindow
        StartingFrame.__init__(self, master)
        self.mainWindow = mainWindow
        self.startingWindow: StartingWindow = master
        self.setupView()

    btnRotoWeighingMachine: Button
    def setupView(self):

        self.btnBack = ImageButton(self, imagePath="./resource/back_button.png", command=self.clickBtnBack)
        self.btnBack.place(relx=0.005, rely=0.89, relwidth=0.15, relheight=0.1)

        self.btnRotoWeighingMachine = StartSetupButton(self, text="Roto Weighing",
                                                       command=lambda: self.startingWindow.startMachine(MachineList.roto_weighing))
        self.btnRotoWeighingMachine.place(relx=0.1, rely=0.07, relwidth=0.2, relheight=0.2)

        # self.btnDemoColorDetect = StartSetupButton(self, text="Color Detect",
        #                                           command=lambda: self.startingWindow.startMachine(MachineList.demo_color_detect))
        # self.btnDemoColorDetect.place(relx=0.4, rely=0.07, relwidth=0.2, relheight=0.2)
        #
        # self.btnDemoLocationDetect = StartSetupButton(self, text="Demo Location",
        #                                               command=lambda: self.startingWindow.startMachine(MachineList.demo_location_detect))
        # self.btnDemoLocationDetect.place(relx=0.7, rely=0.07, relwidth=0.2, relheight=0.2)

    def clickBtnBack(self):
        self.hide()
        self.startingWindow.showTypeMachineFrame()

    def hide(self):
        self.place_forget()