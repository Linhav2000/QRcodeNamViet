from tkinter import ttk
from tkinter import *
from View.Running.ResultFrame import ResultFrame
from View.Running.CommonInfoFrame import CommonInfoLabelFrame
from View.MissingMachine.DateInfoFrame import DateInfoFrame
from View.CountingInConveyor.Counting_In_Conveyor_Result_Frame import Counting_In_Conveyor_Result_Frame
from View.Running.DDK.DDK_Result_Frame import DDK_Result_Frame
from View.Running.SYC_Phone_Result_Frame import SYC_Phone_Result_Frame
from View.Running.Classify_Result_Frame import Classify_Result_Frame

class RunningResultTab(Frame):

    logFrame: Frame
    currentResultFrame: ResultFrame = None
    lastResultFrame: ResultFrame = None
    locationDetectResultFrame: DateInfoFrame = None
    commonSettingFrame: CommonInfoLabelFrame = None
    counting_in_conveyor_result_frame: Counting_In_Conveyor_Result_Frame = None
    ddk_result_frame: DDK_Result_Frame = None
    syc_phone_result: SYC_Phone_Result_Frame = None
    classify_frame: Classify_Result_Frame = None
    showed_frame1 = None
    showed_frame2 = None

    def __init__(self, root: ttk.Notebook, mainWindow):
        from MainWindow import MainWindow
        Frame.__init__(self, root, bg="#676767")
        self.root = root
        self.mainWindow: MainWindow = mainWindow

        self.setupView()
        self.pack(fill='both', expand=1)

    def setupView(self):
        self.currentResultFrame = ResultFrame(self, self.mainWindow, "Current Result", isCurrentFrame=True)
        # self.currentResultFrame.place(relx=0, y = 0, relwidth=0.5, relheight=1)

        self.lastResultFrame = ResultFrame(self, self.mainWindow, "Last Result")
        # self.lastResultFrame.place(relx=0.5, y = 0, relwidth=0.5, relheight=1)

        self.locationDetectResultFrame = DateInfoFrame(self, self.mainWindow, "Today result", "LEFT")
        # self.locationDetectResultFrame.place(relx=0, y=0, relwidth=0.4, relheight=1)

        self.commonSettingFrame = CommonInfoLabelFrame(self, "Common Setting", self.mainWindow)
        # self.commonSettingFrame.place(relx=0.5, y=0, relwidth=0.5, relheight=1)

    def setup_ddk_result_frame(self):
        self.ddk_result_frame = DDK_Result_Frame(self, mainWindow=self.mainWindow)
		
    def setup_syc_phone_check_result_frame(self):
        self.syc_phone_result = SYC_Phone_Result_Frame(self, mainWindow=self.mainWindow)
		
    def setup_classify_result_frame(self):
        self.classify_frame = Classify_Result_Frame(self)

    def updateView(self):
        if self.showed_frame1 is not None:
            self.showed_frame1.place_forget()
        if self.showed_frame2 is not None:
            self.showed_frame2.place_forget()

        machineName = self.mainWindow.startingWindow.machineName
        if machineName.isLocationDetect() or machineName.is_demo_color_detect() or machineName.is_demo_location_detect():
            self.showed_frame1 = self.locationDetectResultFrame
            self.showed_frame2 = self.commonSettingFrame
            self.locationDetectResultFrame.place(relx=0, y=0, relwidth=0.4, relheight=1)
            self.commonSettingFrame.place(relx=0.4, y=0, relwidth=0.6, relheight=1)
        elif machineName.is_counting_in_conveyor():
            if self.counting_in_conveyor_result_frame is None:
                self.counting_in_conveyor_result_frame = Counting_In_Conveyor_Result_Frame(self, self.mainWindow,
                                                                                           title="Coconut Counting")
            self.showed_frame1 = self.counting_in_conveyor_result_frame
            self.counting_in_conveyor_result_frame.place(relx=0, y=0, relwidth=1, relheight=1)
        elif machineName.is_ddk_inspection():
            if self.ddk_result_frame is None:
                self.setup_ddk_result_frame()
            self.showed_frame1 = self.ddk_result_frame
            self.ddk_result_frame.place(relx=0, y=0, relwidth=1, relheight=1)

        elif machineName.is_syc_phone_check():
            if self.syc_phone_result is None:
                self.setup_syc_phone_check_result_frame()
            self.showed_frame1 = self.syc_phone_result
            self.syc_phone_result.place(relx=0, rely=0, relwidth=1, relheight=1)
        elif machineName.is_demo_classify():
            if self.classify_frame is None:
                self.setup_classify_result_frame()
            self.showed_frame1 = self.classify_frame
            self.classify_frame.place(relx=0, y=0, relwidth=1, relheight=1)
        else:
            self.showed_frame1 = self.currentResultFrame
            self.showed_frame2 = self.lastResultFrame
            self.currentResultFrame.place(relx=0, y=0, relwidth=0.5, relheight=1)
            self.lastResultFrame.place(relx=0.5, y = 0, relwidth=0.5, relheight=1)

