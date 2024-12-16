from Modules.MachineSetting.MachineList import MachineList
from View.Common.VisionUI import *
from View.StartingSetup.StartingFrame import StartingFrame

class AssemblyMachineFrame(StartingFrame):

    btnFUAssemblyMachine: StartSetupButton
    btnLoadFrameMachine: StartSetupButton

    def __init__(self, master, mainWindow):
        from Vision import StartingWindow
        StartingFrame.__init__(self, master)
        self.mainWindow = mainWindow
        self.startingWindow: StartingWindow = master
        self.setupView()

    def setupView(self):

        # self.btnBack = Button(self, text=self.mainWindow.languageManager.localized("btnBack"), bg="#66CC99", command=self.clickBtnBack)
        self.btnBack = ImageButton(self, imagePath="./resource/back_button.png", command=self.clickBtnBack)
        self.btnBack.place(relx=0.005, rely=0.89, relwidth=0.15, relheight=0.1)

        self.btnFUAssemblyMachine = StartSetupButton(self, text=self.mainWindow.languageManager.localized("btnFUAssemblyMachine"),
                                                         command=lambda: self.startingWindow.startMachine(MachineList.FUAssemblyMachine))
        self.btnFUAssemblyMachine.place(relx=0.1, rely=0.07, relwidth=0.2, relheight=0.2)



        self.btnLoadFrameMachine = StartSetupButton(self, text=self.mainWindow.languageManager.localized("btnLoadFrameMachine"),
                                                  command=lambda: self.startingWindow.startMachine(MachineList.loadFrameMachine))
        self.btnLoadFrameMachine.place(relx=0.4, rely=0.07, relwidth=0.2, relheight=0.2)
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

