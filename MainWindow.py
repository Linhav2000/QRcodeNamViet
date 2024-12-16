from tkinter import messagebox
import cv2 as cv
import threading
from tkinter import filedialog
import numpy as np
from View.Running.RunningTab import RunningTab
from View.Researching.ResearchingTab import ResearchingTab
from View.ModelSetting.ModelSettingTab import ModelSettingTab
from View.AxisSystemSetting.AS_SettingTab import AS_SettingTab
from View.ModelSetting.ConvertFromCADWindow import ConvertFromCADWindow
from CommonAssit.FileManager import *

# from View.CameraSettingWindow import CameraSettingWindow
from notificationcenter import *
import CommonAssit.TimeControl as TimeControl
from ImageProcess.Algorithm.Algorithm import AlgorithmManager
from Modules.AxisSystem.AS_Manager import AS_Manager
from Modules.CommonSetting.CommonSetting import CommonSettingManager
import CommonAssit.CommonAssit as CommonAssit
from  CommonAssit.LanguageManager import LanguageManager
from View.ImageProcess.ImageRightClickOption import RightClickImageOption
from View.Setting.ImageViewSettingWindow import ImageViewSettingWindow
from View.Running.Ru_ConnectorImageFrame import Ru_ConnectorImageFrame
from View.MissingMachine.MissingMachineResultWindow import MissingMachineResultWindow
from View.Common.LogoView import LogoView
from Modules.MachineSetting.MachineList import MachineList
from Connection.ConnectionManager import ConnectionType
from View.Calibration.ChessboardCalibrationFrame import ChessboardCalibrationFrame
from View.Password.PW_Input_Window import PW_Input_Window
from ImageProcess import ImageProcess
import keyboard
from View.Common.VisionUI import *
from View.Common.ScrollFrame import ScrollView
import math
import pyautogui
from CommonAssit import PathFileControl
from multiprocessing import Process, Queue, Lock

class TabId(enum.Enum):
    runningTab = 0
    ResearchingTab = 1
    ModelSettingTab = 2
    AS_SettingTab = 3

class MenuCallBack:
    def __init__(self, value, command=None):
        self.value = value
        self.command = command

    def __call__(self, *args, **kwargs):
        if self.command is not None:
            self.command(self.value)

class MainWindow:
    imageFrame: VisionFrame
    imageResultFrame: VisionFrame
    image_OK_label: VisionLabel
    image_NG_label: VisionLabel
    imageTitle: VisionLabel
    tabBarFrame: VisionFrame
    bottomRightFrame: VisionFrame
    bottomLeftFrame: VisionFrame
    bottomMiddleFrame: VisionFrame


    rootMenu: VisionMenu
    cameraConfigMenu: VisionMenu
    selectCameraMenu: VisionMenu
    load_camera_feature_menu: VisionMenu
    record_camera_menu: VisionMenu

    imageMenu: VisionMenu
    cutImageMenu: VisionMenu
    newImageMenu: VisionMenu
    drawMenu: VisionMenu
    imageSaveMenu: VisionMenu
    imageResultVisible: VisionMenu
    screenRecordMenu: VisionMenu
    plcConnectionMenu: VisionMenu
    plcEthernetServerMenu: VisionMenu
    selectCommunicationMenu: VisionMenu
    plcEthernetClientMenu: VisionMenu
    plcSerialMenu: VisionMenu
    lightMenu: VisionMenu
    light_hard_test_menu: VisionMenu
    serverMenu: VisionMenu
    dataConfigMenu: VisionMenu
    languageMenu: VisionMenu
    zoomMenu: VisionMenu
    menusFrame: VisionFrame

    #bottom
    bottomLeftLabel: VisionLabel
    logoACE: VisionLabel
    bottomMiddleLabel: VisionLabel

    originalImage = None
    currentImage = None
    zoomImage = None
    zoomLabel = "Zoom"
    widthCoef = 1
    heightCoef = 1

    imageView: Canvas
    ru_connectorImageFrame: Ru_ConnectorImageFrame
    checkMissingWindow: MissingMachineResultWindow
    previous_image_btn: PreviousButton
    next_image_btn: NextButton
    # tab bar
    tabBar: ttk.Notebook
    runningTab: RunningTab
    researchingTab: ResearchingTab
    modelSettingTab: ModelSettingTab
    as_setting_tab: AS_SettingTab

    imageShow: ImageTk.PhotoImage
    drawFlag = False


    basePoint = [0, 0, 0, 0] # (x, y, width, height)

    isRecording = False
    isPaused = False

    zoomScale = 100
    multipleScale = 10

    default_pass = "Vision2021"
    check_pw_time = 0

    choose_area = (0, 0, 0, 0)
    currentImageTitle = ""

    def __init__(self, startingWindow = None):
        from WorkingThread import WorkingThread
        from Vision import StartingWindow
        self.startingWindow: StartingWindow = startingWindow
        self.algorithmManager = AlgorithmManager(self)
        self.as_manager = AS_Manager(self)
        self.commonSettingManager = CommonSettingManager(self)
        self.workingThread = WorkingThread(self)
        self.mainFrame = VisionTopLevel()
        self.notificationCenter: NotificationCenter = NotificationCenter()
        self.languageManager = LanguageManager(self)
        self.notifyRegister()
        self.setupWindow()
        # self.createCheckMissingWindow()
        # self.startKeyboardListening()

    def startKeyboardListening(self):
        keyboardThread = threading.Thread(target=self.keyboardListeningThread, args=())
        keyboardThread.start()

    def keyboardListeningThread(self):
        keyboard.on_release_key("Return", self.pressReturn)  # if key 'q' is pressed
        keyboard.on_release_key("Escape", self.pressEscape)
        # while True:
        #     try:  # used try so that if user pressed other than the given key error will not be shown
        #         keyboard.on_release_key("q", self.pressQkey())  # if key 'q' is pressed
        #     except:
        #         break  # if user pressed a key other than the given key the loop will break
    def pressEscape(self, event):
        # print("S")
        self.notificationCenter.post_notification(sender=None, with_name="Press_Escape")

    def pressReturn(self, event):
        # print("Enter")

        self.notificationCenter.post_notification(sender=None, with_name="Press_Enter")

    def notifyRegister(self):
        self.notificationCenter.add_observer(with_block=self.changeLanguage, for_name="ChangeLanguage")

    def changeLanguage(self, sender, notification_name, info):
        #root menu
        self.menuChangeLanguage(self.rootMenu, "camera")
        self.menuChangeLanguage(self.rootMenu, "LanguagesMenu")
        self.menuChangeLanguage(self.rootMenu, "image")
        self.menuChangeLanguage(self.rootMenu, "CommunicationMenu")
        self.menuChangeLanguage(self.rootMenu, "dataConfig")
        self.menuChangeLanguage(self.rootMenu, "light")
        self.menuChangeLanguage(self.rootMenu, "server")

        # Camera menu
        self.menuChangeLanguage(self.cameraConfigMenu, "setting")
        self.menuChangeLanguage(self.cameraConfigMenu, "connect")
        self.menuChangeLanguage(self.cameraConfigMenu, "disconnect")
        self.menuChangeLanguage(self.cameraConfigMenu, "cameraSelect")
        self.menuChangeLanguage(self.cameraConfigMenu, "Calibration")
        self.menuChangeLanguage(self.cameraConfigMenu, "capturePicture")
        self.menuChangeLanguage(self.cameraConfigMenu, "captureVideo")
        self.menuChangeLanguage(self.cameraConfigMenu, "stopCaptureVideo")
        self.menuChangeLanguage(self.cameraConfigMenu, "loadFeature")

        self.menuChangeLanguage(self.load_camera_feature_menu, "available")
        self.menuChangeLanguage(self.load_camera_feature_menu, "new")

        # Image menu
        self.menuChangeLanguage(self.imageMenu,"new")
        self.menuChangeLanguage(self.imageMenu, "open")
        self.menuChangeLanguage(self.imageMenu, "currentModelDesign")
        self.menuChangeLanguage(self.imageMenu, "draw")
        self.menuChangeLanguage(self.imageMenu, "save")

        self.menuChangeLanguage(self.newImageMenu, "blackImage")
        self.menuChangeLanguage(self.newImageMenu, "whiteImage")
        self.menuChangeLanguage(self.drawMenu, "on")
        self.menuChangeLanguage(self.drawMenu, "off")
        self.menuChangeLanguage(self.imageSaveMenu, "originalImage")
        self.menuChangeLanguage(self.imageSaveMenu, "processingImage")



        # Communication
        self.menuChangeLanguage(self.plcConnectionMenu, "selectCommunicationMenu")
        self.menuChangeLanguage(self.plcConnectionMenu, "viaEthernetClient")
        self.menuChangeLanguage(self.plcConnectionMenu, "viaEthernetServer")
        self.menuChangeLanguage(self.plcConnectionMenu, "viaSerial")

        self.menuChangeLanguage(self.selectCommunicationMenu, "viaEthernetClient")
        self.menuChangeLanguage(self.selectCommunicationMenu, "viaEthernetServer")
        self.menuChangeLanguage(self.selectCommunicationMenu, "viaSerial")

        self.menuChangeLanguage(self.plcEthernetClientMenu, "setting")
        self.menuChangeLanguage(self.plcEthernetClientMenu, "connect")
        self.menuChangeLanguage(self.plcEthernetClientMenu, "disconnect")
        self.menuChangeLanguage(self.plcEthernetClientMenu, "sendTest")

        self.menuChangeLanguage(self.plcEthernetServerMenu, "setting")
        self.menuChangeLanguage(self.plcEthernetServerMenu, "connect")
        self.menuChangeLanguage(self.plcEthernetServerMenu, "disconnect")
        self.menuChangeLanguage(self.plcEthernetServerMenu, "sendTest")

        self.menuChangeLanguage(self.plcSerialMenu, "setting")
        self.menuChangeLanguage(self.plcSerialMenu, "connect")
        self.menuChangeLanguage(self.plcSerialMenu, "disconnect")
        self.menuChangeLanguage(self.plcSerialMenu, "sendTest")

        # Light menu
        self.menuChangeLanguage(self.lightMenu, "connect")
        self.menuChangeLanguage(self.lightMenu, "disconnect")
        self.menuChangeLanguage(self.lightMenu, "settingLightConnection")
        self.menuChangeLanguage(self.lightMenu, "turnOn")
        self.menuChangeLanguage(self.lightMenu, "turnOff")
        self.menuChangeLanguage(self.lightMenu, "settingLightValue")
        self.menuChangeLanguage(self.lightMenu, "refresh")

        # Server menu
        self.menuChangeLanguage(self.serverMenu, "setting")
        self.menuChangeLanguage(self.serverMenu, "connect")
        self.menuChangeLanguage(self.serverMenu, "disconnect")
        self.menuChangeLanguage(self.serverMenu, "test")

        # data config menu
        self.menuChangeLanguage(self.dataConfigMenu, "setting")
        self.menuChangeLanguage(self.dataConfigMenu, "convertPosFromCad")


        # Tabbar
        self.tabBar.tab(tab_id=0, text= self.languageManager.localized("running tab"))
        self.tabBar.tab(tab_id=1, text= self.languageManager.localized("algorithm tab"))
        self.tabBar.tab(tab_id=2, text= self.languageManager.localized("model setting"))
        self.tabBar.tab(tab_id=3, text= self.languageManager.localized("axis system setting"))

    def menuChangeLanguage(self, menu, key):
        _menu: Menu = menu
        _menu.entryconfigure(_menu.index(self.languageManager.localizedLastLanguage(key)),
                             label=self.languageManager.localized(key))

    def setupWindow(self):
        self.setupMainWindow()
        self.setupMenus()
        self.setupImageFrame()
        self.setupRu_connectorImageFrame()
        self.setupTabControl()
        self.setupBottomFrame()
        self.setImageResultVisible()


    def setupMainWindow(self):
        self.mainFrame.title(self.languageManager.localized("version"))
        iconPath = CommonAssit.resource_path("resource\\appIcon.ico")
        self.mainFrame.iconbitmap("resource\\appIcon.ico")
        self.mainFrame.geometry("1240x665")
        self.mainFrame.state("zoomed")
        # self.mainFrame.resizable(0, 0)
        self.mainFrame.protocol("WM_DELETE_WINDOW", self.exit)
        self.mainFrame.bind("<Key>", func=self.keyInput)
    def keyInput(self, event):
        if event.keysym == "x":
            self.cutImage()
        elif event.keysym == "Left":
            self.workingThread.show_previous_image()
        elif event.keysym == "Right":
            self.workingThread.show_next_image()
    def setupMenus(self):
        self.rootMenu = VisionMenu(self.mainFrame)
        self.mainFrame.config(menu=self.rootMenu)
        # Camera config menu
        self.cameraConfigMenu = VisionMenu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label='Camera', menu=self.cameraConfigMenu)
        self.cameraConfigMenu.add_command(label=self.languageManager.localized("setting"), command=self.workingThread.cameraManager.setting)
        self.cameraConfigMenu.add_command(label=self.languageManager.localized("Calibration"), command=self.clickCameraCalibration)
        self.selectCameraMenu = VisionMenu(self.cameraConfigMenu, tearoff=0)
        self.cameraConfigMenu.add_cascade(label=self.languageManager.localized("cameraSelect"), menu=self.selectCameraMenu)
        for i in range(10):
            self.selectCameraMenu.add_command(label="Camera {}".format(i),command=MenuCallBack(i, self.workingThread.cameraManager.changeCamera))

        self.cameraConfigMenu.add_command(label=self.languageManager.localized("connect"), command=self.workingThread.connectCamera)
        self.cameraConfigMenu.add_command(label=self.languageManager.localized("disconnect"), command=self.workingThread.disconnectCamera)
        self.cameraConfigMenu.add_command(label=self.languageManager.localized("capturePicture"), command=self.workingThread.capturePicture)
        self.cameraConfigMenu.add_command(label=self.languageManager.localized("captureVideo"), command=self.workingThread.captureVideo)
        self.cameraConfigMenu.add_command(label=self.languageManager.localized("stopCaptureVideo"), command=self.workingThread.stopCaptureVideo)

        self.load_camera_feature_menu = VisionMenu(self.cameraConfigMenu, tearoff=0)
        self.cameraConfigMenu.add_cascade(label=self.languageManager.localized("loadFeature"), menu=self.load_camera_feature_menu)
        self.load_camera_feature_menu.add_command(label=self.languageManager.localized("available"), command=self.workingThread.cameraManager.load_available_feature)
        self.load_camera_feature_menu.add_command(label=self.languageManager.localized("new"), command=self.workingThread.cameraManager.load_new_feature)

        self.record_camera_menu = VisionMenu(self.cameraConfigMenu, tearoff=0)
        self.cameraConfigMenu.add_cascade(label="Record", menu=self.record_camera_menu)
        self.record_camera_menu.add_command(label="Start",
                                                  command=self.workingThread.cameraManager.start_record_camera)
        self.record_camera_menu.add_command(label="Pause",
                                                  command=self.workingThread.cameraManager.pause_record_camera)
        self.record_camera_menu.add_command(label="Stop",
                                            command=self.workingThread.cameraManager.stop_record_camera)

        # Image menu:
        self.imageMenu = VisionMenu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label=self.languageManager.localized("image"), menu=self.imageMenu)

        self.newImageMenu = VisionMenu(self.imageMenu, tearoff=0)
        self.imageMenu.add_cascade(label=self.languageManager.localized("new"), menu=self.newImageMenu)
        self.newImageMenu.add_command(label=self.languageManager.localized("blackImage"), command=self.workingThread.newBlackImage)
        self.newImageMenu.add_command(label=self.languageManager.localized("whiteImage"), command=self.workingThread.newWhiteImage)

        self.imageMenu.add_command(label=self.languageManager.localized('open'), command=self.workingThread.openImage)
        self.imageMenu.add_command(label=self.languageManager.localized("currentModelDesign"), command=self.workingThread.drawCurrentModelDesign)

        # draw menu
        self.drawMenu = VisionMenu(self.imageMenu, tearoff=0)
        self.imageMenu.add_cascade(label=self.languageManager.localized("draw"), menu=self.drawMenu)

        self.drawMenu.add_command(label=self.languageManager.localized("on"), command=self.drawOn)
        self.drawMenu.add_command(label="Draw cross", command=self.draw_cross)
        self.drawMenu.add_command(label="Draw rectangle", command=self.click_draw_rec)
        self.drawMenu.add_command(label="Draw circle", command=self.click_draw_circle)
        self.drawMenu.add_command(label=self.languageManager.localized("off"), command=self.drawOff)

        # cut image menu
        self.cutImageMenu = VisionMenu(self.imageMenu, tearoff=0)
        self.imageMenu.add_cascade(label="Cut Image", menu=self.cutImageMenu)

        self.cutImageMenu.add_command(label="Save Directory", command=self.chooseCutImageSaveDir)

        # image save menu
        self.imageSaveMenu = VisionMenu(self.imageMenu, tearoff=0)
        self.imageMenu.add_cascade(label=self.languageManager.localized("save"), menu=self.imageSaveMenu)
        self.imageSaveMenu.add_command(label=self.languageManager.localized("originalImage"), command=self.workingThread.saveOriginalImage)
        self.imageSaveMenu.add_command(label=self.languageManager.localized("processingImage"), command=self.workingThread.saveProcessedImage)

        # Screen record menu
        self.screenRecordMenu = VisionMenu(self.imageMenu, tearoff=0)
        self.imageMenu.add_cascade(label="Screen Record", menu=self.screenRecordMenu)
        self.screenRecordMenu.add_command(label="Start", command=self.startRecord)
        self.screenRecordMenu.add_command(label="Pause", command=self.pausedRecord)
        self.screenRecordMenu.add_command(label="Stop", command=self.stopRecord)

        # Image Result visible
        self.imageResultVisible = VisionMenu(self.imageMenu, tearoff=0)
        self.imageMenu.add_cascade(menu=self.imageResultVisible, label="Image Result Visible")
        self.imageResultVisible.add_command(label="Show", command=lambda:self.setImageResultVisible(True))
        self.imageResultVisible.add_command(label="Hide", command=lambda:self.setImageResultVisible(False))

        # Image View Setting
        self.imageMenu.add_command(label="Image View Setting", command=self.clickImageViewSetting)

        # Communication menu
        self.plcConnectionMenu = VisionMenu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label=self.languageManager.localized("CommunicationMenu"), menu=self.plcConnectionMenu)

        # Select communication type
        self.selectCommunicationMenu = VisionMenu(self.plcConnectionMenu, tearoff=0)
        self.plcConnectionMenu.add_cascade(label=self.languageManager.localized("selectCommunicationMenu"), menu=self.selectCommunicationMenu)

        self.selectCommunicationMenu.add_command(label=self.languageManager.localized("viaEthernetClient"), command=lambda:self.selectCommunicationType(ConnectionType.ethernetClient.value))
        self.selectCommunicationMenu.add_command(label=self.languageManager.localized("viaEthernetServer"), command=lambda:self.selectCommunicationType(ConnectionType.ethernetServer.value))
        self.selectCommunicationMenu.add_command(label=self.languageManager.localized("viaSerial"), command=lambda:self.selectCommunicationType(ConnectionType.serial.value))

        #   Connection PLC via ethernet Client
        self.plcEthernetClientMenu = VisionMenu(self.plcConnectionMenu, tearoff=0)
        self.plcConnectionMenu.add_cascade(label=self.languageManager.localized("viaEthernetClient"), menu=self.plcEthernetClientMenu)

        self.plcEthernetClientMenu.add_command(label=self.languageManager.localized("setting"), command=self.workingThread.connectionManager.setting)
        self.plcEthernetClientMenu.add_command(label=self.languageManager.localized("connect"), command=self.workingThread.connectionManager.connect)
        self.plcEthernetClientMenu.add_command(label=self.languageManager.localized("disconnect"), command=self.workingThread.connectionManager.disconnect)
        self.plcEthernetClientMenu.add_command(label=self.languageManager.localized("sendTest"), command=self.workingThread.connectionManager.sendTest)

        #   Connection PLC via ethernet Server
        self.plcEthernetServerMenu = VisionMenu(self.plcConnectionMenu, tearoff=0)
        self.plcConnectionMenu.add_cascade(label=self.languageManager.localized("viaEthernetServer"),
                                           menu=self.plcEthernetServerMenu)

        self.plcEthernetServerMenu.add_command(label=self.languageManager.localized("setting"),
                                               command=self.workingThread.connectionManager.setting)
        self.plcEthernetServerMenu.add_command(label=self.languageManager.localized("connect"),
                                               command=self.workingThread.connectionManager.connect)
        self.plcEthernetServerMenu.add_command(label=self.languageManager.localized("disconnect"),
                                               command=self.workingThread.connectionManager.disconnect)
        self.plcEthernetServerMenu.add_command(label=self.languageManager.localized("sendTest"),
                                               command=self.workingThread.connectionManager.sendTest)



        #   Connection PLC via Serial
        self.plcSerialMenu = VisionMenu(self.plcConnectionMenu, tearoff=0)
        self.plcConnectionMenu.add_cascade(label=self.languageManager.localized("viaSerial"), menu=self.plcSerialMenu)

        self.plcSerialMenu.add_command(label=self.languageManager.localized("setting"), command=self.workingThread.connectionManager.setting)
        self.plcSerialMenu.add_command(label=self.languageManager.localized("connect"), command=self.workingThread.connectionManager.connect)
        self.plcSerialMenu.add_command(label=self.languageManager.localized("disconnect"), command=self.workingThread.connectionManager.disconnect)
        self.plcSerialMenu.add_command(label=self.languageManager.localized("sendTest"), command=self.workingThread.connectionManager.sendTest)

        # Light
        self.lightMenu = VisionMenu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label= self.languageManager.localized("light"), menu=self.lightMenu)
        self.lightMenu.add_command(label=self.languageManager.localized("settingLightConnection"), command=self.workingThread.light.setting)
        self.lightMenu.add_command(label=self.languageManager.localized("connect"), command=self.workingThread.light.connect)
        self.lightMenu.add_command(label=self.languageManager.localized("disconnect"), command=self.workingThread.light.disconnectLight)
        self.lightMenu.add_command(label=self.languageManager.localized("turnOn"), command=self.workingThread.light.turnOn)
        self.lightMenu.add_command(label=self.languageManager.localized("turnOff"), command=self.workingThread.light.turnOff)
        self.lightMenu.add_command(label=self.languageManager.localized("settingLightValue"), command=self.workingThread.light.test)
        self.lightMenu.add_command(label=self.languageManager.localized("refresh"), command=self.workingThread.light.refresh)

        self.light_hard_test_menu = VisionMenu(self.lightMenu, tearoff=0)
        self.lightMenu.add_cascade(label="Hard Test", menu=self.light_hard_test_menu)
        self.light_hard_test_menu.add_command(label="Start", command=self.workingThread.light.start_hard_test)
        self.light_hard_test_menu.add_command(label="Stop", command=self.workingThread.light.stop_hard_test)

        # Server
        self.serverMenu = VisionMenu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label=self.languageManager.localized("server"), menu=self.serverMenu)
        self.serverMenu.add_command(label=self.languageManager.localized("setting"), command=self.workingThread.server.setting)
        self.serverMenu.add_command(label=self.languageManager.localized("connect"), command=self.workingThread.server.connectServer)
        self.serverMenu.add_command(label=self.languageManager.localized("disconnect"), command=self.workingThread.server.disconnectSever)
        self.serverMenu.add_command(label=self.languageManager.localized("test"), command=self.workingThread.server.test)


        # Data Config menu
        self.dataConfigMenu = VisionMenu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label=self.languageManager.localized("dataConfig"), menu=self.dataConfigMenu)
        self.dataConfigMenu.add_command(label=self.languageManager.localized("setting"), command=self.clickSettingData)

        self.dataConfigMenu.add_command(label=self.languageManager.localized("convertPosFromCad"), command=self.clickConvertScrewPosFromCAD)

        self.languageMenu = VisionMenu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label=self.languageManager.localized("LanguagesMenu"), menu=self.languageMenu)
        for lang in self.languageManager.lang_list:
            self.languageMenu.add_command(label=lang, command=MenuCallBack(lang, self.languageManager.changeLanguage))

        # reset error
        self.rootMenu.add_command(label=self.languageManager.localized("reset error"), command=self.resetError)

        # zoom menu
        self.zoomMenu = VisionMenu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label="Zoom", menu=self.zoomMenu)

        self.zoomMenu.add_command(label="Zoom++")
        self.zoomMenu.add_command(label="Zoom--")
        self.zoomMenu.add_command(label="Reset", command=self.resetZoom)

    def resetZoom(self):
        self.showImage(self.zoomImage)
        self.resetBasePoint()
        self.zoomImage = None
        self.zoomScale = 100
        self.multipleScale = 10
        self.rootMenu.entryconfigure(self.rootMenu.index(self.zoomLabel), label="Zoom")
        self.zoomLabel = "Zoom"

    def resetError(self):
        self.showBottomMiddleText("")

    # tabbarSrollView: ScrollView
    def setupTabControl(self):
        # has scroll bar
        # self.tabbarSrollView = ScrollView(self.mainFrame, displayHeight=922, displayWidth=599, borderwidth=0)
        # self.tabbarSrollView.place(relx=0.67, rely=0.015, relwidth=0.325, relheight=0.93)
        #
        #
        # self.tabBarFrame = VisionFrame(self.tabbarSrollView.display, borderwidth=0.5)
        # self.tabBarFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        #
        # no scroll bar
        self.tabBarFrame = VisionFrame(self.mainFrame, borderwidth=0.5)
        self.tabBarFrame.place(relx=0.67, rely=0.015, relwidth=0.325, relheight=0.93)

        self.tabBar = VisionNotebook(self.tabBarFrame)
        self.tabBar.bind("<<NotebookTabChanged>>", self.tabBarSelectChange)
        self.tabBar.place(x=0, y=0, relwidth=1, relheight=1)

        self.runningTab = RunningTab(self.tabBar, self)
        self.researchingTab = ResearchingTab(root=self.tabBar, workerThread=self.workingThread, mainWindow=self)
        self.modelSettingTab = ModelSettingTab(root=self.tabBar, mainWindow=self)
        self.as_setting_tab = AS_SettingTab(root=self.tabBar, mainWindow=self)


        self.tabBar.add(self.runningTab, text=self.languageManager.localized("running tab"))
        self.tabBar.add(self.researchingTab, text=self.languageManager.localized("algorithm tab"))
        self.tabBar.add(self.modelSettingTab, text=self.languageManager.localized("model setting"))
        self.tabBar.add(self.as_setting_tab, text=self.languageManager.localized("axis system setting"))

    def setupBottomFrame(self):
        self.bottomLeftFrame = VisionFrame(self.mainFrame)
        self.bottomLeftFrame.place(relx=0.005, rely=0.96, relwidth=0.3, relheight=0.03)
        self.bottomLeftLabel = VisionLabel(self.bottomLeftFrame, text='')
        self.bottomLeftLabel.place(x =0, y =0)

        self.bottomMiddleFrame = VisionFrame(self.mainFrame)
        self.bottomMiddleFrame.place(relx=0.305, rely=0.946, relwidth=0.4, relheight=0.054)

        self.bottomMiddleLabel = VisionLabel(self.bottomMiddleFrame, fg='red', wraplength=622)
        self.bottomMiddleLabel.place(relx=0, rely=0, relwidth=1, relheight=1)


        self.bottomRightFrame = VisionFrame(self.mainFrame)
        self.bottomRightFrame.place(relx=0.705, rely=0.946, relwidth=0.295, relheight=0.054)

        try:
            self.logoView = LogoView(self.bottomRightFrame, imagePath="./resource/logo.png")
            self.logoView.place(relx=0.4, rely=0, relwidth=0.6,relheight=1)
        except Exception as error:
            self.showError("Cannot find logo.png. Check in resource folder!\nDetail: {}".format(error))

    logoView: LogoView

    def clickImageViewSetting(self):
        ImageViewSettingWindow(mainWindow=self)

    def changeImageViewSetting(self):
        self.imageView.place(relx=(1 - self.commonSettingManager.settingParm.imageViewDimension[0]) / 2,
                             rely=(1 - self.commonSettingManager.settingParm.imageViewDimension[1]) / 2,
                             relwidth=self.commonSettingManager.settingParm.imageViewDimension[0],
                             relheight=self.commonSettingManager.settingParm.imageViewDimension[1])

    def setImageResultVisible(self, show=None):
        if show is not None:
            self.commonSettingManager.settingParm.imageResultFrameVisible = show
        if self.commonSettingManager.settingParm.imageResultFrameVisible:
            self.imageResultFrame.place(relx=0.015, rely=0.015, relwidth=0.08, relheight=0.08)
        else:
            self.imageResultFrame.place_forget()
        self.commonSettingManager.save()

    def showImageOKLabel(self):
        self.image_OK_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.image_NG_label.place_forget()

    def showImageNGLabel(self):
        self.image_OK_label.place_forget()
        self.image_NG_label.place(relx=0, rely=0, relwidth=1, relheight=1)

    def setupImageFrame(self):
        self.imageFrame = VisionFrame(self.mainFrame, borderwidth=0.5, bg=Color.winWhite())
        self.imageFrame.place(relx=0.015, rely=0.015, relwidth=0.64, relheight=0.91)
        self.imageTitle = VisionLabel(self.mainFrame)
        self.imageTitle.place(relx=0.015, rely=0.925, relwidth=0.64, relheight=0.02)

        self.imageResultFrame = VisionFrame(self.mainFrame, bg=Color.winWhite())
        self.image_OK_label = VisionLabel(self.imageResultFrame, bg=Color.winWhite(), fg=Color.winLame(),
                                          text="OK", font=VisionFont.boldFont(45))
        self.image_NG_label = VisionLabel(self.imageResultFrame, bg=Color.winWhite(), fg=Color.winRed(),
                                          text="NG", font=VisionFont.boldFont(45))

        vscrollbar = ttk.Scrollbar(self.imageFrame, orient=VERTICAL)
        # vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        vscrollbar.place(x=0, y=0, width=0, height=0)
        self.imageView = Canvas(self.imageFrame, yscrollcommand=vscrollbar.set)
        vscrollbar.config(command=self.imageView.yview)
        self.imageView.bind_all("<MouseWheel>", self.imageViewMouseEvent)
        self.imageView.bind('<Enter>', self._bound_to_mousewheel)
        self.imageView.bind('<Leave>', self._unbound_to_mousewheel)
        self.imageView.bind("<Button-3>", self.imageViewMouseEvent)
        self.imageView.bind("<Button-2>", self.imageViewMouseEvent)
        self.imageView.bind("<Button-1>", self.imageViewMouseEvent)
        self.imageView.bind("<ButtonRelease-1>", self.imageViewMouseEvent)
        self.imageView.bind("<ButtonRelease-2>", self.imageViewMouseEvent)
        self.imageView.bind("<B1-Motion>", self.imageViewMouseEvent)
        self.imageView.bind("<B2-Motion>", self.imageViewMouseEvent)
        self.imageView.bind("<Motion>", self.imageViewMotion)
        self.imageView.bind("<Configure>", self.onImageViewResize)

        # self.imageView.bind("<Button-4>", self.imageViewMouseEvent)
        # self.imageView.bind("<Button-5>", self.imageViewMouseEvent)

        self.imageView.place(relx=(1-self.commonSettingManager.settingParm.imageViewDimension[0]) / 2,
                             rely=(1 - self.commonSettingManager.settingParm.imageViewDimension[1]) /2,
                             relwidth=self.commonSettingManager.settingParm.imageViewDimension[0],
                             relheight=self.commonSettingManager.settingParm.imageViewDimension[1])

        photo = cv.imdecode(np.fromfile("./resource/photo.png", dtype=np.uint8), cv.IMREAD_COLOR)
        self.showImage(image=photo)

        self.stateLabel = Label(self.mainFrame, text="STATE", font=VisionFont.boldFont(32), fg="#00FF00", bg="#F9E79F")
        # self.stateLabel.place(relx=0.005, rely=0.015, width=300)

        self.previous_image_btn = PreviousButton(self.mainFrame, command=self.workingThread.show_previous_image)
        self.previous_image_btn.place(relx=0, rely=0.45, relwidth=0.015, relheight=0.06)

        self.next_image_btn = NextButton(self.mainFrame, command=self.workingThread.show_next_image)
        self.next_image_btn.place(relx=0.655, rely=0.45, relwidth=0.015, relheight=0.06)

    def cutImage(self):
        global pressImage
        cutImage = pressImage[min(self.choose_area[1],self.choose_area[3]):max(self.choose_area[1],self.choose_area[3]),
                            min(self.choose_area[0], self.choose_area[2]):max(self.choose_area[0], self.choose_area[2])]
        image_path = f"{self.commonSettingManager.settingParm.cutImageSaveDir}/{TimeControl.y_m_d_H_M_S_format()}.png"
        cv.imencode(".png", cutImage)[1].tofile(image_path)
        self.showImage(cutImage, title=self.currentImageTitle)
    stateLabel: Label
    def showStateLabel(self):
        self.stateLabel.place(relx=0.005, rely=0.015, width=300)
    def hideStateLabel(self):
        self.stateLabel.place_forget()

    def _bound_to_mousewheel(self, event):
        self.imageView.bind_all("<MouseWheel>", self.imageViewMouseEvent)
        self.imageViewMouseEvent(event=event)

    def _unbound_to_mousewheel(self, event):
        self.imageView.unbind_all("<MouseWheel>")
    # def clickCameraSetting(self):
        # cameraSetting = CameraSettingWindow(self)
        # return
    def setupRu_connectorImageFrame(self):
        self.ru_connectorImageFrame = Ru_ConnectorImageFrame(self.imageFrame, self)
        # self.ru_connectorImageFrame.show()

    def tabBarSelectChange(self, event):
        self.runningTab.isSelected = False
        self.modelSettingTab.isSelected = False
        self.researchingTab.isSelected = False
        if not self.tabBar.select().__contains__("running"):
            if TimeControl.time() - self.check_pw_time > 600000:
                password_window = PW_Input_Window(self)
                password_window.wait_window()
                if password_window.passed:
                    self.check_pw_time = TimeControl.time()
                else:
                    self.tabBar.select(TabId.runningTab.value)

        if self.tabBar.select().__contains__("modelsetting"):
            if self.startingWindow.machineName is not None and self.startingWindow.machineName.isRUConnectorScrewMachine():
                self.ru_connectorImageFrame.hide()
            self.modelSettingTab.isSelected = True
        elif self.tabBar.select().__contains__("researching"):
            if self.startingWindow.machineName is not None and self.startingWindow.machineName.isRUConnectorScrewMachine():
                self.ru_connectorImageFrame.hide()
            self.researchingTab.isSelected = True
            self.researchingTab.updateAlgorithmForChangeModel()
        elif self.tabBar.select().__contains__("running"):
            if self.startingWindow.machineName is not None and self.startingWindow.machineName.isRUConnectorScrewMachine():
                self.ru_connectorImageFrame.show()
                self.ru_ConnectorUpdateModel()
            self.runningTab.isSelected = True
        elif self.tabBar.select().__contains__("axissytemsetting"):
            print(self.tabBar.select())

        if not self.tabBar.select().__contains__("modelsetting"):
            self.modelSettingTab.modelSelected(None)


    def ru_ConnectorUpdateModel(self):
        self.workingThread.ru_connectorCheckMissing.updateModel()
        self.ru_connectorImageFrame.show()
        self.ru_connectorImageFrame.showDesignImage()
        if self.workingThread.ru_connectorCheckMissing.ringRecognizeAlgorithm is None \
            or self.workingThread.ru_connectorCheckMissing.screwRecognizeAlgorithm is None:
            messagebox.showinfo("Model Setting", "Please choose algorithms in setting model")
        else:
            self.ru_connectorImageFrame.showOkRingImage()
            self.ru_connectorImageFrame.showOkScrewImage()

    def selectCommunicationType(self, type="Serial"):
        self.commonSettingManager.settingParm.communicationType = type
        self.commonSettingManager.save()
        self.runningTab.resultTab.commonSettingFrame.updateInfo()

    chessboardCalibration: ChessboardCalibrationFrame = None
    def clickCameraCalibration(self):
        if self.chessboardCalibration is None:
            self.chessboardCalibration = ChessboardCalibrationFrame(self.mainFrame, self)
        self.chessboardCalibration.place(relx=0.67, rely=0.015, relwidth=0.325, relheight=0.93)
        self.chessboardCalibration.updateValue()

    def init_chessboard_cali_frame(self):
        self.chessboardCalibration = ChessboardCalibrationFrame(self.mainFrame, self)

    def startRecord(self):
        recordThread = threading.Thread(target=self.screenRecordThread, args=())
        recordThread.start()

    def stopRecord(self):
        self.isRecording = False

    def pausedRecord(self):
        self.isPaused = not self.isPaused

    def screenRecordThread(self):
        self.isRecording =  True
        # codec = cv.VideoWriter_fourcc(*"XVID")
        fourcc = cv.VideoWriter_fourcc(*"XVID")
        SCREEN_SIZE = (1920, 1080)
        tempPath = "./Recorded.avi"
        out = cv.VideoWriter(tempPath, fourcc, 13,
                             SCREEN_SIZE)  # Here screen resolution is 1366 x 768, you can change it depending upon your need
        while self.isRecording:
            if not self.isPaused:
                img = pyautogui.screenshot()  # capturing screenshot
                frame = np.array(img)  # converting the image into numpy array representation
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  # converting the BGR image into RGB image
                out.write(frame)  # writing the RBG image to file
            TimeControl.sleep(1)
        out.release()  # closing the video file
        self.isRecording = False
        self.isPaused = False
        fileName = filedialog.asksaveasfilename(title='Select Image',
                                                  filetypes=(('AVI Files','*.avi'),('All files', '*.*')),
                                                  initialdir="/áéá")

        if fileName != "":
            if not fileName.endswith(".avi"):
                fileName = fileName + ".avi"
            PathFileControl.deleteFile(fileName)
            PathFileControl.rename(tempPath, fileName)

    def drawOn(self):
        self.drawFlag = True

    def click_draw_rec(self):
        self.commonSettingManager.settingParm.draw_rectangle = True
        self.commonSettingManager.settingParm.draw_circle = False
        self.commonSettingManager.save()

    def click_draw_circle(self):
        self.commonSettingManager.settingParm.draw_rectangle = False
        self.commonSettingManager.settingParm.draw_circle = True
        self.commonSettingManager.save()

    def draw_cross(self):
        if self.cross_horizontal is None:
            self.cross_vertical = Frame(self.mainFrame, bg="#82E0AA")
            self.cross_horizontal = Frame(self.mainFrame, bg="#82E0AA")

        self.cross_vertical.place(relx=0.3225, rely=0.065, relwidth=0.01, relheight=0.83)
        self.cross_horizontal.place(relx=0.045, rely=0.4625, relwidth=0.57, relheight=0.02)

    cross_vertical: Frame = None
    cross_horizontal: Frame = None

    def hide_cross(self):
        self.cross_vertical.place_forget()
        self.cross_horizontal.place_forget()

    def drawOff(self):
        self.drawFlag = False
        self.hide_cross()

    def chooseCutImageSaveDir(self):
        saveFolder = filedialog.askdirectory(title="Select Cut Image Dir", initialdir="/áéá")
        self.commonSettingManager.settingParm.cutImageSaveDir = saveFolder
        self.commonSettingManager.save()

    def connectCamera(self):
        self.workingThread.connectCamera()

    def clickSettingData(self):
        return

    def clickConvertScrewPosFromCAD(self):
        ConvertFromCADWindow(self)

    def showOriginalImage(self):
        if self.originalImage is not None:
            self.showImage(self.originalImage, True)
    #
    # def showImage(self, image, original = False, isZoomImage=False):
    #     showImageThread = threading.Thread(target=self.showImage, args=(image, original, isZoomImage))
    #     showImageThread.start()

    def showImage(self, image, original = False, isZoomImage=False, title=None):
        if image is None or len(image) == 0:
            messagebox.showerror("Image Error", "The image wanted to show is empty!")
            return
        _image = image.copy()
        isRUConnectorMachine = False
        try:
            isRUConnectorMachine = self.startingWindow.machineName.isRUConnectorScrewMachine()
        except:
            pass

        # show image in connector machine tab
        if isRUConnectorMachine and self.runningTab.isSelected:
            self.ru_connectorImageFrame.currentImageView.showImage(_image)

        # set zoom image if is the first zoom
        if isZoomImage and self.zoomImage is None:
            self.zoomImage = self.currentImage.copy()

        # set original image
        if original:
            self.resetBasePoint()
            self.originalImage = image.copy()
            self.currentImage = image.copy()
            self.algorithmManager.reset_last_execute_step()
        else:
            self.currentImage = image.copy()

        # recalculate the coefficient from canvas size to real image size
        shape = _image.shape
        self.widthCoef = shape[1] / self.imageView.winfo_width()
        self.heightCoef = shape[0] / self.imageView.winfo_height()

        # convert color to suitable for canvas showing color
        if len(shape) == 3:
            try:
                _image = cv.cvtColor(_image, cv.COLOR_BGR2RGB)
            except:
                pass
        else:
            try:
                _image = cv.cvtColor(_image, cv.COLOR_GRAY2RGB)
            except:
                pass
        # resize image to fit the canvas
        _image = cv.resize(_image, (self.imageView.winfo_width(), self.imageView.winfo_height()))

        # convert opencv image to photo image to show on canvas
        try:
            self.imageShow = ImageTk.PhotoImage(Image.fromarray(_image))
        except:
            self.imageShow = ImageTk.PhotoImage(Image.fromarray((_image * 255).astype(np.uint8)))

        self.imageView.create_image(0, 0, anchor=NW, image=self.imageShow)
        self.imageView.image = self.imageShow
        if title is None:
            self.imageTitle.set(self.currentImageTitle)
        else:
            self.imageTitle.set(title)
            self.currentImageTitle = title
        self.mainFrame.update()

    def onImageViewResize(self,event):
        if hasattr(self, "originalImage") and self.currentImage is not None:
            self.showImage(self.currentImage, original=False)

    def resetBasePoint(self):
        self.basePoint = [0, 0, 0, 0]
        self.zoomImage = None
        self.zoomScale = 100


    def imageViewMotion(self, event):
        realPosX = int(event.x * self.widthCoef)
        realPosY = int(event.y * self.heightCoef)

        if self.currentImage is None:
            return

        realChanel = 1 if len(self.currentImage.shape) < 3 else 3
        color = ""
        try:
            color = self.currentImage[realPosY, realPosX]
        except:
            pass
        realHeight = 0
        realWidth = 0
        try:
            realHeight = self.currentImage.shape[0]
            realWidth = self.currentImage.shape[1]
        except:
            pass

        if realPosX < 0 or realPosX > realWidth or realPosY < 0 or realPosY > realHeight:
            return
        if realChanel > 1:
            textShow = f"(x, y) = ({realPosX}, {realPosY})   |    Color = ({color})"
        else:
            textShow = f"(x, y) = ({realPosX}, {realPosY})   |    Color = ({color})"


        if textShow != "":
            self.showBottomLeftText(textShow)

    def imageViewMouseEvent(self, event):

        global realChanel, realHeight, realWidth
        global startX, startY, endX, endY
        global pressImage
        global buttonID
        global justMove
        global isMiddleMouseMove
        global temporaryBasePoint
        # verify the mouse coordinates
        realChanel = 1
        realPosX = int(event.x * self.widthCoef)
        realPosY = int(event.y * self.heightCoef)

        if self.currentImage is None:
            return

        realChanel = 1 if len(self.currentImage.shape) < 3 else 3
        color = ""

        try:
            color = self.currentImage[realPosY, realPosX]
        except:
            pass

        try:
            realHeight = self.currentImage.shape[0]
            realWidth = self.currentImage.shape[1]
        except:
            pass

        if event.num != "??":
            buttonID = event.num
            print("button ID = {}".format(buttonID))

        else:
            # buttonID = 0
            print("unknown button")

        if realPosX < 0 or realPosX > realWidth or realPosY < 0 or realPosY > realHeight:
            return

        if event.type == EventType.MouseWheel:
            zoomDelta = event.delta / 120
            # print("Mouse wheel delta = {}".format(zoomDelta))
            # print(f"x = {realPosX}, y = {realPosY}")
            # print(f"base point = {self.basePoint}")
            if self.zoomImage is not None:
                baseHeight = self.zoomImage.shape[0]
                baseWidth = self.zoomImage.shape[1]
                # print(f"height={self.zoomImage.shape[0]}, width = {self.zoomImage.shape[1]}")
            else:
                self.zoomImage = self.currentImage.copy()
                baseHeight = self.currentImage.shape[0]
                baseWidth = self.currentImage.shape[1]
                # print(f"height={self.currentImage.shape[0]}, width = {self.currentImage.shape[1]}")

            zoomDelta = int(zoomDelta * self.multipleScale)
            print(f"zoom Delta = {zoomDelta}")

            if self.zoomScale + zoomDelta > 100:
                self.zoomScale =  self.zoomScale + zoomDelta
                # print(f"zoom scale = {self.zoomScale}")

                zoomHeight = int(100 * baseHeight / self.zoomScale)
                zoomWidth = int(100 * baseWidth / self.zoomScale)
                # print(f"zoom height = {zoomHeight}, zoom width = {zoomWidth}")

                zoomCusorX = self.basePoint[0] + realPosX
                zoomCusorY = self.basePoint[1] + realPosY

                zoomCenterX = self.basePoint[0] + int(self.currentImage.shape[1] / 2)
                zoomCenterY = self.basePoint[1] + int(self.currentImage.shape[0] / 2)

                startZoomX = zoomCenterX - int(zoomWidth / 2)
                startZoomY = zoomCenterY - int(zoomHeight / 2)

                realCusorXAfterZoom = startZoomX + int(event.x * zoomWidth / self.imageView.winfo_width())
                realCusorYAfterZoom = startZoomY + int(event.y * zoomHeight / self.imageView.winfo_height())

                deltaMoveX = zoomCusorX - realCusorXAfterZoom
                deltaMoveY = zoomCusorY - realCusorYAfterZoom

                startZoomX = startZoomX + deltaMoveX
                startZoomY = startZoomY + deltaMoveY

                endZoomX = startZoomX + zoomWidth
                endZoomY = startZoomY + zoomHeight

                # print(f"deltaMove X = {deltaMoveX}, delta move y = {deltaMoveY}")


                if startZoomX < 0:
                    startZoomX = 0
                    endZoomY = startZoomX + zoomWidth
                if endZoomX > baseWidth:
                    endZoomX = baseHeight
                    startZoomX = baseHeight - zoomWidth
                if startZoomY < 0:
                    startZoomY = 0
                    endZoomY = startZoomY + zoomHeight
                if endZoomY > baseHeight:
                    endZoomY = baseHeight
                    startZoomY = baseHeight - zoomHeight

                self.currentImage = self.zoomImage[startZoomY: endZoomY, startZoomX: endZoomX]
                self.showImage(self.currentImage)
                self.basePoint = (startZoomX, startZoomY, zoomWidth, zoomHeight)

            else:
                self.currentImage = self.zoomImage.copy()
                self.showImage(self.currentImage)
                self.zoomImage = None

        if event.type == EventType.ButtonPress and buttonID == 1:
            # left button press
            justMove = False
            pressImage = self.currentImage.copy()
            self.showImage(self.currentImage, False)
            # print("button 1 Press")
            startX = realPosX
            startY = realPosY

        if event.type == EventType.ButtonRelease and buttonID == 1:
            endX = realPosX
            endY = realPosY
            self.currentImage = pressImage.copy()
            # print("delta X End = {}, delta Y End = {}".format(endX - startX, endY - startY))
        try:
            if event.type == EventType.Enter and justMove:
                justMove = False
                self.currentImage = pressImage.copy()
        except:
            pass

        if event.type == EventType.ButtonPress and buttonID == 3:
            try:
                if self.commonSettingManager.settingParm.draw_rectangle:
                    if min(startX, endX) <= realPosX <= max(startX, endX) and min(startY, endY) <= realPosY <= max(startY, endY):
                        rightClickMenu = RightClickImageOption(self.imageView, self)
                        rightClickMenu.setParameter(startX=min(startX, endX), startY=min(startY, endY), endX=max(endX, startX), endY=max(endY, startY), processImage=self.currentImage)
                        try:
                            rightClickMenu.tk_popup(event.x_root, event.y_root)
                        finally:
                            rightClickMenu.grab_release()
                    else:
                        self.showImage(self.currentImage, False)
                        rightClickMenu = RightClickImageOption(self.imageView, self)
                        rightClickMenu.setParameter(startX=realPosX, startY=realPosY, endX=realPosX, endY=realPosY, processImage=self.currentImage)
                        try:
                            rightClickMenu.tk_popup(event.x_root, event.y_root)
                        finally:
                            rightClickMenu.grab_release()
                elif self.commonSettingManager.settingParm.draw_circle:
                    if ImageProcess.calculateDistanceBy2Points((endX, endY), (realPosX, realPosY)) <= ImageProcess.calculateDistanceBy2Points((endX, endY), (startX, startY)):
                        rightClickMenu = RightClickImageOption(self.imageView, self)
                        rightClickMenu.setParameter(circle_center=(endX, endY),
                                                    circle_radius=int(ImageProcess.calculateDistanceBy2Points((endX, endY), (startX, startY))),
                                                    processImage=self.currentImage)
                        try:
                            rightClickMenu.tk_popup(event.x_root, event.y_root)
                        finally:
                            rightClickMenu.grab_release()
                    else:
                        self.showImage(self.currentImage, False)
                        rightClickMenu = RightClickImageOption(self.imageView, self)
                        rightClickMenu.setParameter(startX=realPosX, startY=realPosY, endX=realPosX, endY=realPosY,
                                                    processImage=self.currentImage)
                        try:
                            rightClickMenu.tk_popup(event.x_root, event.y_root)
                        finally:
                            rightClickMenu.grab_release()
            except:
                self.showImage(self.currentImage, False)
                rightClickMenu = RightClickImageOption(self.imageView, self)
                rightClickMenu.setParameter(startX=realPosX, startY=realPosY, endX=realPosX, endY=realPosY,
                                            processImage=self.currentImage)
                try:
                    rightClickMenu.tk_popup(event.x_root, event.y_root)
                finally:
                    rightClickMenu.grab_release()

        if event.type == EventType.Motion and buttonID == 1:
            endX = realPosX
            endY = realPosY
            processImage = None
            if self.commonSettingManager.settingParm.draw_rectangle:
                processImage = cv.rectangle(pressImage.copy(), (startX, startY), (endX, endY), Color.cvGreen(),
                                            self.workingThread.cameraManager.currentCamera.parameter.textThickness, cv.LINE_AA)
                # self.showImage(processImage, original=False)
            elif self.commonSettingManager.settingParm.draw_circle:
                processImage = cv.circle(pressImage.copy(),center=(endX, endY),
                                         radius=int(ImageProcess.calculateDistanceBy2Points((startX, startY), (endX, endY))),
                                         color=Color.cvGreen(),
                                         thickness=self.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                         lineType=cv.LINE_AA)

            self.showImage(processImage, original=False)
            self.choose_area = (startX, startY, endX, endY)

            # print("delta X = {}, delta Y = {}".format(endX - startX, endY - startY))

        if event.type == EventType.ButtonPress and buttonID == 2:
            try:
                if not isMiddleMouseMove:
                    temporaryBasePoint = [self.basePoint[0],
                                          self.basePoint[1],
                                          self.basePoint[2],
                                          self.basePoint[3]]
                else:
                    self.basePoint = [temporaryBasePoint[0],
                                      temporaryBasePoint[1],
                                      temporaryBasePoint[2],
                                      temporaryBasePoint[3]]
            except:
                temporaryBasePoint = [self.basePoint[0],
                                      self.basePoint[1],
                                      self.basePoint[2],
                                      self.basePoint[3]]

            isMiddleMouseMove = False

            startX = realPosX
            startY = realPosY


        if event.type == EventType.Motion and buttonID == 2:
            isMiddleMouseMove = True
            endX = realPosX
            endY = realPosY
            # processImage = cv.line(pressImage.copy(), (startX, startY), (endX, endY), Color.cvGreen(),
            #                             self.workingThread.cameraManager.currentCamera.parameter.textThickness,
            #                             cv.LINE_AA)
            if self.zoomImage is not None:
                if self.basePoint[0] + startX - endX >= 0 and \
                        self.basePoint[0] + startX - endX + self.basePoint[2] <= self.zoomImage.shape[1]:
                    temporaryBasePoint[0] = self.basePoint[0] + startX - endX
                if self.basePoint[1] + startY - endY >= 0 and \
                        self.basePoint[1] + startY - endY + self.basePoint[3] <= self.zoomImage.shape[0]:
                    temporaryBasePoint[1] = self.basePoint[1] + startY - endY

                # print("startX {}, startY {}, endX {}, endY {}".format(startX, startY, endX, endY))
                # print("basePoint {}".format(self.basePoint))
                self.currentImage = self.zoomImage[temporaryBasePoint[1]: temporaryBasePoint[1] + temporaryBasePoint[3],
                                                    temporaryBasePoint[0]: temporaryBasePoint[0] + temporaryBasePoint[2]]
                self.showImage(self.currentImage)
            # self.showImage(processImage, original=False)

        if event.type == EventType.ButtonRelease and buttonID == 2:
            isMiddleMouseMove = False
            endX = realPosX
            endY = realPosY

            if self.zoomImage is not None:
                self.basePoint = [temporaryBasePoint[0],
                                  temporaryBasePoint[1],
                                  temporaryBasePoint[2],
                                  temporaryBasePoint[3]]
                # print("startX {}, startY {}, endX {}, endY {}".format(startX, startY, endX, endY))
                # print("basePoint {}".format(self.basePoint))
                self.currentImage = self.zoomImage[self.basePoint[1]: self.basePoint[1] + self.basePoint[3],
                                                    self.basePoint[0]: self.basePoint[0] + self.basePoint[2]]
                self.showImage(self.currentImage)

        if self.drawFlag:
            _image = self.currentImage.copy()
            if len(self.currentImage) == 3:
                try:
                    _image = cv.cvtColor(self.currentImage, cv.COLOR_RGB2BGR)
                except:
                    pass
            else:
                try:
                    _image = cv.cvtColor(self.currentImage, cv.COLOR_GRAY2BGR)
                except:
                    pass
            try:
                # if self.originalImage.shape < 3:
                #     cv.cvtColor(self.originalImage, cv.COLOR_GRAY2BGR)
                cv.circle(_image, (realPosX, realPosY), 3, (0, 0, 255), -1)
                self.showImage(_image, False)
            except:
                pass

        textShow = ""
        if event.type == EventType.Motion:
            justMove = True
            textShow = "(x, y, w, h) = ({}, {}, {}, {})   |    current color = {}".format(min(startX, endX), min(startY, endY), int(math.fabs(endX - startX)), int(math.fabs(endY - startY)), color)
            print(textShow)
        # elif event.type == EventType.Motion and buttonID == 0:
        #     if realChanel > 1:
        #         textShow = "(x, y) = ({}, {})   |    Color = ({}, {}, {})".format(realPosX, realPosY, color[0], color[1], color[2])
        #     else:
        #         textShow = "(x, y) = ({}, {})   |    Color = ({})".format(realPosX, realPosY, color)

        elif event.type == EventType.ButtonRelease and buttonID == 1 and justMove:
            image = self.currentImage[min(startY, endY):max(startY, endY), min(startX, endX): max(startX, endX)]
            self.calculateAverageColorThread(image)
            # thread = threading.Thread(target=self.calculateAverageColorThread, args=[image])
            # thread.start()
            justMove = False
        if textShow != "":
            self.showBottomLeftText(textShow)


    def calculateAverageColorThread(self, image):
        averageColor = cv.mean(image)
        averageColor = (int(averageColor[0]), int(averageColor[1]), int(averageColor[2]))
        textShow = "(x, y, w, h) = ({}, {}, {}, {})   |    Average color = {}".format(min(startX, endX),
                                                                                      min(startY, endY),
                                                                                      int(math.fabs(endX - startX)),
                                                                                      int(math.fabs(endY - startY)),
                                                                                      averageColor)

        self.showBottomLeftText(textShow)

    def exit(self):
        if self.workingThread.runningFlag:
            if not self.runningTab.clickBtnStart():
                return
        self.workingThread.disconnectEverything()
        if self.startingWindow is None:
            self.mainFrame.quit()
        else:
            self.hide()
            self.startingWindow.show()

        if self.startingWindow.machineName == MachineList.RUConnectorScrewMachine:
            self.ru_connectorImageFrame.hide()
        if self.startingWindow.machineName == MachineList.counting_in_conveyor:
            try:
                self.runningTab.resultTab.counting_in_conveyor_result_frame.clock.stop()
            except:
                pass

    def disableTab(self, tabId):
        self.tabBar.tab(tab_id=tabId, state='disable')

    def enableTab(self, tabId):
        self.tabBar.tab(tab_id=tabId, state='normal')

    def showBottomRightText(self, text):
        return

    def showBottomLeftText(self, text):
        self.bottomLeftLabel['text'] = "{}".format(text)

    def showBottomMiddleText(self, text):
        self.bottomMiddleLabel.config(text="{}".format(text), fg='black', font=VisionFont.regularFont(10))

    def showError(self, text):
        self.bottomMiddleLabel.config(text="{}".format(text), fg='red', font=VisionFont.boldFont(12))

    def hide(self):
        self.mainFrame.withdraw()

    def show(self):
        self.mainFrame.update()
        self.mainFrame.deiconify()
        self.mainFrame.state("zoomed")
        self.mainFrame.title("{} - {}".format(self.languageManager.localized("version"), self.startingWindow.machineName.value))
        if self.startingWindow.machineName == MachineList.RUConnectorScrewMachine:
            self.ru_ConnectorUpdateModel()

        self.modelSettingTab.updateView()
        self.runningTab.resultTab.updateView()
        self.researchingTab.updateAlgorithmForChangeModel()
        self.runningTab.resultTab.commonSettingFrame.updateInfo()
        self.runningTab.update_view() # gọi hàm syc_update_view khởi tạo giao diện
        # self.rearCheckMissingFrame.updateValue(self.currentModelParameter)
        # self.screwParameterFrame1.changeModel(self.currentModelParameter)
        machineName = self.startingWindow.machineName
        if machineName.isRUConnectorScrewMachine() or machineName.isFilterCoverScrewMachine():
            self.workingThread.adjustingScrewPos.getDesignPositions()
        if machineName.is_counting_in_conveyor():
            self.runningTab.resultTab.counting_in_conveyor_result_frame.clock.start()

    def createCheckMissingWindow(self):
        self.checkMissingWindow = MissingMachineResultWindow(self)
        self.checkMissingWindow.hide()

    def autoStartWorking(self):
        TimeControl.sleep(100)
        self.runningTab.clickBtnStart()

if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.autoStartWorking()
    mainWindow.mainFrame.mainloop()
