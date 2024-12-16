import serial.tools.list_ports
import CommonAssit.CommonAssit as CommonAssit
import tkinter.messagebox as messagebox
from View.Common.VisionUI import *

class SerialSettingView(VisionTopLevel):

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

    def __init__(self, mainWindow, serialInfo, title = ''):
        from MainWindow import MainWindow
        from Connection.SerialManager import SerialInfo
        VisionTopLevel.__init__(self)
        self._title = title
        self.serialInfo: SerialInfo = serialInfo
        self.mainWindow: MainWindow = mainWindow
        self.windowSetting()
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

    def windowSetting(self):
        width = 320
        height = 500
        self.title(self._title)
        self.iconbitmap(CommonAssit.resource_path('resource\\appIcon.ico'))
        self.geometry("{}x{}+{}+{}".format(width, height, int(self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width()/2 - width/2),
                                             int(self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height()/2 - height/2)))
        self.resizable(0, 0)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.close)

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

        self.btnSave = SaveButton(self, command=self.save)
        self.btnSave.place(relx=0.35, y=5 * heightDisplacement, relwidth=0.3, height=40)

    def showLastSetting(self):
        self.baudComboBox.current(self.baudRates.index(self.serialInfo.baud))
        try:
            self.comComboBox.current(self.comNames.index(self.serialInfo.portName))
        except:
            pass
        self.dataSizeComboBox.current(CommonAssit.getIndexByValue(self.dataSizemMap, self.serialInfo.dataSize)[0])
        self.parityComboBox.current(CommonAssit.getIndexByValue(self.partiesMap, self.serialInfo.parity)[0])
        self.stopBitComboBox.current(CommonAssit.getIndexByValue(self.stopBitMap, self.serialInfo.stopBit)[0])

    def save(self):
        try:
            self.serialInfo.portName = self.comNames[self.comComboBox.current()]
            self.serialInfo.baud = self.baudRates[self.baudComboBox.current()]
            self.serialInfo.dataSize = self.dataSizemMap[self.dataSizeComboBox.get()]
            self.serialInfo.parity = self.partiesMap[self.parityComboBox.get()]
            self.serialInfo.stopBit = self.stopBitMap[self.stopBitComboBox.get()]

            self.serialInfo.save()
            self.destroy()

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Serial Info : {}".format(error))
            messagebox.showerror("Save Serial Info", "{}".format(error))

    def close(self):
        try:
            if self.serialInfo.portName != self.comNames[self.comComboBox.current()] \
                or self.serialInfo.baud!= self.baudRates[self.baudComboBox.current()] \
                or self.serialInfo.dataSize != self.dataSizemMap[self.dataSizeComboBox.get()] \
                or self.serialInfo.parity != self.partiesMap[self.parityComboBox.get()] \
                or self.serialInfo.stopBit != self.stopBitMap[self.stopBitComboBox.get()]:
                askSave = messagebox.askyesno("Serial Info Changes", "Would you like to save the data you have changed?")
                if askSave:
                    self.save()
        except:
            pass

        self.destroy()
