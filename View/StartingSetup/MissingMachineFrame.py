from Modules.MachineSetting.MachineList import MachineList
from View.Common.VisionUI import *
from View.StartingSetup.StartingFrame import StartingFrame

class MissingMachineFrame(StartingFrame):

    def __init__(self, master, mainWindow):
        from Vision import StartingWindow
        StartingFrame.__init__(self, master)
        self.mainWindow = mainWindow
        self.startingWindow: StartingWindow = master
        self.setupView()

    btnRearMachine: StartSetupButton
    btnFilterScrewMachine: Button
    btnHousePacking: StartSetupButton
    def setupView(self):

        self.btnBack = ImageButton(self, imagePath="./resource/back_button.png", command=self.clickBtnBack)
        self.btnBack.place(relx=0.005, rely=0.89, relwidth=0.15, relheight=0.1)

        self.btnRearMachine = StartSetupButton(self, text=self.mainWindow.languageManager.localized("btnRearMissingMachine"),
                                               command=lambda: self.startingWindow.startMachine(MachineList.rearMissingInspectionMachine))
        self.btnRearMachine.place(relx=0.1, rely=0.07, relwidth=0.2, relheight=0.2)

        self.btnHousePacking = StartSetupButton(self, text="Housing Connector Packing",
                                               command=lambda: self.startingWindow.startMachine(MachineList.housing_connector_packing))
        self.btnHousePacking.place(relx=0.4, rely=0.07, relwidth=0.2, relheight=0.2)

        # self.btnFilterScrewMachine = StartSetupButton(self, text=self.mainWindow.languageManager.localized("btnFilterScrewMachine"),
        #                                           command=lambda: self.startingWindow.startMachine(MachineList.filterCoverScrewMachine))
        # self.btnFilterScrewMachine.place(relx=0.55, rely=0.1, relwidth=0.3, relheight=0.3)
        #
        # self.btnMissingInspectionMachine = StartSetupButton(self, text=self.mainWindow.languageManager.localized(
        #     "missingMachine"),
        #                                                     command=lambda: self.clickButton("missing"))
        # self.btnMissingInspectionMachine.place(relx=0.15, rely=0.5, relwidth=0.3, relheight=0.3)

    def clickBtnBack(self):
        self.hide()
        self.startingWindow.showTypeMachineFrame()

    def hide(self):
        self.place_forget()
