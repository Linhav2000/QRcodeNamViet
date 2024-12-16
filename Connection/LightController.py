from Connection.SerialManager import SerialCommunication
import CommonAssit.TimeControl as TimeControl
from View.Light.BrightnessSettingWindow import BrightnessSettingWindow
from CommonAssit.FileManager import JsonFile
import CommonAssit.CommonAssit as CommonAssit
from Connection.ConnectionStatus import ConnectionStatus
from View.Light.LightSettingWindow import LightSettingWindow
from View.Light.LightSettingWindow import LightBrand
from View.Light.LightSettingWindow import LightChanel
from Connection import VST_Light_Support
import tkinter.messagebox as messagebox
import threading
import jsonpickle

class LightController(SerialCommunication):

    communicationFrameOn = "S{}T000FC#"

    lLight_1channel_cmdLightUp = "01000128{}04"

    lLight_severalChannel_cmdLightUp = "0100032100{}{}04"       # channel number - value

    csrLight_cmdLightUp = "S{}T{}TC#"

    hard_test_flag = False

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.lightControllerInfo = LightControllerInfo(self.mainWindow)
        SerialCommunication.__init__(self, mainWindow, "LightController")

    def turnOn(self):
        lightParm = self.lightControllerInfo.lightControllerParm
        if lightParm.brand == LightBrand.L_light.value:
            if lightParm.channelAmount == LightChanel._1Chanel.value:
                self.turnOnLLight_1Channel()
            else:
                self.turnOnLLight_SeveralChannels()
        elif lightParm.brand == LightBrand.csr_light.value:
            self.turnOnSCRLight()
        elif lightParm.brand == LightBrand.vst_light.value:
            self.turnOnVSTLight()

    def turnOnVSTLight(self):
        channelAmount = int(self.lightControllerInfo.lightControllerParm.channelAmount[0])
        for channel in range(channelAmount):
            self.lightUpVSTLight_ServeralChannels(channel + 1,
                                               self.lightControllerInfo.lightControllerParm.lightValue[channel])

    def turnOnSCRLight(self):
        self.lightUpSCRLight(int(self.lightControllerInfo.lightControllerParm.lightValue[0]), int(self.lightControllerInfo.lightControllerParm.lightValue[1]))

    def turnOnLLight_1Channel(self):
        self.lightUpLLight_1Channel(int(self.lightControllerInfo.lightControllerParm.lightValue[0]))

    def turnOnLLight_SeveralChannels(self):
        channelAmount = int(self.lightControllerInfo.lightControllerParm.channelAmount[0])
        for channel in range(channelAmount):
            self.lightUpLLight_SeveralChannels(channel + 1, self.lightControllerInfo.lightControllerParm.lightValue[channel])

    def turnOff(self):
        lightParm = self.lightControllerInfo.lightControllerParm
        if lightParm.brand == LightBrand.L_light.value:
            if lightParm.channelAmount == LightChanel._1Chanel.value:
                self.turnOffLLight_1Channel()
            else:
                self.turnOffLLight_SeveralChannels()
        elif lightParm.brand == LightBrand.csr_light.value:
            self.turnOffSCRLight()
        elif lightParm.brand == LightBrand.vst_light.value:
            self.turn_off_vst_light()

    def turn_off_vst_light(self):
        cmd_turn_off = VST_Light_Support.turn_off_cmd(1)
        self.sendAsciiData(cmd_turn_off)
        TimeControl.sleep(1)
        self.read_feedback_with_time(50)

    def turnOffSCRLight(self):
        self.lightUpSCRLight(0, 0)

    def turnOffLLight_1Channel(self):
        self.lightUpLLight_1Channel(0)

    def turnOffLLight_SeveralChannels(self):
        channelAmount = int(self.lightControllerInfo.lightControllerParm.channelAmount[0])
        for channel in range(channelAmount):
            self.lightUpLLight_SeveralChannels(channel + 1, 0)

    def lightUp(self, channel, buttonList):
        lightParm = self.lightControllerInfo.lightControllerParm
        if lightParm.brand == LightBrand.L_light.value:
            if lightParm.channelAmount == LightChanel._1Chanel.value:
                value = 0
                try:
                    value = buttonList[0].lightValue
                except:
                    pass
                self.lightUpLLight_1Channel(value)
            else:
                for index in range(channel):
                    self.lightUpLLight_SeveralChannels(index + 1, buttonList[index].lightValue)
        elif lightParm.brand == LightBrand.csr_light.value:
            value1 = 0
            value2 = 0
            try:
                value1 = buttonList[0].lightValue
                value2 = buttonList[1].lightValue
            except:
                pass
            self.lightUpSCRLight(value1, value2)
        elif lightParm.brand == LightBrand.vst_light.value:
            self.lightUpVSTLight_ServeralChannels(channel, buttonList[channel-1].lightValue)

    def lightUpSCRLight(self, value1, value2):
        channel1Value = CommonAssit.change2Format3Number(value1)
        channel2Value = CommonAssit.change2Format3Number(value2)
        self.sendAsciiData(self.csrLight_cmdLightUp.format(channel1Value, channel2Value))
        TimeControl.sleep(50)
        rev = self.readAsciiData()
        if rev != "!":
            messagebox.showerror("Light up", "Cannot not turn on the light")
        self.mainWindow.runningTab.insertLog("light controller rev: {}".format(rev))

    def lightUpLLight_1Channel(self, value):
        valueSend = CommonAssit.decimal2Hex(int(value))
        onData = self.lLight_1channel_cmdLightUp.format(valueSend)
        self.sendHexData(onData)
        TimeControl.sleep(2)
        rev = self.readHexData()
        self.mainWindow.runningTab.insertLog("light controller rev: {}".format(rev))

    def lightUpLLight_SeveralChannels(self, channel,  value):
        channelSend = CommonAssit.decimal2Hex(int(channel))
        valueSend = CommonAssit.decimal2Hex(int(value))
        onData = self.lLight_severalChannel_cmdLightUp.format(channelSend,valueSend)
        self.sendHexData(onData)
        TimeControl.sleep(2)
        rev = self.readHexData()
        self.mainWindow.runningTab.insertLog("light controller rev: {}".format(rev))

    def lightUpVSTLight_ServeralChannels(self, channel, value):
        cmd_changeValue = VST_Light_Support.change_value_cmd(value=value, channel=channel)
        cmd_turn_on = VST_Light_Support.turn_on_cmd(channel=channel)
        self.sendAsciiData(cmd_changeValue)
        self.read_feedback_with_time(50)
        self.sendAsciiData(cmd_turn_on)
        self.read_feedback_with_time(50)

    def read_feedback_with_time(self, time_out=50):
        time = TimeControl.time()
        while TimeControl.time() - time < time_out:
            rev = self.readAsciiData()
            if rev != "":
                self.mainWindow.runningTab.insertLog("light controller rev: {}".format(rev))
                break
            TimeControl.sleep(1)

    def read_feed_back(self):
        read_feed_back_thread = threading.Thread(target=self.read_feed_back_thread, args=())
        read_feed_back_thread.start()

    def read_feed_back_thread(self):
        time = TimeControl.time()
        while TimeControl.time() - time < 100:
            rev = self.readAsciiData()
            if rev != "":
                self.mainWindow.runningTab.insertLog("light controller rev: {}".format(rev))
                break
            TimeControl.sleep(1)

    def stop_hard_test(self):
        self.hard_test_flag = False

    def start_hard_test(self):
        if self.hard_test_flag:
            self.mainWindow.runningTab.insertLog("Warning! The hard test thread already start")
            return
        if not self.isOpened:
            self.mainWindow.runningTab.insertLog("Warning! The light still not connected!")
            return
        self.hard_test_flag = True
        hard_test_thread = threading.Thread(target=self.hard_test_thread, args=())
        hard_test_thread.start()

    def hard_test_thread(self):
        while self.hard_test_flag:
            try:
                self.turnOn()
                TimeControl.sleep(1000)
                self.turnOff()
                TimeControl.sleep(1000)
            except Exception as error:
                self.mainWindow.runningTab.insertLog(f"ERROR hard test light. Detail: {error}")


    def test(self):
        lightTestWindow = BrightnessSettingWindow(self.mainWindow, self.lightControllerInfo)

    def connect(self):
        if self.open():
            self.mainWindow.runningTab.setLightStatus(ConnectionStatus.connected)

    def disconnectLight(self):
        self.disconnect()
        self.mainWindow.runningTab.setLightStatus(ConnectionStatus.disconnected)

    def setting(self):
        lightSettingWindow = LightSettingWindow(self.mainWindow, self.serialInfo, self.lightControllerInfo)

    def refresh(self):
        for i in range(30):
            self.sendHexData("0101002804")
            TimeControl.sleep(5)
            rev = self.readHexData()
            self.mainWindow.runningTab.insertLog("light controller rev: {}".format(rev))

class LightControllerInfo:
    filePath = "./config/lightSetting.json"

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.lightControllerParm = LightControllerParm()
        self.getInfo()

    def save(self):
        fileManager = JsonFile(filePath=self.filePath)
        jsonData = {}
        try:
            jsonData = jsonpickle.encode(self.lightControllerParm)
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Light Controller Settiing: {}".format(error))
            messagebox.showerror("Save Light Controller Settiing", "Cannot save this Light controller setting\n detail error {}".format(error))
        fileManager.data = jsonData
        fileManager.saveFile()

    def getInfo(self):
        file = JsonFile(self.filePath)
        jsonData = file.readFile()
        if jsonData != "":
            try:
                self.lightControllerParm = jsonpickle.decode(jsonData)
            except Exception as error:
                print("ERROR Get Light Controller setting: {}".format(error))
        self.lightControllerParm.makeStandardFile()

class LightControllerParm:
    lightValue = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
    brand = LightBrand.L_light.value
    channelAmount = LightChanel._1Chanel.value

    def makeStandardFile(self):
        valueList = []
        for value in self.lightValue:
            valueList.append(int(value))

        self.lightValue = valueList