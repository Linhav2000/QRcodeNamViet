from Connection.PLCSerial import PLCSerial
from Connection.PLCEthernetClient import PLCEthernetClient
from Connection.PLCEthernetServer import PLCEthernetServer
from Connection.ConnectionStatus import ConnectionStatus
from View.Setting.CommunicationSendTestWindow import CommunicationSendTestWindow
import tkinter.messagebox as messagebox
import enum
import threading
from CommonAssit import TimeControl

class ConnectionType(enum.Enum):
    serial = "Serial"
    ethernetClient = "Ethernet Client"
    ethernetServer = "Ethernet Server"

    def isSerial(self):
        return self.value is self.serial.value

    def isEthernetClient(self):
        return self.value is self.ethernetClient.value

    def isEthernetServer(self):
        return self.value is self.ethernetServer.value

class ConnectionManager:
    plcTimeOut = 20000

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        self.mainWindow: MainWindow = mainWindow
        self.plcEthernetClient = PLCEthernetClient(self.mainWindow)
        self.plcEthernetServer = PLCEthernetServer(self.mainWindow)

        self.plcSerial = PLCSerial(self.mainWindow)

    # def isConnected(self):
    #     if self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.serial.value:
    #         return self.plcSerial.isOpened
    #     elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetClient.value:
    #         return self.plcEthernetClient.isConnected()
    #     elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetServer.value:
    #         return self.plcEthernetServer.isOpened

    def isReady(self):
        if self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.serial.value:
            return self.plcSerial.isOpened
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetClient.value:
            return self.plcEthernetClient.ready
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetServer.value:
            return self.plcEthernetServer.isOpened

    def isConnected(self):
        if self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.serial.value:
            return self.plcSerial.isOpened
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetClient.value:
            return self.plcEthernetClient.ready
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetServer.value:
            return self.plcEthernetServer.isConnected

    def connect(self):
        if self.isReady():
            return True
        ret = False
        if self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.serial.value:
            ret = self.plcSerialConnect()
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetClient.value:
            ret = self.plcEthernetClientConnect()
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetServer.value:
            ret = self.plcEthernetServerOpen()

        if ret:
            self.mainWindow.runningTab.setPLCStatus(ConnectionStatus.connected)
            self.mainWindow.runningTab.insertLog("PLC is connected successfully!")
            self.startThread()
        else:
            self.mainWindow.runningTab.insertLog("Cannot connect PLC, check cable or Ethernet setting!")
            # messagebox.showerror("PLC Connection", "Cannot connect PLC, check cable or Ethernet setting!")

        return ret

    def reconnect(self):
        reconnect_thread = threading.Thread(target=self.reconnect_thread, args=())
        reconnect_thread.start()

    def reconnect_thread(self):
        while not self.isReady():
            self.connect()
            TimeControl.sleep(1)

    def disconnect(self):
        self.mainWindow.workingThread.plcReadingFlag = False
        if self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.serial.value:
            self.plcSerialDisconnect()
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetClient.value:
            self.plcEthernetClientDisconnect()
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetServer.value:
            self.plcEthernetServerClose()

    def disconnectAll(self):
        self.mainWindow.workingThread.plcReadingFlag = False
        self.plcSerialDisconnect()
        self.plcEthernetClientDisconnect()
        self.plcEthernetServerClose()
        self.mainWindow.runningTab.setPLCStatus(ConnectionStatus.disconnected)

    def re_open_server(self):
        re_open_server_thread = threading.Thread(target=self.re_open_server_thread, args=())
        re_open_server_thread.start()

    def re_open_server_thread(self):
        try:
            self.disconnect()
            TimeControl.sleep(200)
            self.connect()
        except Exception as error:
            self.mainWindow.runningTab.insertLog(f"ERROR Cannot reopen server port!! detail: {error}")

    def sendData(self, data):
        if self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.serial.value:
            self.plcSerial.sendAsciiData(data)
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetClient.value:
            self.plcEthernetClientSendData(data)
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetServer.value:
            self.plcEthernetServer.sendAsciiData(data)

    def readData(self):
        if self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.serial.value:
            return self.plcSerial.readAsciiData()
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetClient.value:
            return self.plcEthernetClientRead()
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetServer.value:
            return self.plcEthernetServer.readAsciiData()

    def sendTest(self):
        CommunicationSendTestWindow(self.mainWindow)
        # self.sendData("Test")

    def setting(self):
        if self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.serial.value:
            self.plcSerial.setting()
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetClient.value:
            self.plcEthernetClientSetting()
        elif self.mainWindow.commonSettingManager.settingParm.communicationType == ConnectionType.ethernetServer.value:
            self.plcEthernetServer.setting()

    def plcSerialSetting(self):
        self.plcSerial.setting()

    def plcEthernetClientSetting(self):
        self.plcEthernetClient.setting()

    def plcSerialConnect(self):
        if self.plcSerial.isOpened:
            return True
        return self.plcSerial.connect()

    def plcSerialDisconnect(self):
        self.plcSerial.disconnectPLC()
        self.mainWindow.runningTab.setPLCStatus(ConnectionStatus.disconnected)
        self.mainWindow.runningTab.insertLog("PLC is disconnected!")

    def plcEthernetClientConnect(self):
        if self.plcEthernetClient.ready:
            return True
        return self.plcEthernetClient.connect()


    def plcEthernetServerOpen(self):
        return self.plcEthernetServer.open()

    def plcEthernetServerClose(self):
        self.plcEthernetServer.close()
        self.mainWindow.runningTab.setPLCStatus(ConnectionStatus.disconnected)
        self.mainWindow.runningTab.insertLog("PLC is disconnected!")

    def startThread(self):
        machineName = self.mainWindow.startingWindow.machineName
        thread = None
        if machineName.isRUConnectorScrewMachine():
            thread = threading.Thread(target=self.mainWindow.workingThread.ru_connectorScrewMachineThread, args=())
            # _thread.start_new_thread(self.mainWindow.workingThread.ru_connectorScrewMachineThread, ())
        elif machineName.isFilterCoverScrewMachine():
            thread = threading.Thread(target=self.mainWindow.workingThread.coverFilterScrewMachineThread, args=())
            # _thread.start_new_thread(self.mainWindow.workingThread.coverFilterScrewMachineThread, ())
        elif machineName.isRearMissingInspectionMachine():
            thread = threading.Thread(target=self.mainWindow.workingThread.rearCheckMissingThread, args=())
        elif machineName.isFUAssemblyMachine() or machineName.isLoadFrameMachine():
            thread = threading.Thread(target=self.mainWindow.workingThread.fu_assy_Thread, args=())
            # _thread.start_new_thread(self.mainWindow.workingThread.fu_assy_Thread, ())
        elif machineName.isLocationDetect():
            thread = threading.Thread(target=self.mainWindow.workingThread.locationDemoThread, args=())
        elif machineName.is_roto_weighing_robot():
            thread = threading.Thread(target=self.mainWindow.workingThread.rotoWeighingThread, args=())
        elif machineName.is_washing_machine_inspection():
            thread = threading.Thread(target=self.mainWindow.workingThread.washing_machine_inspection_thread, args=())
        elif machineName.is_ddk_inspection():
            thread = threading.Thread(target=self.mainWindow.workingThread.ddk_inspection_thread, args=())
        if thread is not None:
            thread.start()

    def plcEthernetClientDisconnect(self):
        self.plcEthernetClient.disconnect()
        self.mainWindow.runningTab.setPLCStatus(ConnectionStatus.disconnected)
        self.mainWindow.runningTab.insertLog("PLC is disconnected!")

    def plcEthernetClientSendTest(self):
        self.plcEthernetClient.sendData("Test")

    def plcEthernetClientRead(self):
        return self.plcEthernetClient.readData()

    def plcEthernetClientSendData(self, data):
        self.plcEthernetClient.sendData("{}".format(data))
        # ret, rev = self.plcEthernet.readData()
        self.mainWindow.runningTab.insertLog("Communication send: {}".format(data))


    def modelNameFormSend(self, modelName):
        valueSend = ""
        if len(modelName) <= 6:
            modelSendLength = 6
            realModeLength = len(modelName)
            for i in range(modelSendLength - realModeLength):
                valueSend += '0'
            valueSend = "{}{}".format(valueSend, modelName)
        else:
            valueSend = modelName[0:6]
        return valueSend

    def numberOfPosFormSend(self, numberOfPos):
        valueSend = ""
        try:
            numOfPosLengthSend = 6
            realNumOfPosLength = len(str(int(numberOfPos)))
            for i in range(numOfPosLengthSend - realNumOfPosLength):
                valueSend += '0'
            valueSend = "{}{}".format(valueSend, numberOfPos)
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Number of Position Form Send: {}".format(error))
            messagebox.showerror("Number of Position Form Send", "{}".format(error))
        return valueSend

    def getPointFormatSend(self, point, coordinateLength = 6):
        lengthX = len(str(int(point[0])))
        valueSendX = ""
        if lengthX < coordinateLength:
            for i in range(coordinateLength - lengthX):
                valueSendX += '0'
            valueSendX = "{}{}".format(valueSendX, point[0])
        else:
            valueSendX = "{}".format(str(point[0])[0:coordinateLength])

        lengthY = len(str(int(point[1])))
        valueSendY = ""
        if lengthY < coordinateLength:
            for i in range(coordinateLength - lengthY):
                valueSendY += '0'
            valueSendY = "{}{}".format(valueSendY, point[1])
        else:
            valueSendY = "{}".format(str(point[1])[0:coordinateLength])

        valueSendZ = ""
        if len(point) == 3:
            lengthZ = len(str(int(point[2])))
            if lengthZ < coordinateLength:
                for i in range(coordinateLength - lengthZ):
                    valueSendZ += '0'
                valueSendZ = "{}{}".format(valueSendZ, point[2])
            else:
                valueSendZ = "{}".format(str(point[2])[0:coordinateLength])
        else:
            lengthZ = 0
            for i in range(coordinateLength - lengthZ):
                valueSendZ += '0'
        # return valueSendX, valueSendY, valueSendZ
        return valueSendY, valueSendX, valueSendZ

    def getLocationDetectFormatSend(self, point, coordinateLength = 5):
        lengthX = len(str(int(point[0])))
        valueSendX = ""
        if lengthX < coordinateLength:
            for i in range(coordinateLength - lengthX):
                valueSendX += '0'
            valueSendX = "{}{}".format(valueSendX, point[0])
        else:
            valueSendX = "{}".format(str(point[0])[0:coordinateLength])

        lengthY = len(str(int(point[1])))
        valueSendY = ""
        if lengthY < coordinateLength:
            for i in range(coordinateLength - lengthY):
                valueSendY += '0'
            valueSendY = "{}{}".format(valueSendY, point[1])
        else:
            valueSendY = "{}".format(str(point[1])[0:coordinateLength])

        return valueSendY, valueSendX

    def getPointFU_AssyFormatSend(self, point, coordinateLength = 5):
        lengthX = len(str(int(point[0])))
        valueSendX = ""
        if lengthX < coordinateLength:
            for i in range(coordinateLength - lengthX):
                valueSendX += '0'
            valueSendX = "{}{}".format(valueSendX, point[0])
        else:
            valueSendX = "{}".format(str(point[0])[0:coordinateLength])

        lengthY = len(str(int(point[1])))
        valueSendY = ""
        if lengthY < coordinateLength:
            for i in range(coordinateLength - lengthY):
                valueSendY += '0'
            valueSendY = "{}{}".format(valueSendY, point[1])
        else:
            valueSendY = "{}".format(str(point[1])[0:coordinateLength])

        valueSendZ = ""
        if len(point) >= 3:
            lengthZ = len(str(int(point[2])))
            if lengthZ < coordinateLength:
                for i in range(coordinateLength - lengthZ):
                    valueSendZ += '0'
                valueSendZ = "{}{}".format(valueSendZ, point[2])
            else:
                valueSendZ = "{}".format(str(point[2])[0:coordinateLength])
        else:
            lengthZ = 0
            for i in range(coordinateLength - lengthZ):
                valueSendZ += '0'

        valueSendU = ""
        if len(point) == 4:
            lengthU = len(str(int(point[3])))
            if lengthU < coordinateLength:
                for i in range(coordinateLength - lengthU):
                    valueSendU += '0'
                valueSendU = "{}{}".format(valueSendU, point[3])
            else:
                valueSendU = "{}".format(str(point[3])[0:coordinateLength])
        else:
            lengthU = 0
            for i in range(coordinateLength - lengthU):
                valueSendU += '0'
        return valueSendY, valueSendX, valueSendZ, valueSendU

