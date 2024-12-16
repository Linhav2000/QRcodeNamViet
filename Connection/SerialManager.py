import serial
import serial.tools.list_ports
from os import linesep
from Connection.Serial_Communication_Wrapper import Wrapper_Serial
import tkinter.messagebox as messagebox
from CommonAssit.FileManager import CsvFile
from View.Setting.SerialSettingView import SerialSettingView

class SerialCommunication:
    serial_port: serial
    # serial_wrapper: Wrapper_Serial = None
    running = True
    gettingData = False
    isOpened = False
    use_wrapper = False

    def __init__(self, mainWin, nameController, use_wrapper=False):
        from MainWindow import MainWindow
        self.serial_port = serial.Serial()
        self.use_wrapper = use_wrapper
        self.nameController = nameController
        self.serialInfo = SerialInfo(nameController)
        self.mainWindow: MainWindow = mainWin

    def isConnected(self):
        try:
            return self.serial_port.isOpen()
        except:
            return True

    def open(self):
        if self.isOpened:
            return True
        try:
            # if self.use_wrapper:
            #     self.serial_port = Wrapper_Serial(
            #         port=int(self.serialInfo.portName[-1]),
            #         baudrate=self.serialInfo.baud,
            #         bytesize=self.serialInfo.dataSize,
            #         stop_bit=self.serialInfo.stopBit,
            #         )
            #     self.isOpened = self.serial_port.isOpen()
            # else:
            #     self.serial_port = serial.Serial(
            #         port=self.serialInfo.portName,
            #         baudrate=self.serialInfo.baud,
            #         parity=self.serialInfo.parity,
            #         stopbits=self.serialInfo.stopBit,
            #         bytesize=self.serialInfo.dataSize
            #     )
            self.serial_port.baudrate = self.serialInfo.baud
            self.serial_port.parity = self.serialInfo.parity
            self.serial_port.stopbits = self.serialInfo.stopBit
            self.serial_port.bytesize = self.serialInfo.dataSize
            device = self.get_device_name(self.serialInfo.portName)
            self.serial_port.port = device
            self.serial_port.rts = False
            self.serial_port.open()
            self.isOpened = True
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Open Serial Port: {}".format(error))
            return False
        if not self.isOpened:
            self.mainWindow.runningTab.insertLog("Cannot Open Port!")
        else:
            self.mainWindow.runningTab.insertLog("Open Serial Port successfully!")
        return self.isOpened

    def get_device_name(self, serial_number):
        """
        Get full device name/path from serial number
        Parameters
        ----------
        serial_number: string
            The usb-serial's serial number
        Returns
        -------
        string
            Full device name/path, e.g. /dev/ttyUSBx (on *.nix system or COMx on Windows)
        Raises
        ------
        IOError
            When not found device with this serial number
        """
        serial_numbers = []
        activePorts = serial.tools.list_ports.comports()
        for pinfo in activePorts:
            if str(pinfo.name).strip() == str(serial_number).strip():
                return pinfo.device
            # save list of serial numbers for user reference
            serial_numbers.append(pinfo.name.encode('utf-8'))
        raise IOError(
            'Could not find device with provided serial number {}Found devices with following serial numbers: {}{}'.format(
                linesep, linesep, serial_numbers))

    def disconnect(self):
        if not self.isOpened:
            return
        self.isOpened = False
        try:
            self.serial_port.close()
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Disconnect Serial Port: {}".format(error))
            messagebox.showerror("Disconnect Serial Port", "{}".format(error))

    def setting(self):
        serialSettingView = SerialSettingView(self.mainWindow, self.serialInfo, "Serial Communication Setting")

    def sendHexData(self, data):
        if not self.isOpened:
            self.mainWindow.runningTab.insertLog("Serial Send Data: The port is not open!")
            return self.isOpened
        dataSend = str(data)
        try:
            if self.serial_port.isOpen():
                dataSend = bytearray.fromhex(dataSend)
                # self.serial_port.write(dataSend.encode("utf-8"))
                self.serial_port.write(dataSend)
                self.mainWindow.runningTab.insertLog("Serial Data Send: {}".format(data))
            else:
                self.mainWindow.runningTab.insertLog("Cannot connect to the serial port")
                return False
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Serial Send Data: {}".format(error))
            return False

    def sendAsciiData(self, data):
        if not self.isOpened:
            self.mainWindow.runningTab.insertLog("Serial Send Data: The port is not open!")
            return self.isOpened
        dataSend = str(data)
        try:
            if self.serial_port.isOpen():
                self.serial_port.write(dataSend.encode("utf-8")) if not self.use_wrapper else self.serial_port.write(dataSend)
                self.mainWindow.runningTab.insertLog("Serial Data Send: {}".format(data))
            else:
                self.mainWindow.runningTab.insertLog("Cannot connect to the serial port")
                return False
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Serial Send Data - ERROR; {}".format(error))
            return  False
        return True

    def send_command(self, cmd_string):
        cmd_bytes = bytearray.fromhex(cmd_string)
        for cmd_byte in cmd_bytes:
            hex_byte = ("{0:02x}".format(cmd_byte))
            # print (hex_byte)
            self.serial_port.write(bytearray.fromhex(hex_byte))

    def readAsciiData(self):
        output = ""
        if not self.isOpened:
            return output
        try:
            res = self.serial_port.read_all()
            output += res.decode('utf-8') if not self.use_wrapper else res
        except:
            pass

        return output

    def readHexData(self):
        output = ""
        if not self.isOpened:
            return output
        try:
            res = self.serial_port.read_all()
            output += res.hex()
        except Exception as eror:
            pass

        return output

class SerialInfo:
    NAME_IDX = 0
    BAUD_IDX = 1
    DATA_SIZE_IDX = 2
    PAIRTY_IDX = 3
    STOP_BIT_IDX = 4

    portName = "COM1"
    baud = 115200
    dataSize = serial.EIGHTBITS
    parity = serial.PARITY_EVEN
    stopBit = serial.STOPBITS_ONE
    pathFile = "./config/SerialSetting.csv"

    def __init__(self, nameController):
        self.nameController = nameController
        self.pathFile = "./config/{}.csv".format(nameController)
        self.getSetting()

    def save(self):
        fileManager = CsvFile(filePath=self.pathFile)
        fileManager.readFile()
        if len(fileManager.dataList) < 1:
            fileManager.dataList.append([0])
        fileManager.dataList[0] = ([self.portName, self.baud, self.dataSize, self.parity, self.stopBit])
        fileManager.saveFile()

    def getSetting(self):
        fileManager = CsvFile(filePath=self.pathFile)
        data = []
        try:
            data = fileManager.readFile()[0]
        except:
            pass

        try:
            self.portName = data[self.NAME_IDX]
        except:
            self.portName = "COM1"

        try:
            self.baud = int(data[self.BAUD_IDX])
        except:
            self.baud = 115200

        try:
            self.dataSize = int(data[self.DATA_SIZE_IDX])
        except:
            self.dataSize = serial.EIGHTBITS

        try:
            self.parity = data[self.PAIRTY_IDX]
        except:
            self.parity = serial.PARITY_EVEN

        try:
            self.stopBit = float(data[self.STOP_BIT_IDX])
        except:
            self.stopBit = serial.STOPBITS_ONE
