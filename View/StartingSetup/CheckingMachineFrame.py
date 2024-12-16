from Modules.MachineSetting.MachineList import MachineList
from View.Common.VisionUI import *
from View.StartingSetup.StartingFrame import StartingFrame

class CheckingMachineFrame(StartingFrame):
    btn_emap_checking: StartSetupButton
    btn_counting_in_conveyor: StartSetupButton

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

        self.btn_emap_checking = StartSetupButton(self, text="EMAP Checking",
                                                     command=lambda: self.startingWindow.startMachine(MachineList.e_map_checking))
        self.btn_emap_checking.place(relx=0.1, rely=0.07, relwidth=0.2, relheight=0.2)

        self.btn_counting_in_conveyor = StartSetupButton(self, text="Counting In Conveyor",
                                                  command=lambda: self.startingWindow.startMachine(
                                                      MachineList.counting_in_conveyor))
        self.btn_counting_in_conveyor.place(relx=0.4, rely=0.07, relwidth=0.2, relheight=0.2)

    def clickBtnBack(self):
        self.hide()
        self.startingWindow.showTypeMachineFrame()

    def hide(self):
        self.place_forget()