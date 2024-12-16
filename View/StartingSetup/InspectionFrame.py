from Modules.MachineSetting.MachineList import MachineList
from View.Common.VisionUI import *
from View.StartingSetup.StartingFrame import StartingFrame

class InspectionFrame(StartingFrame):
    btn_fpc_inspection: StartSetupButton
    btn_fpc_verify: StartSetupButton
    btn_ddk_inspection: StartSetupButton
    btn_washing_machine_inspection: StartSetupButton
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

        self.btn_fpc_inspection = StartSetupButton(self, text="FPC Inspection",
                                                  command=lambda: self.startingWindow.startMachine(MachineList.fpc_inspection))
        self.btn_fpc_inspection.place(relx=0.1, rely=0.07, relwidth=0.2, relheight=0.2)

        self.btn_fpc_verify = StartSetupButton(self, text="FPC Verify",
                                                   command=lambda: self.startingWindow.startMachine(
                                                       MachineList.fpc_verify))
        self.btn_fpc_verify.place(relx=0.1, rely=0.34, relwidth=0.2, relheight=0.2)


        self.btn_ddk_inspection = StartSetupButton(self, text="DDK Inspection",
                                                   command=lambda: self.startingWindow.startMachine(
                                                       MachineList.ddk_inspection))
        self.btn_ddk_inspection.place(relx=0.4, rely=0.07, relwidth=0.2, relheight=0.2)

        self.btn_syc_phone_inspection = StartSetupButton(self, text="SYC Phone Inspection",
                                                   command=lambda: self.startingWindow.startMachine(
                                                       MachineList.syc_phone_check)) #lệnh gọi ctrinh sẽ chạy
        self.btn_syc_phone_inspection.place(relx=0.4, rely=0.34, relwidth=0.2, relheight=0.2)#nút bấm chọn ctrinh sẽ chạy

        self.btn_washing_machine_inspection = StartSetupButton(self, text="Washing Machine",
                                                   command=lambda: self.startingWindow.startMachine(
                                                       MachineList.washing_machine_inspection))
        self.btn_washing_machine_inspection.place(relx=0.7, rely=0.07, relwidth=0.2, relheight=0.2)


    def clickBtnBack(self):
        self.hide()
        self.startingWindow.showTypeMachineFrame()

    def hide(self):
        self.place_forget()