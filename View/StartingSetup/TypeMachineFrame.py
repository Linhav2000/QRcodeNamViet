from View.Common.VisionUI import *
from View.StartingSetup.StartingFrame import StartingFrame
from Modules.MachineSetting.MachineList import MachineList

class TypeMachineFrame(StartingFrame):

    btnScrewMachine: StartSetupButton
    btnAssyMachine: StartSetupButton
    btnMissingInspectionMachine: StartSetupButton
    btnDetectLocationMachine: StartSetupButton
    btnRobotMachine: StartSetupButton
    btnBarcodeReadingMachine: StartSetupButton
    btnCheckingMachine: StartSetupButton
    InspectionMachine: StartSetupButton


    def __init__(self, master, mainWindow):
        from Vision import StartingWindow
        StartingFrame.__init__(self, master)
        self.mainWindow = mainWindow
        self.startingWindow: StartingWindow = master
        self.setupView()

    def setupView(self):
        self.setupChosenMachineFrame()

    def setupChosenMachineFrame(self):
        if self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.filterCoverScrewMachine.value \
            or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.RUConnectorScrewMachine.value:

            self.btnScrewMachine = StartSetupButton(self, text=self.mainWindow.languageManager.localized("screwMachine"),
                                                    command=self.startingWindow.showScrewMachineFrame)
            self.btnScrewMachine.place(relx=0.1, rely=0.07, relwidth=0.2, relheight=0.2)

        elif self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.FUAssemblyMachine.value \
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.loadFrameMachine.value:
            self.btnAssyMachine = StartSetupButton(self, text=self.mainWindow.languageManager.localized("assyMachine"),
                                                   command=self.startingWindow.showAssemblyMachineFrame)
            self.btnAssyMachine.place(relx=0.4, rely=0.07, relwidth=0.2, relheight=0.2)

        elif self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.rearMissingInspectionMachine.value \
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.housing_connector_packing.value :
            self.btnMissingInspectionMachine = StartSetupButton(self, text=self.mainWindow.languageManager.localized("missingMachine"),
                                                                command=self.startingWindow.showMissingMachineFrame)
            self.btnMissingInspectionMachine.place(relx=0.7, rely=0.07, relwidth=0.2, relheight=0.2)

        elif self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.locationDetect.value \
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.demo_counting.value \
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.demo_focus_checking.value \
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.demo_classify.value \
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.demo_circle_measurement.value \
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.demo_line_measurement.value \
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.demo_location_detect.value \
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.demo_color_detect.value:

            self.btnDetectLocationMachine = StartSetupButton(self, text="Demo",
                                                             command=self.startingWindow.showDemoFrame)
            self.btnDetectLocationMachine.place(relx=0.1, rely=0.34, relwidth=0.2, relheight=0.2)

        elif self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.fpc_inspection.value\
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.fpc_verify.value \
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.ddk_inspection.value \
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.washing_machine_inspection.value \
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.syc_phone_check.value:
            self.InspectionMachine = StartSetupButton(self, text="Inspection",
                                                      command=self.startingWindow.showInspectionMachineFrame)
            self.InspectionMachine.place(relx=0.7, rely=0.34, relwidth=0.2, relheight=0.2)

        elif self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.hik_barcode_demo.value \
                or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.reading_weighing.value:
            self.btnBarcodeReadingMachine = StartSetupButton(self, text="Reading",
                                                             command=self.startingWindow.showReadingFrame)
            self.btnBarcodeReadingMachine.place(relx=0.1, rely=0.61, relwidth=0.2, relheight=0.2)

        elif self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.e_map_checking.value \
            or self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.counting_in_conveyor.value:
            self.btnCheckingMachine = StartSetupButton(self, text="Checking",
                                                       command=self.startingWindow.showCheckingMachineFrame)
            self.btnCheckingMachine.place(relx=0.4, rely=0.61, relwidth=0.2, relheight=0.2)

        elif self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.roto_weighing.value:
            self.btnRobotMachine = StartSetupButton(self, text="Robot",
                                                             command=self.startingWindow.showRobotFrame)
            self.btnRobotMachine.place(relx=0.4, rely=0.34, relwidth=0.2, relheight=0.2)

        elif self.mainWindow.commonSettingManager.settingParm.currentMachine == MachineList.all.value:
            self.btnScrewMachine = StartSetupButton(self, text=self.mainWindow.languageManager.localized("screwMachine"),
                                                    command=self.startingWindow.showScrewMachineFrame)
            self.btnScrewMachine.place(relx=0.1, rely=0.07, relwidth=0.2, relheight=0.2)

            self.btnAssyMachine = StartSetupButton(self, text=self.mainWindow.languageManager.localized("assyMachine"),
                                                   command=self.startingWindow.showAssemblyMachineFrame)
            self.btnAssyMachine.place(relx=0.4, rely=0.07, relwidth=0.2, relheight=0.2)

            self.btnMissingInspectionMachine = StartSetupButton(self, text=self.mainWindow.languageManager.localized("missingMachine"),
                                                                command=self.startingWindow.showMissingMachineFrame)
            self.btnMissingInspectionMachine.place(relx=0.7, rely=0.07, relwidth=0.2, relheight=0.2)

            self.btnDetectLocationMachine = StartSetupButton(self, text="Demo",
                                                             command=self.startingWindow.showDemoFrame)
            self.btnDetectLocationMachine.place(relx=0.1, rely=0.34, relwidth=0.2, relheight=0.2)

            self.btnRobotMachine = StartSetupButton(self, text="Robot",
                                                             command=self.startingWindow.showRobotFrame)
            self.btnRobotMachine.place(relx=0.4, rely=0.34, relwidth=0.2, relheight=0.2)

            self.InspectionMachine = StartSetupButton(self, text="Inspection",
                                                      command=self.startingWindow.showInspectionMachineFrame)
            self.InspectionMachine.place(relx=0.7, rely=0.34, relwidth=0.2, relheight=0.2)

            self.btnBarcodeReadingMachine = StartSetupButton(self, text="Reading",
                                                             command=self.startingWindow.showReadingFrame)
            self.btnBarcodeReadingMachine.place(relx=0.1, rely=0.61, relwidth=0.2, relheight=0.2)

            self.btnCheckingMachine = StartSetupButton(self, text="Checking",
                                                       command=self.startingWindow.showCheckingMachineFrame)
            self.btnCheckingMachine.place(relx=0.4, rely=0.61, relwidth=0.2, relheight=0.2)

    def hide(self):
        self.place_forget()
