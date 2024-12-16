import serial.tools.list_ports
import CommonAssit.CommonAssit as CommonAssit
from View.Common.VisionUI import *

class SerialSettingFrame(VisionLabelFrame):

    comNames = []
    baudRates = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]
    dataSizes = []
    parities = []
    stopBits = []

    partiesMap = {"NONE": serial.PARITY_NONE,
                  "EVEN": serial.PARITY_EVEN,
                  "ODD": serial.PARITY_ODD,
                  "MARK": serial.PARITY_MARK,
                  "SPACE": serial.PARITY_SPACE}

    stopBitMap = {"1": serial.STOPBITS_ONE,
                  "1.5": serial.STOPBITS_ONE_POINT_FIVE,
                  "2": serial.STOPBITS_TWO}

    dataSizemMap = {"5": serial.FIVEBITS,
                    "6": serial.SIXBITS,
                    "7": serial.SEVENBITS,
                    "8": serial.EIGHTBITS}

    # bauds = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]
    activePorts = serial.tools.list_ports.comports()
    comshows = []

    comComboBox: ttk.Combobox
    baudComboBox: ttk.Combobox
    dataSizeComboBox: ttk.Combobox
    parityComboBox: ttk.Combobox
    stopBitComboBox: ttk.Combobox

    btnSave: Button

    def __init__(self, master, mainWindow, serialInfo):
        from MainWindow import MainWindow
        from Connection.SerialManager import SerialInfo
        VisionLabelFrame.__init__(self, text="Serial Parameter", master=master)
        self.serialInfo: SerialInfo = serialInfo
        self.mainWindow: MainWindow = mainWindow
        self.initVariables()
        self.createView()
        self.showLastSetting()

    def initVariables(self):
        self.parities = list(self.partiesMap.keys())
        self.stopBits = list(self.stopBitMap.keys())
        self.dataSizes = list(self.dataSizemMap.keys())

        self.activePorts = serial.tools.list_ports.comports()
        self.comNames = []
        self.comshows = []
        for port in self.activePorts:
            if port[2] != 'n/a':
                self.comshows.append("{} ({})".format(port.device, port.description))
                self.comNames.append("{}".format(port.device))


    def createView(self):
        heightSpace = 25
        comboWidth = 280
        heightDisplacement = 80

        # COM name
        comLabel = VisionLabel(self, text="COM Port")
        comLabel.place(x=10, y=10)
        self.comComboBox = ttk.Combobox(self, value=self.comshows, state='readonly', cursor="hand2")
        self.comComboBox.place(x=10, y=35, width=comboWidth, height=heightSpace)

        # baud rate
        comLabel = VisionLabel(self, text="Baud rate")
        comLabel.place(x=10, y=heightDisplacement)
        self.baudComboBox = ttk.Combobox(self, value=self.baudRates, state='readonly', cursor="hand2")
        self.baudComboBox.place(x=10, y=heightDisplacement + 25, width=comboWidth, height=heightSpace)

        # Data size
        comLabel = VisionLabel(self, text="Data size")
        comLabel.place(x=10, y=2 * heightDisplacement)
        self.dataSizeComboBox = ttk.Combobox(self, value=self.dataSizes, state='readonly', cursor="hand2")
        self.dataSizeComboBox.place(x=10, y=2 * heightDisplacement + 25, width=comboWidth, height=heightSpace)

        # Parity
        comLabel = VisionLabel(self, text="Parity")
        comLabel.place(x=10, y=3 * heightDisplacement)
        self.parityComboBox = ttk.Combobox(self, value=self.parities, state='readonly', cursor="hand2")
        self.parityComboBox.place(x=10, y=3 * heightDisplacement + 25, width=comboWidth, height=heightSpace)

        # Stop bit
        comLabel = VisionLabel(self, text="Stop bit")
        comLabel.place(x=10, y=4 * heightDisplacement)
        self.stopBitComboBox = ttk.Combobox(self, value=self.stopBits, state='readonly', cursor="hand2")
        self.stopBitComboBox.place(x=10, y=4 * heightDisplacement + 25, width=comboWidth, height=heightSpace)


    def showLastSetting(self):
        self.baudComboBox.current(self.baudRates.index(self.serialInfo.baud))
        try:
            self.comComboBox.current(self.comNames.index(self.serialInfo.portName))
        except:
            pass
        self.dataSizeComboBox.current(CommonAssit.getIndexByValue(self.dataSizemMap, self.serialInfo.dataSize)[0])
        self.parityComboBox.current(CommonAssit.getIndexByValue(self.partiesMap, self.serialInfo.parity)[0])
        self.stopBitComboBox.current(CommonAssit.getIndexByValue(self.stopBitMap, self.serialInfo.stopBit)[0])