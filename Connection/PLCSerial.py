from Connection.SerialManager import SerialCommunication
from Connection.ConnectionStatus import ConnectionStatus
from View.Setting.SerialSettingView import SerialSettingView
class PLCSerial(SerialCommunication):

    def __init__(self, mainWindow):
        SerialCommunication.__init__(self, mainWindow, "PLCSerial")

    def connect(self):
        if self.open():
            self.mainWindow.runningTab.setPLCStatus(ConnectionStatus.connected)
            self.mainWindow.runningTab.insertLog("PLC is connected successfully!")
            return True
        else:
            return False

    def disconnectPLC(self):
        self.disconnect()
        self.mainWindow.runningTab.setPLCStatus(ConnectionStatus.disconnected)

    def setting(self):
        lightSettingWindow = SerialSettingView(self.mainWindow, self.serialInfo)