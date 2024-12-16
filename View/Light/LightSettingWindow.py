import serial.tools.list_ports
import CommonAssit.CommonAssit as CommonAssit
import tkinter.messagebox as messagebox
from View.Setting.SerialParameterFrame import SerialSettingFrame
from View.Common.VisionUI import *


class LightBrand(enum.Enum):
    L_light= "L-Light"
    csr_light = "CSR-Light"
    vst_light = "VST-Light"

class LightChanel(enum.Enum):
    _1Chanel = "1 chanel"
    _2Channel = "2 channels"
    _3Channel = "3 channels"
    _4Channel = "4 channels"
    _6Channel = "6 channels"
    _8Channel = "8 channels"
    _16Channel = "16 channels"

class LightSettingWindow(VisionTopLevel):

    brandCombobox = ttk.Combobox
    channelAmountCombobox = ttk.Combobox
    brandList = []
    channelAmountList = []

    def __init__(self, mainWindow, serialInfo, lightControllerInfo):
        self.mainWindow = mainWindow
        self.serialInfo = serialInfo
        self.lightControllerInfo = lightControllerInfo
        VisionTopLevel.__init__(self)
        self.serialParameterFrame = SerialSettingFrame(self, mainWindow, serialInfo)
        self.settingWindow()
        self.setupView()

    def settingWindow(self):
        width = 623
        height = 523
        self.title(self.mainWindow.languageManager.localized("lightSettingTitle"))
        self.iconbitmap(CommonAssit.resource_path('resource\\appIcon.ico'))
        self.geometry("{}x{}+{}+{}".format(width, height, int(self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width()/2 - width/2),
                                             int(self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height()/2 - height/2)))
        self.resizable(0, 0)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.close)

    def setupView(self):
        self.serialParameterFrame.place(x=300, y=0, width=320, height=420)
        self.btnSave = SaveButton(self, command=self.save)
        self.btnSave.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)
        self.setupConnectionFrame()
        self.showLastSetting()

    def setupConnectionFrame(self):
        self.brandList = []
        self.channelAmountList = []
        for channelAmount in LightChanel:
            self.channelAmountList.append(channelAmount.value)
        for brand in LightBrand:
            self.brandList.append(brand.value)

        self.connectionSettingFrame = VisionLabelFrame(self, text="Connection Parameter")
        self.connectionSettingFrame.place(x=5, y=0, width=290, height=420)

        heightSpace = 25
        comboWidth = 250
        heightDisplacement = 80

        # brand
        brandLabel = VisionLabel(self.connectionSettingFrame, text=self.mainWindow.languageManager.localized("brand"))
        brandLabel.place(x=10, y=10)
        self.brandCombobox = ttk.Combobox(self.connectionSettingFrame, value=self.brandList, state='readonly', cursor="hand2")
        self.brandCombobox.place(x=10, y=35, width=comboWidth, height=heightSpace)

        # channel amount
        channelAmountLabel = VisionLabel(self.connectionSettingFrame, text=self.mainWindow.languageManager.localized("channelAmount"))
        channelAmountLabel.place(x=10, y=heightDisplacement)
        self.channelAmountCombobox = ttk.Combobox(self.connectionSettingFrame, value=self.channelAmountList, state='readonly', cursor="hand2")
        self.channelAmountCombobox.place(x=10, y=heightDisplacement + 25, width=comboWidth, height=heightSpace)


    def showLastSetting(self):
        self.channelAmountCombobox.current(self.channelAmountList.index(self.lightControllerInfo.lightControllerParm.channelAmount))
        self.brandCombobox.current(self.brandList.index(self.lightControllerInfo.lightControllerParm.brand))

    def save(self):
        try:
            self.serialInfo.portName = self.serialParameterFrame.comNames[self.serialParameterFrame.comComboBox.current()]
            self.serialInfo.baud = self.serialParameterFrame.baudRates[self.serialParameterFrame.baudComboBox.current()]
            self.serialInfo.dataSize = self.serialParameterFrame.dataSizemMap[self.serialParameterFrame.dataSizeComboBox.get()]
            self.serialInfo.parity = self.serialParameterFrame.partiesMap[self.serialParameterFrame.parityComboBox.get()]
            self.serialInfo.stopBit = self.serialParameterFrame.stopBitMap[self.serialParameterFrame.stopBitComboBox.get()]

            self.lightControllerInfo.lightControllerParm.brand = self.brandCombobox.get()
            self.lightControllerInfo.lightControllerParm.channelAmount = self.channelAmountCombobox.get()

            self.serialInfo.save()
            self.lightControllerInfo.save()
            self.destroy()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Serial Info : {}".format(error))
            messagebox.showerror("Save Serial Info", "{}".format(error))

    def close(self):
        try:
            if self.serialInfo.portName != self.serialParameterFrame.comNames[self.serialParameterFrame.comComboBox.current()] \
                or self.serialInfo.baud!= self.serialParameterFrame.baudRates[self.serialParameterFrame.baudComboBox.current()] \
                or self.serialInfo.dataSize != self.serialParameterFrame.dataSizemMap[self.serialParameterFrame.dataSizeComboBox.get()] \
                or self.serialInfo.parity != self.serialParameterFrame.partiesMap[self.serialParameterFrame.parityComboBox.get()] \
                or self.serialInfo.stopBit != self.serialParameterFrame.stopBitMap[self.serialParameterFrame.stopBitComboBox.get()]\
                or self.lightControllerInfo.lightControllerParm.channelAmount != self.channelAmountCombobox.get()\
                or self.lightControllerInfo.lightControllerParm.brand != self.brandCombobox.get():
                askSave = messagebox.askyesno("Serial Info Changes", "Would you like to save the data you have changed?")
                if askSave:
                    self.save()
                else:
                    self.destroy()
            else:
                self.destroy()
        except:
            self.destroy()
            pass

