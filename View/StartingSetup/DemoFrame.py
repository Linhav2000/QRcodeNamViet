from Modules.MachineSetting.MachineList import MachineList
from View.Common.VisionUI import *
from View.StartingSetup.StartingFrame import StartingFrame

class DemoFrame(StartingFrame):
    btnLocationDetect: Button

    btnDemo_Counting: StartSetupButton
    btnDemo_line_measurement: StartSetupButton
    btnDemo_circle_measurement: StartSetupButton
    btnDemoColorDetect: StartSetupButton
    btnDemoLocationDetect: StartSetupButton
    btnDemo_focus_checking: StartSetupButton
    btnDemo_classify: StartSetupButton
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

        self.btnLocationDetect = StartSetupButton(self, text="Location dectect",
                                                  command=lambda: self.startingWindow.startMachine(MachineList.locationDetect))
        self.btnLocationDetect.place(relx=0.1, rely=0.07, relwidth=0.2, relheight=0.2)

        self.btnDemoColorDetect = StartSetupButton(self, text="Color Detect",
                                                  command=lambda: self.startingWindow.startMachine(MachineList.demo_color_detect))
        self.btnDemoColorDetect.place(relx=0.4, rely=0.07, relwidth=0.2, relheight=0.2)

        self.btnDemoLocationDetect = StartSetupButton(self, text="Demo Location",
                                                      command=lambda: self.startingWindow.startMachine(MachineList.demo_location_detect))
        self.btnDemoLocationDetect.place(relx=0.7, rely=0.07, relwidth=0.2, relheight=0.2)

        self.btnDemo_Counting = StartSetupButton(self, text=MachineList.demo_counting.value,
                                                  command=lambda: self.startingWindow.startMachine(
                                                      MachineList.demo_counting))
        self.btnDemo_Counting.place(relx=0.1, rely=0.34, relwidth=0.2, relheight=0.2)

        self.btnDemo_line_measurement = StartSetupButton(self, text=MachineList.demo_line_measurement.value,
                                                   command=lambda: self.startingWindow.startMachine(
                                                       MachineList.demo_line_measurement))
        self.btnDemo_line_measurement.place(relx=0.4, rely=0.34, relwidth=0.2, relheight=0.2)

        self.btnDemo_circle_measurement = StartSetupButton(self, text=MachineList.demo_circle_measurement.value,
                                                      command=lambda: self.startingWindow.startMachine(
                                                          MachineList.demo_circle_measurement))
        self.btnDemo_circle_measurement.place(relx=0.7, rely=0.34, relwidth=0.2, relheight=0.2)

        self.btnDemo_focus_checking = StartSetupButton(self, text=MachineList.demo_focus_checking.value,
                                                           command=lambda: self.startingWindow.startMachine(
                                                               MachineList.demo_focus_checking))
        self.btnDemo_focus_checking.place(relx=0.1, rely=0.61, relwidth=0.2, relheight=0.2)

        self.btnDemo_classify = StartSetupButton(self, text=MachineList.demo_classify.value,
                                                       command=lambda: self.startingWindow.startMachine(
                                                           MachineList.demo_classify))
        self.btnDemo_classify.place(relx=0.4, rely=0.61, relwidth=0.2, relheight=0.2)

    def clickBtnBack(self):
        self.hide()
        self.startingWindow.showTypeMachineFrame()

    def hide(self):
        self.place_forget()