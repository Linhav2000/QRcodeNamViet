import CommonAssit.CommonAssit as CommonAssit
from tkinter import messagebox
from View.Common.VisionUI import *


class BrightnessSettingWindow(VisionTopLevel):

    lightValueSlider: VisionSlider
    btnUp: VisionButton
    btnDown: VisionButton

    buttonList = []

    btnSave: SaveButton
    channels = 1

    def __init__(self, mainWindow, lightControllerInfo):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow
        self.lightControllerInfo = lightControllerInfo
        VisionTopLevel.__init__(self)
        self.bind("<Return>", self.push_enter)
        self.initVariables()
        self.windowSetting()
        self.createView()
        # self.showLastSetting()

    def push_enter(self, event):
        self.save()

    def initVariables(self):
        self.channels = int(self.lightControllerInfo.lightControllerParm.channelAmount[0])

    def windowSetting(self):
        eachHeight = 50
        width = 436
        height = self.channels * eachHeight + 80
        self.title("Light Testing")
        self.iconbitmap(CommonAssit.resource_path('resource\\appIcon.ico'))
        self.geometry("{}x{}+{}+{}".format(width, height, int
            (self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width( ) /2 - width /2),
                                           int
                                               (self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height( ) /2 - height /2)))
        self.resizable(0, 0)
        self.grab_set()
        # self.protocol("WM_DELETE_WINDOW", self.close)

    def createView(self):
        # self.setupSlider()
        self.setupButton()


    def setBrightness(self, channel):
        self.mainWindow.workingThread.light.lightUp(channel, self.buttonList)

    def setupButton(self):
        yPos = 50
        self.buttonList = []
        for index in range(self.channels):
            button = LightButtonFrame(self, self.lightControllerInfo.lightControllerParm.lightValue[index], index)
            button.place(x=0, y=index*yPos, width=436, height=yPos)
            self.buttonList.append(button)

        self.btnSave = SaveButton(self, command=self.clickBtnSave)
        self.btnSave.place(relx = 0.3, y = self.channels * yPos + 20, width=120, height=35)

    def close(self):
        if self.dataIsChanged():
            ask = messagebox.askyesno("Save information", "Do you want to save brightness value")
            if ask:
                self.save()

        self.destroy()

    def dataIsChanged(self):
        ret = False
        for index in range(len(self.buttonList)):
            ret = ret or self.lightControllerInfo.lightControllerParm.lightValue[index] != self.buttonList[index].lightValue
        return ret

    def clickBtnSave(self):
        self.save()

    def save(self):
        for index in range(len(self.buttonList)):
            self.lightControllerInfo.lightControllerParm.lightValue[index] = self.buttonList[index].lightValue
        self.lightControllerInfo.save()
        self.destroy()

    def showLastSetting(self):
        self.lightValueSlider.set(self.mainWindow.workingThread.light.lightControllerInfo.lightControllerParm.lightValue)

class LightButtonFrame(VisionFrame):

    lightValueSlider: VisionSlider
    btnUp: VisionButton
    btnDown: VisionButton
    lightValue = 100

    def __init__(self, master, lastValue, index):
        VisionFrame.__init__(self, master=master)
        self.master: BrightnessSettingWindow = master
        self.lightValue = lastValue
        self.channel = index + 1
        self.setupView()

    def setupView(self):
        self.setupSlider()
        self.setupButton()
        self.showLastSetting()

    def setupSlider(self):
        self.lightValueSlider = VisionSlider(self, orient=HORIZONTAL, from_ = 0, to = 250)
        self.lightValueSlider.bind("<ButtonRelease-1>", self.whenSliderButtonUp)
        self.lightValueSlider.place(x=65, y=5, width = 300)

    def setupButton(self):
        self.btnDown = VisionButton(self, text="<<<", command=self.clickDown)
        self.btnDown.place(x=10, y=20)

        self.btnUp = VisionButton(self, text=">>>", command=self.clickUp)
        self.btnUp.place(x=390, y=20)

    def whenSliderChangeValue(self, val):
        self.lightValue = val
        self.master.setBrightness(self.channel)
        # valueSend = self.mainWindow.workingThread.connectionManager.numberOfPosFormSend(val)
        # self.mainWindow.workingThread.light.lightUp(valueSend)

    def whenSliderButtonUp(self, event):
        self.lightValue = int(self.lightValueSlider.get())
        self.master.setBrightness(self.channel)

    def clickDown(self):
        currentValue = self.lightValueSlider.get()
        if currentValue == 0:
            return
        self.lightValueSlider.set(currentValue - 1)
        self.master.setBrightness(self.channel)

    def clickUp(self):
        currentValue = self.lightValueSlider.get()
        if currentValue == 255:
            return
        self.lightValueSlider.set(currentValue + 1)
        self.master.setBrightness(self.channel)

    def showLastSetting(self):
        self.lightValueSlider.set(self.lightValue)