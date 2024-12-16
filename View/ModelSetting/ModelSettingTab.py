from __future__ import print_function
import tkinter.filedialog
from View.ModelSetting.NewModelView import NewModelView
from CommonAssit.FileManager import CsvFile
from CommonAssit import CommunicationReceiveAnalyze
from CommonAssit.CommunicationReceiveAnalyze import CommunicationReceiveInfo
from View.ModelSetting.ActivePointAdvanceSettingView import ActivePointAdvanceSettingView
from Modules.ModelSetting.ModelManager import ModelManager
from Modules.ModelSetting.ModelParameter import ModelParameter
from Modules.ModelSetting.NumOfRefPoint import NumOfRefPoint
from View.ModelSetting.VisionSettingWindow import VisionSettingWindow
from View.ModelSetting.RearCheckMissingFrame import RearCheckMissingFrame
from View.ModelSetting.LocationDetectSettingFrame import LocationDetectSettingFrame
from View.ModelSetting.DemoColorDetectSettingFrame import DemoColorDetectSettingFrame
from View.ModelSetting.DemoLocationDetectSettingFrame import DemoLocationDetectSettingFrame
from View.ModelSetting.RoboWeighingRobot.RotoWeghingSettingModelFrame import RotoWeighingSettingModelFrame
from View.ModelSetting.FPC_Inspection.FPC_Inspection_Model_Setting_Frame import FPC_Inspection_Model_Setting_Frame
from View.ModelSetting.DDK_Inspection.DDK_Inspection_Model_Setting import DDK_Inspection_Model_Setting
from View.ModelSetting.SYC_Inspection.SYC_Model_Setting import SYC_Model_Setting
# from ImageProcess.MachineProcess.SYC_Inspection import SYC_Inspection
from View.ModelSetting.Fu_Assy_SettingFrame import Fu_Assy_Setting_Frame
from View.ModelSetting.ScrewParameterTab import ScrewParameterTab
from View.ModelSetting.BarcodeReading.HikBarcodeDemoSetting import HikBarcodeDemoSetting
from View.ModelSetting.E_map.E_Map_Model_Setting import E_Map_Model_Setting
from View.ModelSetting.HousingConnectorPacking.THCP_Model_Setting import THCP_Model_Setting
from View.ModelSetting.Reading_Weighing.Read_Weighing_Model_Setting import Read_Weighing_Model_Setting
from View.ModelSetting.CountingInConveyor.Counting_In_Conveyor_Setting import Counting_In_Conveyor_Setting
from View.ModelSetting.WashingMachineInspection.WM_Inspection_Model_Setting import WM_Inspection_Model_Setting
from Connection.SocketManager import SocketClientManager
from ImageProcess import ImageProcess
from CommonAssit import PathFileControl
from CommonAssit import TimeControl
import copy
from View.Common.VisionUI import *
import math
try: from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace

from tkinter import messagebox

class ModelSettingTab(VisionFrame):
    btnAddNewModel: AddButton = None
    btnSave: SaveButton = None
    btnDelete: DeleteButton = None
    btnTakeCoefficient: VisionButton = None
    screwParameterFrame: VisionLabelFrame = None
    rearCheckMissingFrame: RearCheckMissingFrame = None
    screwParameterFrame1: ScrewParameterTab = None
    locationDetectSettingFrame: LocationDetectSettingFrame = None
    demo_color_detect_setting_frame: DemoColorDetectSettingFrame = None
    demo_location_detect_setting_frame: DemoLocationDetectSettingFrame = None
    hik_barcode_demo_setting: HikBarcodeDemoSetting = None
    e_map_model_setting: E_Map_Model_Setting = None
    thcp_model_setting: THCP_Model_Setting = None
    read_weighing_model_setting: Read_Weighing_Model_Setting = None
    roto_weighing_robot_model_setting_frame: RotoWeighingSettingModelFrame = None
    fu_assy_Frame: Fu_Assy_Setting_Frame = None
    fpc_inspection_frame: FPC_Inspection_Model_Setting_Frame = None
    ddk_inspection_frame: DDK_Inspection_Model_Setting = None
    counting_in_conveyor_setting: Counting_In_Conveyor_Setting = None
    wm_inspection_model_setting: WM_Inspection_Model_Setting = None
    syc_model_setting_frame:SYC_Model_Setting = None
    # syc_inspection : SYC_Inspection = None


    currentSettingFrame = None

    modelNameList = []
    modelList = []
    modelComboBox: ttk.Combobox
    startTakeCoefFlag = False
    getOffsetFlag = False
    startCaliOffsetFlag = False
    modelTestFlag = False
    startTakeRuCoefFlag = False
    startTakeFuCoefFlag = False
    startCaliRuOffsetFlag = False
    startCaliFuOffsetFlag = False

    convertPoint1 = ()
    convertPoint2 = ()
    moveDistance = -2.5

    # Cali offset
    caliPosition = (0, 0, 0)
    caliDesignRef1 = (0, 0)

    numOfRefPointCombo: ttk.Combobox
    numOfRefPointList = []

    nameEntry: VisionEntry
    refPoint1xEntry: VisionEntry
    refPoint1yEntry: VisionEntry

    refPoint2xEntry: VisionEntry
    refPoint2yEntry: VisionEntry

    refPoint3xEntry: VisionEntry
    refPoint3yEntry: VisionEntry

    offsetPointXEntry: VisionEntry
    offsetPointYEntry: VisionEntry

    btnRef1Select: VisionButton
    btnRef2Select: VisionButton
    btnRef3Select: VisionButton
    btnOffsetPointSelect: VisionButton

    offsetXEntry: VisionEntry
    offsetYEntry: VisionEntry
    offsetZEntry: VisionEntry
    filePathEntry: VisionEntry

    activeFromEntry: VisionEntry
    activeToEntry: VisionEntry

    threshEntry: VisionEntry

    btnCaliOffset: VisionButton
    btnGetOffset: VisionButton
    btnModelTest: VisionButton
    btnSelectDesignFile: VisionButton
    btnActiveAdvanceSetting: VisionButton
    btnVisionSetting: VisionButton
    btnModelTest:VisionButton
    roto_weighing_robot_model_setting_frame:VisionFrame
    conversionCoefficientEntry: VisionEntry

    ref1Pos = -1
    ref2Pos = -1
    ref3Pos = -1
    offsetPos = -1

    isSelected = False
    yDistance = 35
    xDistance = 150

    def __init__(self, root: ttk.Notebook, mainWindow):
        from MainWindow import MainWindow
        VisionFrame.__init__(self, root)
        self.root = root
        self.mainWindow: MainWindow = mainWindow
        self.registerNotification()
        self.modelManager = ModelManager()
        self.currentModelParameter = ModelParameter()

        self.getParameter()
        self.setupView()
        self.pack(fill='both', expand=1)
        self.setupViewFinish()

    def setupViewFinish(self):
        self.refreshButtonState()

    def refreshButtonState(self):
        self.btnGetOffset.config(state="disable")
        self.btnCaliOffset.config(state="disable")

    def registerNotification(self):
        self.mainWindow.notificationCenter.add_observer(with_block=self.notifyUpdate, for_name="UpdateListModel")
        self.mainWindow.notificationCenter.add_observer(with_block=self.changeLanguage, for_name="ChangeLanguage")

    def changeLanguage(self, sender, notification_name, info):
        self.modelNameLabel.config(text=self.mainWindow.languageManager.localized("modelNameLbl"))
        self.ref1Lbl.config(text=self.mainWindow.languageManager.localized("ref1Lbl"))
        self.ref2Lbl.config(text=self.mainWindow.languageManager.localized("ref2Lbl"))
        self.ref3Lbl.config(text=self.mainWindow.languageManager.localized("ref3Lbl"))
        self.offsetPointLbl.config(text=self.mainWindow.languageManager.localized("offsetPointLbl"))
        self.offsetParmLbl.config(text=self.mainWindow.languageManager.localized("offsetParmLbl"))
        self.conversionLbl.config(text=self.mainWindow.languageManager.localized("conversionLbl"))
        self.designPathLbl.config(text=self.mainWindow.languageManager.localized("designPathLbl"))
        self.activePointFromLbl.config(text=self.mainWindow.languageManager.localized("activeFromLbl"))
        self.activePointToLbl.config(text=self.mainWindow.languageManager.localized("activeToLbl"))
        self.threshLbl.config(text=self.mainWindow.languageManager.localized("threshLbl"))
        self.btnRef1Select.config(text=self.mainWindow.languageManager.localized("ref1SelectBtn"))
        self.btnRef2Select.config(text=self.mainWindow.languageManager.localized("ref2SelectBtn"))
        self.btnRef3Select.config(text=self.mainWindow.languageManager.localized("ref3SelectBtn"))
        self.btnOffsetPointSelect.config(text=self.mainWindow.languageManager.localized("offsetPointSelectBtn"))
        self.btnCaliOffset.config(text=self.mainWindow.languageManager.localized("calibrationOffsetBtn"))
        self.btnGetOffset.config(text=self.mainWindow.languageManager.localized("getOffsetBtn"))
        self.btnTakeCoefficient.config(text=self.mainWindow.languageManager.localized("btnTakeCoefficient"))
        self.btnSelectDesignFile.config(text=self.mainWindow.languageManager.localized("designFileSelect"))
        self.btnActiveAdvanceSetting.config(text=self.mainWindow.languageManager.localized("advanceActiveBtn"))
        self.btnVisionSetting.config(text=self.mainWindow.languageManager.localized("visionSettingBtn"))
        self.btnSave.config(text=self.mainWindow.languageManager.localized("saveBtn"))
        self.btnDelete.config(text=self.mainWindow.languageManager.localized("deleteBtn"))
        self.btnAddNewModel.config(text=self.mainWindow.languageManager.localized("addNewModelBtn"))
        self.btnModelTest.config(text=self.mainWindow.languageManager.localized("model test"))
        # self.roto_weighing_robot_model_setting_frame.config(text=self.mainWindow.languageManager.localized("roto WR"))

    def notifyUpdate(self, sender, notification_name, info):
        self.updateListModel()
        print("model setting update list model")

    def updateListModel(self):
        self.getParameter()
        self.modelComboBox.config(value=self.modelNameList)
        try:
            self.modelManager.currentModelPos = len(self.modelNameList) - 1
            self.modelComboBox.current(self.modelManager.currentModelPos)
            self.showCurrentModel()
            self.save()
            self.mainWindow.runningTab.refreshModel()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Update list model: {}".format(error))
            messagebox.showerror("Error", "{}".format(error))

    def updateView(self):
        if self.currentSettingFrame is not None:
            self.currentSettingFrame.place_forget()

        machineName = self.mainWindow.startingWindow.machineName
        if machineName.isRearMissingInspectionMachine():
            if self.rearCheckMissingFrame is None:
                self.rearCheckMissingFrame = RearCheckMissingFrame(self, "Rear missing parameter")

            self.currentSettingFrame = self.rearCheckMissingFrame
            self.rearCheckMissingFrame.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)
        elif machineName.isFUAssemblyMachine() or machineName.isLoadFrameMachine():
            if self.fu_assy_Frame is None:
                self.fu_assy_Frame = Fu_Assy_Setting_Frame(self, mainWindow=self.mainWindow, text="Assembly parameter")
            self.currentSettingFrame = self.fu_assy_Frame
            self.fu_assy_Frame.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)
        elif machineName.isLocationDetect():
            if self.locationDetectSettingFrame is None:
                self.locationDetectSettingFrame = LocationDetectSettingFrame(self, "Location Detect")

            self.currentSettingFrame = self.locationDetectSettingFrame
            self.locationDetectSettingFrame.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)
        elif machineName.is_demo_color_detect():
            if self.demo_color_detect_setting_frame is None:
                self.demo_color_detect_setting_frame = DemoColorDetectSettingFrame(self, "Demo Color Detect")
            self.currentSettingFrame = self.demo_color_detect_setting_frame
            self.demo_color_detect_setting_frame.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)
        elif machineName.is_demo_location_detect():

            if self.demo_location_detect_setting_frame is None:
                self.demo_location_detect_setting_frame = DemoLocationDetectSettingFrame(self, "Demo Location Detect")


            self.currentSettingFrame = self.demo_location_detect_setting_frame
            self.demo_location_detect_setting_frame.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)
        elif machineName.is_roto_weighing_robot()\
                    or machineName.is_demo_counting()\
                    or machineName.is_focus_checking()\
                    or machineName.is_demo_circle_measurement()\
                    or machineName.is_demo_line_measurement() :
            if self.roto_weighing_robot_model_setting_frame is None:
                self.roto_weighing_robot_model_setting_frame = RotoWeighingSettingModelFrame(self,mainWindow=self.mainWindow, text=self.mainWindow.languageManager.localized("roto WR"))
            self.currentSettingFrame = self.roto_weighing_robot_model_setting_frame
            self.roto_weighing_robot_model_setting_frame.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)
        elif machineName.is_syc_phone_check()\
                    or machineName.is_demo_counting()\
                    or machineName.is_focus_checking()\
                    or machineName.is_demo_circle_measurement()\
                    or machineName.is_demo_line_measurement() :
            if self.syc_model_setting_frame is None:
                # self.syc_inspection=SYC_Inspection(self)
                self.syc_model_setting_frame = SYC_Model_Setting(self,"Error sample")
            self.currentSettingFrame = self.syc_model_setting_frame
            self.syc_model_setting_frame.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)

        elif machineName.is_fpc_inspection():
            if self.fpc_inspection_frame is None:
                self.fpc_inspection_frame = FPC_Inspection_Model_Setting_Frame(self,
                                                                               text="FPC Inspection Model Setting")
            self.currentSettingFrame = self.fpc_inspection_frame
            self.fpc_inspection_frame.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)
        elif machineName.is_ddk_inspection():
            if self.ddk_inspection_frame is None:
                self.ddk_inspection_frame = DDK_Inspection_Model_Setting(self, text="DDK Inspection Model Setting")
            self.currentSettingFrame = self.ddk_inspection_frame
            self.ddk_inspection_frame.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)

        elif machineName.is_hik_barcode_demo():
            if self.hik_barcode_demo_setting is None:
                self.hik_barcode_demo_setting = HikBarcodeDemoSetting(self, text="HIK Barcode Demo Setting")
            self.currentSettingFrame = self.hik_barcode_demo_setting
            self.hik_barcode_demo_setting.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)
        elif machineName.is_e_map_checking():
            if self.e_map_model_setting is None:
                self.e_map_model_setting = E_Map_Model_Setting(self, self.mainWindow)
            self.currentSettingFrame = self.e_map_model_setting
            self.e_map_model_setting.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)
        elif machineName.is_housing_connector_packing():
            if self.thcp_model_setting is None:
                self.thcp_model_setting = THCP_Model_Setting(self, self.mainWindow)
            self.currentSettingFrame = self.thcp_model_setting
            self.thcp_model_setting.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)
        elif machineName.is_reading_weighing():
            if self.read_weighing_model_setting is None:
                self.read_weighing_model_setting = Read_Weighing_Model_Setting(self, self.mainWindow)
            self.currentSettingFrame = self.read_weighing_model_setting
            self.read_weighing_model_setting.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)
        elif machineName.is_counting_in_conveyor():
            if self.counting_in_conveyor_setting is None:
                self.counting_in_conveyor_setting = Counting_In_Conveyor_Setting(self, self.mainWindow)
            self.currentSettingFrame = self.counting_in_conveyor_setting
            self.counting_in_conveyor_setting.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)

        elif machineName.is_washing_machine_inspection():
            if self.wm_inspection_model_setting is None:
                self.wm_inspection_model_setting = WM_Inspection_Model_Setting(self, text="Washing machine inspection")
            self.currentSettingFrame = self.wm_inspection_model_setting
            self.wm_inspection_model_setting.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)
        else:
            self.currentSettingFrame = self.screwParameterFrame
            self.screwParameterFrame.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.75)

        self.showCurrentModel()

    def setupView(self):
        self.setupScrewParameterFrame()
        self.setupAddNewButton()
        self.setupDuplicateButton()
        self.setupSaveButton()
        self.setupDeleteButton()
        self.setupBtnTest()
        self.setupModelName()
        self.setupBtnTakePic()
        self.setupModelChosen()

    def setupModelChosen(self):
        modelLabel = VisionLabel(self, text="Model: ")
        modelLabel.place(relx=0.02, rely=0.02)

        self.modelComboBox = ttk.Combobox(self, value=self.modelNameList, state='readonly', cursor="hand2")
        self.modelComboBox.bind("<<ComboboxSelected>>", self.modelSelected)
        self.modelComboBox.place(relx=0.15, rely=0.02)
        try:
            self.modelComboBox.current(self.modelManager.currentModelPos)
            self.showCurrentModel()
            self.mainWindow.runningTab.refreshModel()
        except:
            pass

    def setupBtnTakePic(self):
        btnTakePic = TakePicButton(self, self.mainWindow.workingThread.capturePicture)
        btnTakePic.place(relx=0.68, rely=0.069, relwidth=0.2, relheight = 0.05)

    def setupBtnTest(self):
        self.btnModelTest = VisionButton(self, text=self.mainWindow.languageManager.localized("model test"), command=self.clickBtnModelTest)
        self.btnModelTest.place(relx=0.6, rely=0.015)

    def modelSelected(self, param):
        if self.isChanged():
            askSave = messagebox.askyesno(self.mainWindow.languageManager.localized("title_saveModel"),
                                          self.mainWindow.languageManager.localized("msg_saveModel").format(self.modelNameList[self.modelManager.currentModelPos]))
            if askSave:
                if self.modelList[self.modelManager.currentModelPos].name != self.nameEntry.get() and\
                        self.modelManager.modelNameExisted(self.nameEntry.get()):
                    askChange = messagebox.askyesno("Model Name", "The model name \"{}\" is existed, Do you want to change another name?\nyes = stay and change\nno = move without saving".format(self.nameEntry.get()))
                    if askChange:
                        self.modelComboBox.current(self.modelManager.currentModelPos)
                        self.mainWindow.runningTab.refreshModel()
                        return
                else:
                    self.save()
        self.modelManager.currentModelPos = self.modelComboBox.current()
        self.showCurrentModel()
        self.refreshButtonState()
        self.modelManager.save()
        self.mainWindow.runningTab.refreshModel()
        if self.mainWindow.startingWindow.machineName is not None and self.mainWindow.startingWindow.machineName.isFilterCoverScrewMachine():
            self.drawCurrentModelDesign()

    def setupModelName(self):
        # Name entry
        self.modelNameLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("modelNameLbl"))
        self.modelNameLabel.place(relx=0.02, rely=0.069)

        self.nameEntry = VisionEntry(self)
        self.nameEntry.place(relx=0.25, rely=0.069, width=180, height=20)

    def setupAddNewButton(self):
        self.btnAddNewModel = AddButton(self, command=self.addNewModel)
        self.btnAddNewModel.place(relx=0.02, rely=0.92, relwidth=0.225, relheight=0.05)

    def setupDuplicateButton(self):
        self.btnDuplicate = CopyButton(self, command=self.duplicateModel)
        self.btnDuplicate.place(relx=0.265, rely=0.92, relwidth=0.225, relheight=0.05)

    def setupSaveButton(self):
        self.btnSave = SaveButton(self, command=self.clickBtnSave)
        self.btnSave.place(relx=0.510, rely=0.92, relwidth=0.225, relheight=0.05)

    def setupDeleteButton(self):
        self.btnDelete = DeleteButton(self, command=self.clickBtnDelete)
        self.btnDelete.place(relx=0.755, rely=0.92, relwidth=0.225, relheight=0.05)

    def setupScrewParameterFrame(self):
        self.screwParameterFrame1 = ScrewParameterTab(self, self.mainWindow, None)
        distanceY = 0.07

        self.screwParameterFrame = VisionLabelFrame(self, text=self.mainWindow.languageManager.localized("parameter"))

        for numOfRefPoint in NumOfRefPoint:
            self.numOfRefPointList.append(numOfRefPoint.value)
        self.numOfRefPointCombo = ttk.Combobox(self.screwParameterFrame, state='readonly', value=self.numOfRefPointList, cursor="hand2")
        self.numOfRefPointCombo.place(relx=0.02, rely=0.05, relwidth=0.22)

        # reference points
        nameLabel = VisionLabel(self.screwParameterFrame, text="X")
        nameLabel.place(relx=0.3, rely=distanceY + 0.02)

        nameLabel = VisionLabel(self.screwParameterFrame, text="Y")
        nameLabel.place(relx=0.6, rely=distanceY + 0.02)

        # reference point 1
        self.ref1Lbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("ref1Lbl"))
        self.ref1Lbl.place(relx=0.02, rely=2*distanceY)

        self.refPoint1xEntry = VisionEntry(self.screwParameterFrame)
        self.refPoint1xEntry.place(relx=0.22, rely=2*distanceY, relwidth=0.2, relheight=0.045)

        self.refPoint1yEntry = VisionEntry(self.screwParameterFrame)
        self.refPoint1yEntry.place(relx=0.52, rely=2 * distanceY, relwidth=0.2, relheight=0.045)

        self.btnRef1Select = VisionButton(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("ref1SelectBtn"), command=self.clickBtnRef1Select)
        self.btnRef1Select.place(relx=0.83, rely=2 * distanceY, relwidth=0.15, relheight=0.05)


        #reference point 2
        self.ref2Lbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("ref2Lbl"))
        self.ref2Lbl.place(relx=0.02, rely=3 * distanceY)

        self.refPoint2xEntry = VisionEntry(self.screwParameterFrame)
        self.refPoint2xEntry.place(relx=0.22, rely=3 * distanceY, relwidth=0.2, relheight=0.045)

        self.refPoint2yEntry = VisionEntry(self.screwParameterFrame)
        self.refPoint2yEntry.place(relx=0.52, rely=3 * distanceY, relwidth=0.2, relheight=0.045)

        self.btnRef2Select = VisionButton(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("ref2SelectBtn"), command=self.clickBtnRef2Select)
        self.btnRef2Select.place(relx=0.83, rely=3 * distanceY, relwidth=0.15, relheight=0.05)

        #reference point 3
        self.ref3Lbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("ref3Lbl"))
        self.ref3Lbl.place(relx=0.02, rely=4 * distanceY)

        self.refPoint3xEntry = VisionEntry(self.screwParameterFrame)
        self.refPoint3xEntry.place(relx=0.22, rely=4 * distanceY, relwidth=0.2, relheight=0.045)

        self.refPoint3yEntry = VisionEntry(self.screwParameterFrame)
        self.refPoint3yEntry.place(relx=0.52, rely=4 * distanceY, relwidth=0.2, relheight=0.045)

        self.btnRef3Select = VisionButton(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("ref3SelectBtn"), command=self.clickBtnRef3Select)
        self.btnRef3Select.place(relx=0.83, rely=4 * distanceY, relwidth=0.15, relheight=0.05)

        # offset position
        self.offsetPointLbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("offsetPointLbl"))
        self.offsetPointLbl.place(relx=0.02, rely=5 * distanceY)

        self.offsetPointXEntry = VisionEntry(self.screwParameterFrame)
        self.offsetPointXEntry.place(relx=0.22, rely=5 * distanceY, relwidth=0.2, relheight=0.045)

        self.offsetPointYEntry = VisionEntry(self.screwParameterFrame)
        self.offsetPointYEntry.place(relx=0.52, rely=5 * distanceY, relwidth=0.2, relheight=0.045)

        self.btnOffsetPointSelect = VisionButton(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("offsetPointSelectBtn"), command=self.clickBtnOffsetPointSelect)
        self.btnOffsetPointSelect.place(relx=0.83, rely=5 * distanceY, relwidth=0.15, relheight=0.05)

        # Offset
        self.offsetParmLbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("offsetParmLbl"))
        self.offsetParmLbl.place(relx=0.02, rely=6 * distanceY)

        self.offsetXEntry = VisionEntry(self.screwParameterFrame)
        self.offsetXEntry.place(relx=0.22, rely=6 * distanceY, relwidth=0.18, relheight=0.045)

        self.offsetYEntry = VisionEntry(self.screwParameterFrame)
        self.offsetYEntry.place(relx=0.46, rely=6 * distanceY, relwidth=0.18, relheight=0.045)

        self.offsetZEntry = VisionEntry(self.screwParameterFrame)
        self.offsetZEntry.place(relx=0.70, rely=6 * distanceY, relwidth=0.18, relheight=0.045)

        self.btnCaliOffset = VisionButton(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("calibrationOffsetBtn"), command=self.clickBtnCaliOffset)
        self.btnCaliOffset.place(relx=0.3, rely=7 * distanceY, relwidth=0.3)

        self.btnGetOffset = VisionButton(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("getOffsetBtn"), command=self.clickBtnGetOffset)
        self.btnGetOffset.place(relx=0.65, rely=7 * distanceY, relwidth=0.25)

        # conversion coefficient

        self.conversionLbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("conversionLbl"))
        self.conversionLbl.place(relx=0.02, rely= 8 * distanceY)

        self.conversionCoefficientEntry = VisionEntry(self.screwParameterFrame)
        self.conversionCoefficientEntry.place(relx=0.35, rely=8 * distanceY, relwidth=0.25, relheight=0.045)

        self.btnTakeCoefficient = VisionButton(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("btnTakeCoefficient"), command=self.clickBtnTakeCoef)
        self.btnTakeCoefficient.place(relx=0.65, rely=7.9 * distanceY, relwidth=0.3)

        # Offset
        self.designPathLbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("designPathLbl"))
        self.designPathLbl.place(relx=0.02, rely=9 * distanceY)

        self.filePathEntry = VisionEntry(self.screwParameterFrame)
        self.filePathEntry.place(relx=0.3, rely=9 * distanceY, relwidth=0.55, relheight=0.045)

        self.btnSelectDesignFile = VisionButton(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("designFileSelect"), command=self.clickBtnSelectFile)
        self.btnSelectDesignFile.place(relx= 0.65, rely=9.9 * distanceY, relwidth=0.25)

        # Active positions
        self.activePointFromLbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("activeFromLbl"))
        self.activePointFromLbl.place(relx=0.02, rely=11 * distanceY)

        self.activeFromEntry = VisionEntry(self.screwParameterFrame)
        self.activeFromEntry.place(relx=0.36, rely=11 * distanceY, relwidth=0.1, relheight=0.045)

        self.activePointToLbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("activeToLbl"))
        self.activePointToLbl.place(relx=0.51, rely=11 * distanceY)

        self.activeToEntry = VisionEntry(self.screwParameterFrame)
        self.activeToEntry.place(relx=0.61, rely=11 * distanceY, relwidth=0.1, relheight=0.045)

        self.btnActiveAdvanceSetting = VisionButton(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("advanceActiveBtn"), command=self.clickBtnActiveAdvance)
        self.btnActiveAdvanceSetting.place(relx=0.74, rely= 10.9 * distanceY, relwidth = 0.25)

        # Thresh setting
        self.threshLbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("threshLbl"))
        self.threshLbl.place(relx=0.02, rely=12 * distanceY)

        self.threshEntry = VisionEntry(self.screwParameterFrame)
        self.threshEntry.place(relx=0.3, rely=12 * distanceY, relwidth=0.2, relheight=0.045)

        self.btnVisionSetting = VisionButton(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("visionSettingBtn"), command=self.clickBtnVisionSetting)
        self.btnVisionSetting.place(relx=0.6, rely=12 * distanceY, relwidth=0.3)

    def clickBtnVisionSetting(self):
        visionSettingWindow = VisionSettingWindow(self.mainWindow, self.modelList[self.modelManager.currentModelPos])
        visionSettingWindow.wait_window()
        if visionSettingWindow.saveFlag:
            self.modelList[self.modelManager.currentModelPos].screwRecognizeAlgorithm = visionSettingWindow.screwRecognizeAlgorithm
            self.modelList[self.modelManager.currentModelPos].ringRecognizeAlgorithm = visionSettingWindow.ringRecognizeAlgorithm
            self.modelList[self.modelManager.currentModelPos].centerHoleAlgorithm = visionSettingWindow.centerHoleAlgorithm


    def clickBtnRef1Select(self):
        if not self.pointExisted():
            return
        from View.ModelSetting.ReferencePositionSelectWindow import ReferencePositionSelectWindow
        referenceWindow1 = ReferencePositionSelectWindow(self.mainWindow)
        referenceWindow1.wait_window()
        if not referenceWindow1.isChosenFlag:
            return
        point = self.mainWindow.workingThread.adjustingScrewPos.originalPositions[referenceWindow1.posChosen]
        self.refPoint1xEntry.delete(0, END)
        self.refPoint1yEntry.delete(0, END)

        self.refPoint1xEntry.insert(0,"{}".format(point[0]))
        self.refPoint1yEntry.insert(0,"{}".format(point[1]))

        self.ref1Pos = referenceWindow1.posChosen

    def clickBtnRef2Select(self):
        if not self.pointExisted():
            return
        from View.ModelSetting.ReferencePositionSelectWindow import ReferencePositionSelectWindow
        referenceWindow2 = ReferencePositionSelectWindow(self.mainWindow)
        referenceWindow2.wait_window()
        if not referenceWindow2.isChosenFlag:
            return
        point = self.mainWindow.workingThread.adjustingScrewPos.originalPositions[referenceWindow2.posChosen]
        self.refPoint2xEntry.delete(0, END)
        self.refPoint2yEntry.delete(0, END)

        self.refPoint2xEntry.insert(0,"{}".format(point[0]))
        self.refPoint2yEntry.insert(0,"{}".format(point[1]))

        self.ref2Pos = referenceWindow2.posChosen

    def clickBtnRef3Select(self):
        if not self.pointExisted():
            return
        from View.ModelSetting.ReferencePositionSelectWindow import ReferencePositionSelectWindow
        referenceWindow3 = ReferencePositionSelectWindow(self.mainWindow)
        referenceWindow3.wait_window()
        if not referenceWindow3.isChosenFlag:
            return
        point = self.mainWindow.workingThread.adjustingScrewPos.originalPositions[referenceWindow3.posChosen]
        self.refPoint3xEntry.delete(0, END)
        self.refPoint3yEntry.delete(0, END)

        self.refPoint3xEntry.insert(0,"{}".format(point[0]))
        self.refPoint3yEntry.insert(0,"{}".format(point[1]))

        self.ref3Pos = referenceWindow3.posChosen

    def clickBtnOffsetPointSelect(self):
        if not self.pointExisted():
            return
        from View.ModelSetting.ReferencePositionSelectWindow import ReferencePositionSelectWindow
        offsetSelectWindow = ReferencePositionSelectWindow(self.mainWindow)
        offsetSelectWindow.wait_window()
        if not offsetSelectWindow.isChosenFlag:
            return
        point = self.mainWindow.workingThread.adjustingScrewPos.originalPositions[offsetSelectWindow.posChosen]
        self.offsetPointXEntry.delete(0, END)
        self.offsetPointYEntry.delete(0, END)

        self.offsetPointXEntry.insert(0,"{}".format(point[0]))
        self.offsetPointYEntry.insert(0,"{}".format(point[1]))

        self.offsetPos = offsetSelectWindow.posChosen

    def pointExisted(self):
        if len(self.mainWindow.workingThread.adjustingScrewPos.originalPositions) <= 0:
            messagebox.showerror(self.mainWindow.languageManager.localized("title_noPointExisted"),
                                 self.mainWindow.languageManager.localized("msg_title_noPointExisted"))
            return False
        else:
            return True

    def clickBtnActiveAdvance(self):
        activeAdvanceSetting = ActivePointAdvanceSettingView(self.mainWindow,
                                                             activeFrom=int(float(self.activeFromEntry.get())),
                                                             activeTo=int(float(self.activeToEntry.get())),
                                                             lastSetting=self.modelList[self.modelManager.currentModelPos].activePointsSetting)
        activeAdvanceSetting.wait_window()
        for state in activeAdvanceSetting.result:
            print(state)

        if activeAdvanceSetting.confirmYes:
            self.modelList[self.modelManager.currentModelPos].activePointsSetting = activeAdvanceSetting.result

    def clickBtnSelectFile(self):
        filePath = tkinter.filedialog.askopenfilename(title="Select design file",
                                                      filetypes=(('Csv file', '*.csv'), ('All files', '*.*')),
                                                      initialdir="/áéá")
        if filePath == "":
            return
        self.filePathEntry.delete(0, END)
        self.filePathEntry.insert(0, filePath)
        self.filePathEntry.xview(END)

        self.drawCurrentModelDesign()

    def drawCurrentModelDesign(self):
        self.modelList[self.modelManager.currentModelPos].designFilePath = self.filePathEntry.get()
        self.mainWindow.runningTab.modelManager.models = self.modelList
        self.mainWindow.workingThread.drawCurrentModelDesign()

    def clickBtnModelTest(self):
        machineName = self.mainWindow.startingWindow.machineName
        if machineName.is_hik_barcode_demo():
            self.testHikBarcodeDemo()
        elif machineName.is_e_map_checking():
            self.e_map_model_setting.testDraw()
        elif machineName.is_housing_connector_packing():
            self.thcp_model_setting.testDraw()
        elif machineName.is_reading_weighing():
            self.read_weighing_model_setting.testDraw()
        elif machineName.is_counting_in_conveyor():
            self.counting_in_conveyor_setting.testModel()
        elif machineName.is_syc_phone_check():
            self.mainWindow.workingThread.create_syc_phone_check()
            self.mainWindow.workingThread.syc_inspection.doProcess(image=self.mainWindow.originalImage,
                                                                   isRunningFlag=False)
        elif machineName.is_roto_weighing_robot():
            self.mainWindow.workingThread.create_roto_weighing()
            roto_weighing = self.mainWindow.workingThread.roto_weighing_robot
            roto_weighing.updateModel()
            plcInfo = CommunicationReceiveInfo()
            plcInfo.step = 1
            plcInfo.axisSystemName = self.mainWindow.as_manager.currentName
            roto_weighing.calculateDeviationCoordinates(plcInfo, image=self.mainWindow.originalImage)
        self.modelTestFlag = True

    def testHikBarcodeDemo(self):
        barcodeReaderStart = SocketClientManager(self.mainWindow, "HikBarcodeTrigger")
        barcodeReaderResponse = SocketClientManager(self.mainWindow, "HikBarcodeResponse")
        barcodeReaderStart.sockInfo.host = "192.168.1.6"
        barcodeReaderStart.sockInfo.port = 2001
        barcodeReaderStart.sockInfo.save()

        barcodeReaderResponse.sockInfo.host = "192.168.1.6"
        barcodeReaderResponse.sockInfo.port = 1500
        barcodeReaderResponse.sockInfo.save()

        PathFileControl.generatePath("./data")
        barocdeFile = CsvFile("./data/hik_barcode_data.csv")

        if not barcodeReaderStart.connect():
            messagebox.showerror("Trigger connection","Cannot connect to barcode reader to send trigger")
            barcodeReaderStart.disconnect()
            barcodeReaderResponse.disconnect()
            return
        if not barcodeReaderResponse.connect():
            messagebox.showerror("Response connection","Cannot connect to barcode reader to get response!")
            barcodeReaderStart.disconnect()
            barcodeReaderResponse.disconnect()
            return

        barcodeReaderStart.sendData("start")
        time = TimeControl.time()
        ret = False
        while TimeControl.time() - time < 3000:
            res = barcodeReaderResponse.readData()

            if res != "":
                try:
                    dataList = []
                    resList = res.split(";")
                    for data in resList:
                        dataList.append([TimeControl.ymd_HMSFormat(), data])
                    barocdeFile.appendData(data=dataList, isList=True)
                    self.mainWindow.runningTab.insertLog("barcode response: {}".format(res))
                    ret = True
                    break
                except Exception as error:
                    text = f"ERROR Read barcode. Detail: {error}"
                    self.mainWindow.runningTab.insertLog(text)
                    break
            TimeControl.sleep(3)
        if not ret:
            messagebox.showerror("Barcode Reader", "Timeout response error!")
        barcodeReaderStart.disconnect()
        barcodeReaderResponse.disconnect()


    def refreshModel(self):
        self.modelManager.refresh()
        self.modelComboBox.current(self.modelManager.currentModelPos)
        self.showCurrentModel()
        self.refreshButtonState()
        self.mainWindow.researchingTab.updateAlgorithmForChangeModel()

    def updateModelParameter(self, currentIndex):
        return

    def isChanged(self):
        if len(self.modelList) < 1:
            return False
        currentModel = self.modelList[self.modelManager.currentModelPos]

        ret = (currentModel.name != self.nameEntry.get())\
              or (currentModel.numOfRefPoint != self.numOfRefPointCombo.get())\
              or (currentModel.refPoint1[0] != (float(self.refPoint1xEntry.get())))\
              or (currentModel.refPoint1[1] != (float(self.refPoint1yEntry.get())))\
              or (currentModel.refPoint2[0] != (float(self.refPoint2xEntry.get())))\
              or (currentModel.refPoint2[1] != (float(self.refPoint2yEntry.get())))\
              or (currentModel.refPoint3[0] != (float(self.refPoint3xEntry.get())))\
              or (currentModel.refPoint3[1] != (float(self.refPoint3yEntry.get()))) \
              or (currentModel.offsetPoint[0] != (float(self.offsetPointXEntry.get()))) \
              or (currentModel.offsetPoint[1] != (float(self.offsetPointYEntry.get()))) \
              or (currentModel.offset[0] != (float(self.offsetXEntry.get()))) \
              or (currentModel.offset[1] != (float(self.offsetYEntry.get()))) \
              or (currentModel.offset[2] != (float(self.offsetZEntry.get()))) \
              or (currentModel.designFilePath != self.filePathEntry.get()) \
              or (currentModel.activeFrom != int(float(self.activeFromEntry.get()))) \
              or (currentModel.activeTo != int(float(self.activeToEntry.get()))) \
              or (currentModel.threshValue != int(float(self.threshEntry.get()))) \
              or (currentModel.conversionCoef != (float(self.conversionCoefficientEntry.get())))

        machineName = self.mainWindow.startingWindow.machineName
        if machineName is not None:
            if machineName.isRearMissingInspectionMachine():
                ret = ret or self.rearCheckMissingFrame.isChanged(currentModel)
            elif machineName.isLocationDetect():
                ret = ret or self.locationDetectSettingFrame.isChanged(currentModel)
            elif machineName.is_demo_color_detect():
                ret = ret or self.demo_color_detect_setting_frame.isChanged(currentModel)
            elif machineName.is_demo_location_detect():
                ret = ret or self.demo_location_detect_setting_frame.isChanged(currentModel)
            elif machineName.is_roto_weighing_robot()\
                    or machineName.is_demo_counting()\
                    or machineName.is_focus_checking()\
                    or machineName.is_demo_circle_measurement()\
                    or machineName.is_demo_line_measurement():
                ret = ret or self.roto_weighing_robot_model_setting_frame.isChanged(currentModel)
            elif machineName.is_fpc_inspection():
                ret = ret or self.fpc_inspection_frame.isChanged(currentModel)
            elif machineName.is_hik_barcode_demo():
                ret = ret or self.hik_barcode_demo_setting.isChanged(currentModel)
            elif machineName.isFUAssemblyMachine() or machineName.isLoadFrameMachine():
                ret = ret or self.fu_assy_Frame.isChanged(currentModel)
            elif machineName.is_e_map_checking():
                ret = ret or self.e_map_model_setting.isChanged(currentModel)
            elif machineName.is_housing_connector_packing():
                ret = ret or self.thcp_model_setting.isChanged(currentModel)
            elif machineName.is_reading_weighing():
                ret = ret or self.read_weighing_model_setting.isChanged(currentModel)
            elif machineName.is_counting_in_conveyor():
                ret = ret or self.counting_in_conveyor_setting.isChanged(currentModel)
            elif machineName.is_ddk_inspection():
                ret = ret or self.ddk_inspection_frame.isChanged(parameter=currentModel)
            elif machineName.is_washing_machine_inspection():
                ret = ret or self.wm_inspection_model_setting.isChanged(parameter=currentModel)
            elif machineName.is_syc_phone_check():
                ret = ret or self.syc_model_setting_frame.isChanged(parameter=currentModel)
        return ret

    def clickBtnDelete(self):
        askDelete = messagebox.askyesno("Delete Model", "Are sure want to delete this model?")
        if askDelete:
            try:
                self.modelList.remove(self.modelList[self.modelManager.currentModelPos])
                self.modelManager.models = self.modelList
                self.modelManager.save()
                self.updateListModel()
                messagebox.showinfo("Delete Model", "Delete Model successfully!")
            except Exception as error:
                self.mainWindow.runningTab.insertLog("ERROR Delete Model: {}".format(error))
                messagebox.showerror("Delete Model", "{}".format(error))

    def clickBtnTakeCoef(self):
        self.startTakeCoefFlag = True

    def clickBtnGetOffset(self):
        self.getOffsetFlag = True

    def clickBtnCaliOffset(self):
        # designRef1X, designRef1Y = self.modelList[self.modelManager.currentModelPos].refPoint1
        #
        # caliDesignRef1X = int(self.plcLengthScale * designRef1X)
        # caliDesignRef1Y = int(self.plcLengthScale * designRef1Y)
        designOffsetPointX, designOffsetPointY = self.modelList[self.modelManager.currentModelPos].offsetPoint

        # caliDesignRef1X = int(self.plcLengthScale * designOffsetPointX)
        # for mirror axis
        caliDesignRef1X = int(self.mainWindow.workingThread.adjustingScrewPos.plcLengthScale * (self.mainWindow.workingThread.adjustingScrewPos.mirrorXValue - designOffsetPointX))
        caliDesignRef1Y = int(self.mainWindow.workingThread.adjustingScrewPos.plcLengthScale * designOffsetPointY)

        self.caliDesignRef1 = (caliDesignRef1X, caliDesignRef1Y)
        self.startCaliOffsetFlag = True

    def setOffsetValue(self, plcValue):
        try:
            plcRevInfo = CommunicationReceiveAnalyze.getRuConnectorInfo(plcValue)
            x = plcRevInfo.x
            y = plcRevInfo.y
            z = plcRevInfo.z
            caliPosX, caliPosY = self.caliDesignRef1
            offsetX = x - caliPosX
            offsetY = y - caliPosY


            self.offsetXEntry.delete(0, END)
            self.offsetYEntry.delete(0, END)
            self.offsetZEntry.delete(0, END)

            self.offsetXEntry.insert(0, offsetX)
            self.offsetYEntry.insert(0, offsetY)
            self.offsetZEntry.insert(0, z)
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Set offset: {}".format(error))
            messagebox.showerror("Set offset", "{}".format(error))

    def caliOffset(self, plcValue):
        # XXXXX,YYYYY,ZZZZZ,OFFSETC
        move = False
        caliPos = (0, 0)
        try:
            plcRevInfo = CommunicationReceiveAnalyze.getRuConnectorInfo(plcValue)
            currentX = plcRevInfo.x
            currentY = plcRevInfo.y
            currentZ = plcRevInfo.z
            currentModel = self.modelList[self.modelManager.currentModelPos]
            caliPos = (currentX, currentY, currentZ)
            ret, image = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
            image = ImageProcess.flipHorizontal(image.copy()) # because the origin of axis coordinates is different from machine axis coordinates
            centerImageY = int(image.shape[0]/2)
            centerImageX = int(image.shape[1]/2)
            if ret:
                ret, circle, _ = self.mainWindow.workingThread.adjustingScrewPos.getRefPosition(image)
                (currentCoordinateX, currentCoordinateY) = circle[0]
                pixelDeltaX = currentCoordinateX - centerImageX
                pixelDeltaY = currentCoordinateY - centerImageY

                conversionCoef = float(self.conversionCoefficientEntry.get())

                if pixelDeltaX > 10 or pixelDeltaY > 10 or pixelDeltaX < -10 or pixelDeltaY < -10:
                    deltaX = int(self.mainWindow.workingThread.adjustingScrewPos.plcLengthScale * (pixelDeltaX * conversionCoef))
                    deltaY = int(self.mainWindow.workingThread.adjustingScrewPos.plcLengthScale * (pixelDeltaY * conversionCoef))

                    caliPosX = currentX + deltaX
                    caliPosY = currentY + deltaY

                    self.caliDesignRef1 = (self.caliDesignRef1[0] + deltaX, self.caliDesignRef1[1] + deltaY)
                    caliPos = (caliPosX, caliPosY, currentZ)
                    self.caliPosition = caliPos
                    move = True
                else:
                    self.btnGetOffset.config(state="normal")

                if not ret:
                    messagebox.showerror("Calibration Offset", "Cannot take find reference position!")
                    move = False
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Calibration offset: {}".format(error))
            messagebox.showerror("Calibrate Offset", "{}".format(error))
        return move, caliPos


    def takeConvertPoint1(self, plcRev):
        # XXXXX,YYYYY,ZZZZZ,CONVE1
        try:
            ret, image = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
            if ret:
                ret, circle, _ = self.mainWindow.workingThread.adjustingScrewPos.getRefPosition(image)
                self.convertPoint1 = circle[0]
                if not ret:
                    messagebox.showerror("Conversion Coefficient", "Cannot detect the reference position!")
            plcRevInfo = CommunicationReceiveAnalyze.getRuConnectorInfo(plcRev)
            plcConvertPoint1 = (plcRevInfo.x, plcRevInfo.y, plcRevInfo.z)

            self.modelList[self.modelManager.currentModelPos].plcRef1Pos = plcConvertPoint1

            plcConvertPoint2 = (plcConvertPoint1[0] + int(self.mainWindow.workingThread.adjustingScrewPos.plcLengthScale * self.moveDistance), plcConvertPoint1[1], plcConvertPoint1[2])
            return plcConvertPoint2
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Conversion Coefficient: {}".format(error))
            messagebox.showerror("Conversion Coefficient", "{}".format(error))
            return 0, 0

    def takeConvertPoint2(self):
        try:
            ret, image = self.mainWindow.workingThread.cameraManager.currentCamera.takePicture()
            if ret:
                ret, circle, _  = self.mainWindow.workingThread.adjustingScrewPos.getRefPosition(image)
                self.convertPoint2 = circle[0]
                if not ret:
                    messagebox.showerror("Conversion Coefficient", "Cannot detect the reference position!")
        except:
            return False
        return  self.calculateConversionCoef() and ret

    def calculateConversionCoef(self):
        try:
            x1, y1 = self.convertPoint1
            x2, y2 = self.convertPoint2
            distance = math.sqrt((int(x2) - int(x1)) ** 2 + (int(y2) - int(y1)) ** 2)
            coefficient = math.fabs(self.moveDistance)/ distance

            self.conversionCoefficientEntry.delete(0, END)
            self.conversionCoefficientEntry.insert(0, coefficient)
            self.btnCaliOffset.config(state="normal")
            # self.save()
            return True
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Calculate conversion coefficient: {}".format(error))
            messagebox.showerror("Calculate conversion coefficient", "{}".format(error))
            return False

    def clickBtnSave(self):
        if self.modelList[self.modelManager.currentModelPos].name != self.nameEntry.get() and \
                self.modelManager.modelNameExisted(self.nameEntry.get()):
            askChange = messagebox.askyesno("Model Name",
                                            "The model name \"{}\" is existed, Do you want to change another name?\nyes = stay and change\nno = move without saving".format(
                                                self.nameEntry.get()))
            if askChange:
                self.modelComboBox.current(self.modelManager.currentModelPos)
                return
        else:
            if self.save():
                self.modelComboBox.current(self.modelManager.currentModelPos)
                self.mainWindow.runningTab.refreshModel()

    def save(self, notification = True):
        modelParameter: ModelParameter = self.modelList[self.modelManager.currentModelPos]
        self.currentModelParameter = self.modelList[self.modelManager.currentModelPos]
        machineName = self.mainWindow.startingWindow.machineName
        try:

            modelParameter.name = self.nameEntry.get()
            modelParameter.refPoint1 = ((float(self.refPoint1xEntry.get())), (float(self.refPoint1yEntry.get())))
            modelParameter.refPoint2 = ((float(self.refPoint2xEntry.get())), (float(self.refPoint2yEntry.get())))
            modelParameter.refPoint3 = ((float(self.refPoint3xEntry.get())), (float(self.refPoint3yEntry.get())))
            modelParameter.offsetPoint = ((float(self.offsetPointXEntry.get())), (float(self.offsetPointYEntry.get())))
            modelParameter.offset = (int(float(self.offsetXEntry.get())), int(float(self.offsetYEntry.get())), int(float(self.offsetZEntry.get())))
            modelParameter.conversionCoef = float(self.conversionCoefficientEntry.get())
            modelParameter.designFilePath = self.filePathEntry.get()
            modelParameter.activeFrom = int(float(self.activeFromEntry.get()))
            modelParameter.activeTo = int(float(self.activeToEntry.get()))
            modelParameter.threshValue = int(float(self.threshEntry.get()))

            if modelParameter.activeTo < modelParameter.activeFrom:
                messagebox.showerror("Save Model", "Activated end point is grater than start point")
                return False

            modelParameter.numOfRefPoint = self.numOfRefPointCombo.get()
            if modelParameter.numOfRefPoint == NumOfRefPoint._2RefPoint.value:
                try:
                    coeff = 10000000000
                    ref1 = (int(coeff*modelParameter.refPoint1[0]), int(coeff*modelParameter.refPoint1[1]))
                    ref2 = (int(coeff*modelParameter.refPoint2[0]), int(coeff*modelParameter.refPoint2[1]))

                    ret, ref3 = ImageProcess.equilateralTriangleFrom2Points(ref1, ref2)
                    if ret:
                        modelParameter.refPoint3 = (ref3[0] / coeff, ref3[1] / coeff)

                        self.refPoint3xEntry.delete(0, END)
                        self.refPoint3yEntry.delete(0, END)

                        self.refPoint3xEntry.insert(0, modelParameter.refPoint3[0])
                        self.refPoint3yEntry.insert(0, modelParameter.refPoint3[1])
                    else:
                        messagebox.showerror("Number Of Reference Points",
                                             "Cannot Calculate the Reference point 3\nPlease check the Ref point 1 and Ref point 2")

                except Exception as error:
                    self.mainWindow.runningTab.insertLog("ERROR Number Of Reference Points: {}".format(error))
                    messagebox.showerror("Number Of Reference Points", "Cannot Calculate the Reference point 3\nPlease check the Ref point 1 and Ref point 2" )

            if machineName.isRearMissingInspectionMachine():
                self.rearCheckMissingFrame.save(model=modelParameter)
            elif machineName.isLocationDetect():
                self.locationDetectSettingFrame.save(model=modelParameter)
            elif machineName.is_demo_color_detect():
                self.demo_color_detect_setting_frame.save(model=modelParameter)
            elif machineName.is_demo_location_detect():
                self.demo_location_detect_setting_frame.save(model=modelParameter)
            elif machineName.is_roto_weighing_robot()\
                    or machineName.is_demo_counting()\
                    or machineName.is_focus_checking()\
                    or machineName.is_demo_circle_measurement()\
                    or machineName.is_demo_line_measurement():
                self.roto_weighing_robot_model_setting_frame.save(model=modelParameter)
            elif machineName.is_fpc_inspection():
                self.fpc_inspection_frame.save(model=modelParameter)
            elif machineName.is_ddk_inspection():
                self.ddk_inspection_frame.save(parameter=modelParameter)
            elif machineName.is_syc_phone_check():
                self.syc_model_setting_frame.save(parameter=modelParameter)
            elif machineName.is_hik_barcode_demo():
                self.hik_barcode_demo_setting.save(model=modelParameter)
            elif machineName.is_e_map_checking():
                self.e_map_model_setting.save(parameter=modelParameter)
            elif machineName.is_housing_connector_packing():
                self.thcp_model_setting.save(parameter=modelParameter)
            elif machineName.is_reading_weighing():
                self.read_weighing_model_setting.save(parameter=modelParameter)
            elif machineName.isFUAssemblyMachine() or machineName.isLoadFrameMachine():
                self.fu_assy_Frame.save(parameter=modelParameter)
            elif machineName.is_counting_in_conveyor():
                self.counting_in_conveyor_setting.save(parameter=modelParameter)
            elif machineName.is_washing_machine_inspection():
                self.wm_inspection_model_setting.save(parameter=modelParameter)

            self.modelList[self.modelManager.currentModelPos] = modelParameter
            self.modelNameList[self.modelManager.currentModelPos] = modelParameter.name
            self.modelComboBox.config(value=self.modelNameList)

        except:
            messagebox.showerror("Save model", "Cannot not save Model")
            return False
        self.modelManager.models = self.modelList
        self.modelManager.save()
        if machineName.isFilterCoverScrewMachine() or machineName.isRUConnectorScrewMachine():
            self.saveReferencePosition()

        if notification:
            messagebox.showinfo("Save Model", "Save Model successfully!")

        if machineName.isRearMissingInspectionMachine():
            self.mainWindow.workingThread.rearCheckMissing.updateModel()
        elif machineName.isRUConnectorScrewMachine():
            self.mainWindow.workingThread.ru_connectorCheckMissing.updateModel()
        elif machineName.isFUAssemblyMachine() or machineName.isLoadFrameMachine():
            self.mainWindow.workingThread.fu_assy_adjusting.updateModel()
            if not self.mainWindow.workingThread.fu_assy_adjusting.startWorking():
                messagebox.showwarning("Fu Assembly", "Devices are still not ready for use!\nCheck setting and connection")

        return True

    def saveReferencePosition(self):
        refsPos = []
        listRefsCoordinate = []

        if self.ref1Pos != -1:
            refsPos.append(self.ref1Pos)
        if self.ref2Pos != -1:
            refsPos.append(self.ref2Pos)
        if self.ref3Pos != -1:
            refsPos.append(self.ref3Pos)

        try:
            originalPositions = self.mainWindow.workingThread.adjustingScrewPos.originalPositions.copy()
            for index in refsPos:
                listRefsCoordinate.append(originalPositions[index])

            refsPos.sort()
            for index in reversed(refsPos):
                originalPositions.remove(originalPositions[index])

            originalPositions += listRefsCoordinate

            designFile = CsvFile(self.modelList[self.modelManager.currentModelPos].designFilePath)
            originalPositions.insert(0, ["X", "Y"])
            designFile.dataList = originalPositions
            designFile.saveFile()
            self.drawCurrentModelDesign()
            self.ref1Pos = -1
            self.ref2Pos = -1
            self.ref3Pos = -1
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Reference Position: {}".format(error))
            messagebox.showerror("Save Reference Position", "{}".format(error))

    def getParameter(self):
        self.modelNameList.clear()
        self.modelList.clear()
        self.modelManager.getParameter()
        self.modelList = self.modelManager.models
        for model in self.modelList:
            self.modelNameList.append(model.name)

    def showCurrentModel(self):
        try:
            currentModel = self.modelList[self.modelManager.currentModelPos]
            self.currentModelParameter = self.modelList[self.modelManager.currentModelPos]
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Show current model: {}".format(error))

            messagebox.showerror("Model Error", "{}".format(error))
            return
        self.nameEntry.delete(0, END)
        self.refPoint1xEntry.delete(0, END)
        self.refPoint1yEntry.delete(0, END)
        self.refPoint2xEntry.delete(0, END)
        self.refPoint2yEntry.delete(0, END)
        self.refPoint3xEntry.delete(0, END)
        self.refPoint3yEntry.delete(0, END)
        self.offsetPointXEntry.delete(0, END)
        self.offsetPointYEntry.delete(0, END)
        self.offsetXEntry.delete(0, END)
        self.offsetYEntry.delete(0, END)
        self.offsetZEntry.delete(0, END)
        self.conversionCoefficientEntry.delete(0, END)
        self.filePathEntry.delete(0, END)
        self.activeFromEntry.delete(0, END)
        self.activeToEntry.delete(0, END)
        self.threshEntry.delete(0, END)


        self.nameEntry.insert(0, currentModel.name)
        self.numOfRefPointCombo.current(self.numOfRefPointList.index(currentModel.numOfRefPoint))
        self.refPoint1xEntry.insert(0,"{}".format(currentModel.refPoint1[0]))
        self.refPoint1yEntry.insert(0,"{}".format(currentModel.refPoint1[1]))
        self.refPoint2xEntry.insert(0,"{}".format(currentModel.refPoint2[0]))
        self.refPoint2yEntry.insert(0,"{}".format(currentModel.refPoint2[1]))
        self.refPoint3xEntry.insert(0,"{}".format(currentModel.refPoint3[0]))
        self.refPoint3yEntry.insert(0,"{}".format(currentModel.refPoint3[1]))
        self.offsetPointXEntry.insert(0,"{}".format(currentModel.offsetPoint[0]))
        self.offsetPointYEntry.insert(0,"{}".format(currentModel.offsetPoint[1]))
        self.offsetXEntry.insert(0,"{}".format(currentModel.offset[0]))
        self.offsetYEntry.insert(0,"{}".format(currentModel.offset[1]))
        self.offsetZEntry.insert(0,"{}".format(currentModel.offset[2]))
        self.conversionCoefficientEntry.insert(0,"{}".format(currentModel.conversionCoef))
        self.activeFromEntry.insert(0, "{}".format(currentModel.activeFrom))
        self.activeToEntry.insert(0, "{}".format(currentModel.activeTo))
        self.threshEntry.insert(0, "{}".format(currentModel.threshValue))
        self.filePathEntry.insert(0, "{}".format(currentModel.designFilePath))
        self.filePathEntry.xview(len(currentModel.designFilePath) - 1)

        machineName = self.mainWindow.startingWindow.machineName
        if machineName is None:
            return

        if machineName.isRearMissingInspectionMachine():
            self.rearCheckMissingFrame.updateValue(currentModel)
        elif machineName.isLocationDetect():
            self.locationDetectSettingFrame.updateValue(currentModel)
        elif machineName.is_demo_color_detect():
            self.demo_color_detect_setting_frame.updateValue(currentModel)
        elif machineName.is_demo_location_detect():
            self.demo_location_detect_setting_frame.updateValue(currentModel)
        elif machineName.is_roto_weighing_robot():
            self.roto_weighing_robot_model_setting_frame.updateValue(currentModel)
        elif machineName.isFUAssemblyMachine():
            self.fu_assy_Frame.updateParameter(currentModel)
        elif machineName.is_fpc_inspection():
            self.fpc_inspection_frame.updateValue(currentModel)
        elif machineName.is_hik_barcode_demo():
            self.hik_barcode_demo_setting.updateValue(currentModel)
        elif machineName.is_e_map_checking():
            self.e_map_model_setting.updateValue(currentModel)
        elif machineName.is_housing_connector_packing():
            self.thcp_model_setting.updateValue(currentModel)
        elif machineName.is_reading_weighing():
            self.read_weighing_model_setting.updateValue(currentModel)
        elif machineName.is_counting_in_conveyor():
            self.counting_in_conveyor_setting.updateValue(currentModel)
        elif machineName.is_ddk_inspection():
            self.ddk_inspection_frame.updateValue(currentModel)
        elif machineName.is_washing_machine_inspection():
            self.wm_inspection_model_setting.updateValue(currentModel)
        elif machineName.is_syc_phone_check():
            self.syc_model_setting_frame.updateValue(currentModel)

    def addNewModel(self):
        newModelView = NewModelView(self.mainWindow, modelManager=self.modelManager)

    def duplicateModel(self):
        self.currentModelParameter = self.modelList[self.modelManager.currentModelPos]
        newModel: ModelParameter = copy.deepcopy(self.currentModelParameter)
        try:
            newModel.name = self.currentModelParameter.name + "_Copy"
            index = 1
            while self.modelManager.modelNameExisted(newModel.name):
                newModel.name = self.currentModelParameter.name + "_Copy_{}".format(index)
                index += 1

            self.modelManager.addNew(newModel)
            self.updateListModel()
        except Exception as error:
            messagebox.showwarning("Copy new model", "detail : {}".format(error))
