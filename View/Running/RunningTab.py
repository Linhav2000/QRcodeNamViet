from tkinter import messagebox
import CommonAssit.TimeControl as TimeControl
import os
from CommonAssit.FileManager import TextFile
from Modules.ModelSetting.ModelManager import ModelManager
import CommonAssit.CommonAssit as CommonAssit
from View.Running.RunningLogTab import RunningLogTab
from View.Running.RunningResultTab import RunningResultTab
from View.Common.VisionUI import *
from Connection.ConnectionStatus import ConnectionStatus
from View.Running.Running_Manual_Tab import Running_Manual_Tab
from View.Running.DDK.DDK_Process_Image import DDK_Process_Image
import threading

class RunningTab(VisionFrame):
    root: ttk.Notebook
    tabBar: ttk.Notebook
    btnStart: ImageButton

    ConnectionFrame: VisionLabelFrame
    modelRunningFrame: VisionLabelFrame
    currentModelLabel: VisionLabel
    cameraStatus: VisionLabel
    plcStatus: VisionLabel
    serverStatus: VisionLabel
    lightStatus: VisionLabel

    logFrame:VisionLabelFrame
    logView:Text
    status: VisionLabel
    holeNumber: VisionLabel
    tactTime: VisionLabel
    scale: VisionLabel


    cameraStatusLbl: VisionLabel
    plcStatusLbl: VisionLabel
    serverStatusLbl: VisionLabel
    lightStatusLbl: VisionLabel

    startBtnImage: PhotoImage
    stopBtnImage: PhotoImage
    connectedStatus: PhotoImage
    disconnectedStatus: PhotoImage
    reconnectingStatus: PhotoImage

    modelLabel: VisionLabel
    modelComboBox: ttk.Combobox
    logTab: RunningLogTab
    resultTab: RunningResultTab
    running_manual: Running_Manual_Tab
    ddk_process_image_frame: DDK_Process_Image
    # currentModelPos = 0
    modelNameList = []

    isSelected = False
    btn_start_status = False # biến khai báo trạng thái nút start

    def __init__(self, root: ttk.Notebook, mainWindow):
        from MainWindow import MainWindow
        VisionFrame.__init__(self, root)
        self.root = root
        self.mainWindow: MainWindow = mainWindow
        self.modelManager = ModelManager()
        self.setupView()
        self.pack(fill='both', expand=1)

    def setupView(self):
        self.setStartButton()
        self.setupConnectionStatusView()
        self.setupCurrentModelFrame()
        self.setupResultView()
        self.setupTabBar()
        self.setupModelChosenView()
        self.notifyRegister()
        self.setExecutetButton()

    def notifyRegister(self):
        self.mainWindow.notificationCenter.add_observer(with_block=self.changeLanguage, for_name="ChangeLanguage")

    def changeLanguage(self, sender, notification_name, info):
        self.plcStatusLbl.config(text=self.mainWindow.languageManager.localized("plcStatusLbl"))
        self.cameraStatusLbl.config(text=self.mainWindow.languageManager.localized("cameraStatusLbl"))
        self.serverStatusLbl.config(text=self.mainWindow.languageManager.localized("serverStatusLbl"))
        self.lightStatusLbl.config(text=self.mainWindow.languageManager.localized("lightStatusLbl"))
        self.modelRunningFrame.config(text=self.mainWindow.languageManager.localized("runningModel"))
        self.modelLabel.config(text=self.mainWindow.languageManager.localized("selectModel"))
        self.tabBar.tab(tab_id=0, text= self.mainWindow.languageManager.localized("resultTab"))
        self.tabBar.tab(tab_id=1, text= self.mainWindow.languageManager.localized("log"))
        self.tabBar.tab(tab_id=2, text= self.mainWindow.languageManager.localized("manualTab"))
        self.tabBar.tab(tab_id=3, text= self.mainWindow.languageManager.localized("processedImage"))

    def setupModelChosenView(self):
        for model in self.modelManager.models:
            self.modelNameList.append(model.name)

        self.modelLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("selectModel"))
        self.modelLabel.place(x=0, y=210)

        self.modelComboBox = ttk.Combobox(self, value=self.modelNameList, state='readonly', cursor="hand2")
        self.modelComboBox.bind("<<ComboboxSelected>>", self.modelSelected)
        self.modelComboBox.place(x=120, y=210,width = 153)
        try:
            self.modelComboBox.current(self.modelManager.currentModelPos)
            self.currentModelLabel.set(self.modelComboBox.get())

        except:
            # self.modelComboBox.current(0)
            pass

    def modelSelected(self, even):
        if self.mainWindow.workingThread.runningFlag:
            messagebox.showwarning("Change Model",
                                   "You cannot change model when program is in running process\nStop program before changing model!")
            self.modelComboBox.current(self.modelManager.currentModelPos)
            return
        ask = messagebox.askyesno("Change Model", "Are you sure want to change model?")
        if ask:
            self.modelManager.currentModelPos = self.modelComboBox.current()
            self.modelManager.save()
        else:
            self.modelComboBox.current(self.modelManager.currentModelPos)
            return
        self.mainWindow.modelSettingTab.refreshModel()
        self.currentModelLabel.set(self.modelComboBox.get())
        machineName = self.mainWindow.startingWindow.machineName
        if machineName.isFilterCoverScrewMachine() or machineName.isRUConnectorScrewMachine():
            self.mainWindow.workingThread.drawCurrentModelDesign()

    def refreshModel(self):
        self.modelManager.refresh()
        self.modelNameList.clear()
        for model in self.modelManager.models:
            self.modelNameList.append(model.name)
        self.modelComboBox.config(value=self.modelNameList)
        if len(self.modelNameList) > 0:
            self.modelComboBox.current(self.modelManager.currentModelPos)
        try:
            if self.mainWindow.startingWindow.machineName.isFilterCoverScrewMachine() \
                    or self.mainWindow.startingWindow.machineName.isRUConnectorScrewMachine():
                self.mainWindow.workingThread.adjustingScrewPos.getDesignPositions()
        except:
            pass
        self.mainWindow.researchingTab.updateAlgorithmForChangeModel()

    def setupCurrentModelFrame(self):
        self.modelRunningFrame = VisionLabelFrame(self, text=self.mainWindow.languageManager.localized("runningModel"))
        self.modelRunningFrame.place(x=1, y=140, width=245, height=60)
        self.currentModelLabel = VisionLabel(self.modelRunningFrame, text ="SAMSUNG A32 5G BLACK")
        self.currentModelLabel.place(x=1, y=2.5)

    def setupConnectionStatusView(self):
        self.ConnectionFrame = VisionLabelFrame(self, text="Connection")
        self.ConnectionFrame.place(x=1, y=10, width=245, height=125)

        self.cameraStatusLbl = VisionLabel(self.ConnectionFrame, text=self.mainWindow.languageManager.localized("cameraStatusLbl"))
        self.cameraStatusLbl.place(x=1, y=2)
        self.cameraStatus = VisionLabel(self.ConnectionFrame)
        self.cameraStatus.place(x=100, y=2)

        self.plcStatusLbl = VisionLabel(self.ConnectionFrame, text=self.mainWindow.languageManager.localized("plcStatusLbl"))
        self.plcStatusLbl.place(x=1, y=26)
        self.plcStatus = VisionLabel(self.ConnectionFrame)
        self.plcStatus.place(x=100, y=26)

        self.serverStatusLbl = VisionLabel(self.ConnectionFrame, text=self.mainWindow.languageManager.localized("serverStatusLbl"))
        self.serverStatusLbl.place(x=1, y=50)
        self.serverStatus = VisionLabel(self.ConnectionFrame)
        self.serverStatus.place(x=100, y=50)

        self.lightStatusLbl = VisionLabel(self.ConnectionFrame, text=self.mainWindow.languageManager.localized("lightStatusLbl"))
        self.lightStatusLbl.place(x=1, y=74)
        self.lightStatus = VisionLabel(self.ConnectionFrame)
        self.lightStatus.place(x=100, y=74)

        self.setPLCStatus(ConnectionStatus.disconnected)
        self.setServerStatus(ConnectionStatus.disconnected)
        self.setCameraStatus(ConnectionStatus.disconnected)
        self.setLightStatus(ConnectionStatus.disconnected)

    def update_view(self):
        machineName = self.mainWindow.startingWindow.machineName
        if machineName.is_syc_phone_check():
            self.serverStatus.place_forget()
            self.plcStatus.place_forget()
            self.lightStatus.place_forget()
            self.plcStatusLbl.place_forget()
            self.serverStatusLbl.place_forget()
            self.lightStatusLbl.place_forget()
            self.btnExcute.place(x=273, y=150, width=112, height=50)
        else:
            self.plcStatus.place(x=100, y=26)
            self.serverStatus.place(x=100, y=50)
            self.lightStatus.place(x=100, y=74)
            self.plcStatusLbl.place(x=1, y=26)
            self.serverStatusLbl.place(x=1, y=50)
            self.lightStatusLbl.place(x=1, y=74)
            self.btnExcute.place_forget()

        self.running_manual.updateView()

    def setupResultView(self):
        return

    def setCameraStatus(self, status = ConnectionStatus.disconnected):
        if status == ConnectionStatus.connected:
            self.cameraStatus.config(text="Connected", font=VisionFont.boldFont(11), fg=Color.winLame())
        elif status == ConnectionStatus.disconnected:
            self.cameraStatus.config(text="Disconnected", font=VisionFont.boldFont(11), fg=Color.winRed())
        elif status == ConnectionStatus.reconnecting:
            self.cameraStatus.config(text="Reconnecting", font=VisionFont.boldFont(11), fg=Color.winBlue())

    def setPLCStatus(self, status: ConnectionStatus = ConnectionStatus.connected):
        if status == ConnectionStatus.connected:
            self.plcStatus.config(text="Connected", font=VisionFont.boldFont(11), fg=Color.winLame())
        elif status == ConnectionStatus.disconnected:
            self.plcStatus.config(text="Disconnected", font=VisionFont.boldFont(11), fg=Color.winRed())
        elif status == ConnectionStatus.reconnecting:
            self.plcStatus.config(text="Reconnecting", font=VisionFont.boldFont(11), fg=Color.winBlue())
        elif status == ConnectionStatus.waiting:
            self.plcStatus.config(text="Waiting", font=VisionFont.boldFont(11), fg=Color.winBlue())

    def setServerStatus(self, status: ConnectionStatus = ConnectionStatus.connected):
        if status == ConnectionStatus.connected:
            self.serverStatus.config(text="Connected", font=VisionFont.boldFont(11), fg=Color.winLame())
        elif status == ConnectionStatus.disconnected:
            self.serverStatus.config(text="Disconnected", font=VisionFont.boldFont(11), fg=Color.winRed())
        elif status == ConnectionStatus.reconnecting:
            self.serverStatus.config(text="Reconnecting", font=VisionFont.boldFont(11), fg=Color.winBlue())

    def setLightStatus(self, status: ConnectionStatus = ConnectionStatus.connected):
        if status == ConnectionStatus.connected:
            self.lightStatus.config(text="Connected", font=VisionFont.boldFont(11), fg=Color.winLame())
        elif status == ConnectionStatus.disconnected:
            self.lightStatus.config(text="Disconnected", font=VisionFont.boldFont(11), fg=Color.winRed())
        elif status == ConnectionStatus.reconnecting:
            self.lightStatus.config(text="Reconnecting", font=VisionFont.boldFont(11), fg=Color.winBlue())

    def setupTabBar(self):
        self.tabBar = ttk.Notebook(self)
        self.tabBar.place(x=0,rely=0.4, relwidth=1, relheight=0.6)

        self.resultTab = RunningResultTab(self.tabBar, self.mainWindow)
        self.tabBar.add(self.resultTab, text=self.mainWindow.languageManager.localized("resultTab"))

        self.logTab = RunningLogTab(self.tabBar, self.mainWindow)
        self.tabBar.add(self.logTab, text=self.mainWindow.languageManager.localized("log"))

        self.running_manual = Running_Manual_Tab(self.tabBar, self.mainWindow)
        self.tabBar.add(self.running_manual, text=self.mainWindow.languageManager.localized("manualTab"))

        self.ddk_process_image_frame = DDK_Process_Image(self.tabBar, self.mainWindow)
        self.tabBar.add(self.ddk_process_image_frame, text=self.mainWindow.languageManager.localized("processedImage"))

    def setStartButton(self):
        self.startBtnImage = ImageTk.PhotoImage(file='./resource/start_button.png')
        self.stopBtnImage = PhotoImage(file=CommonAssit.resource_path('resource\\stop_button.png'))
        # self.btnStart = Button(self, image=self.startBtnImage, borderwidth=0, command=self.clickBtnStart)
        self.btnStart = ImageButton(self,imagePath="./resource/start_button.png",command=self.clickBtnStart)
        self.btnStart.place(x=273, y=45, width=112, height=69)

    def setExecutetButton(self):
        self.btnExcute = ImageButton(self,imagePath="./resource/execute_button.png",command=self.syc_clickBtnExecute)
        self.btnExcute.place(x=273, y=150, width=112, height=50)

    def syc_clickBtnExecute(self): # Hàm thực thi lệnh từ nút bấm Execute của SYC phone check
        # Check phần mềm có đang chạy auto hay k bằng cách check trạng thái của nút bấm Start
        if self.mainWindow.runningTab.btn_start_status is False: # Nếu trạng thái nút bấm là False (ctrình đang k auto)
            self.mainWindow.workingThread.create_syc_phone_check() # gọi hàm "create_syc_phone_check"
            self.mainWindow.workingThread.syc_execute_phone_check() # gọi hàm "syc_execute_phone_check"
        # Ngược lại thì báo lỗi
        else:
            messagebox.showwarning("SYC Error","Unable to execute \nPlease press Stop program first!")
            # messagebox và showwarning biến mặc định của Tkinter


    def clickBtnStart(self, showMessage=True):
        if not self.mainWindow.workingThread.runningFlag:
            if self.mainWindow.workingThread.startWorking():
                # self.btnStart.config(image=self.stopBtnImage)
                self.btnStart.setImagePath('./resource/stop_button.png')
                self.btn_start_status = True # gửi trạng thái True cho "btn_start_status" (ctrinh đang chạy auto )
                return True
            else:
                return False
        else:
            if showMessage:
                resultMsB = messagebox.askyesno('Stop', 'Are you surely want to Stop program?')
                if not resultMsB:
                    return False
            # self.btnStart.config(image=self.startBtnImage)
            self.btnStart.setImagePath('./resource/start_button.png')
            self.mainWindow.workingThread.stopWorking()
            self.btn_start_status = False# gửi trạng thái True cho "btn_start_status" (ctrinh đang dừng)
            return True

    def insertLog(self, log):
        thread = threading.Thread(target=self.insertLogThread, args=[log])
        thread.start()
        # logForm = "{} {}\n".format(TimeControl.logTime(), log)
        # self.logTab.logView.insert(END, logForm)
        # self.logTab.logView.see(END)
        # print(logForm)
        #
        # logFolder = "./Log"
        # connectionLogFolder = logFolder + "/Connection"
        # filePath = connectionLogFolder + "/" + TimeControl.y_m_dFormat() + ".txt"
        #
        # if not os.path.exists(logFolder):
        #     os.makedirs(logFolder)
        # if not os.path.exists(connectionLogFolder):
        #     os.makedirs(connectionLogFolder)
        #
        # logFile = TextFile(filePath)
        # logFile.appendData(logForm)

    def insertLogThread(self, log = ""):
        if log.startswith("ERROR"):
            self.mainWindow.showError(log)

        logForm = "{} {}\n".format(TimeControl.logTime(), log)

        if self.mainWindow.commonSettingManager.settingParm.printLogFlag:
            self.logTab.logView.insert(END, logForm)
            self.logTab.logView.see(END)
            print(logForm)

        if self.mainWindow.startingWindow.machineName is not None \
                and self.mainWindow.startingWindow.machineName.isRearMissingInspectionMachine() \
                and log.startswith("ERROR"):
            self.mainWindow.checkMissingWindow.middleFrame.insertLog(log)


        logFolder = "./Log"
        connectionLogFolder = logFolder + "/Connection"
        filePath = connectionLogFolder + "/" + TimeControl.y_m_dFormat() + ".txt"

        if not os.path.exists(logFolder):
            os.makedirs(logFolder)
        if not os.path.exists(connectionLogFolder):
            os.makedirs(connectionLogFolder)

        logFile = TextFile(filePath)
        logFile.appendData(logForm)

    def showCurrentResult(self):
        self.resultTab.currentResultFrame.showResult()

    def showLastResult(self):
        self.resultTab.lastResultFrame.result = self.resultTab.currentResultFrame.result
        self.resultTab.lastResultFrame.showResult()