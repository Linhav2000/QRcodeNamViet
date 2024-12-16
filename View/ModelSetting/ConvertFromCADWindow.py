import tkinter.filedialog
from CommonAssit.FileManager import TextFile
from CommonAssit.FileManager import CsvFile
import tkinter.messagebox as messagebox
import CommonAssit.CommonAssit as CommonAssit
from View.Common.VisionUI import *


class ConvertFromCADWindow(VisionTopLevel):

    cadInputEntry: VisionEntry
    csvOutputEntry: VisionEntry
    btnConvert: Button
    btnSelectCADPath: Button
    btnSelectOutputPath: Button
    btnSave: Button

    listPointRefactor = []

    def __init__(self, mainWindow):
        from MainWindow import MainWindow
        from Connection.SocketManager import SocketInfo
        VisionTopLevel.__init__(self)
        self.mainWindow: MainWindow = mainWindow
        self.windowSetting()
        self.createView()

    def windowSetting(self):
        self.title(self.mainWindow.languageManager.localized("convertPosFromCad"))
        self.iconbitmap(CommonAssit.resource_path('resource\\appIcon.ico'))
        width = 536
        height = 222
        self.geometry("{}x{}+{}+{}".format(width,
                                           height,
                                           int(self.mainWindow.mainFrame.winfo_x() + self.mainWindow.mainFrame.winfo_width() / 2 - width / 2),
                                           int(self.mainWindow.mainFrame.winfo_y() + self.mainWindow.mainFrame.winfo_height() / 2 - height / 2)))
        self.resizable(0, 0)
        self.grab_set()
        # self.protocol("WM_DELETE_WINDOW", self.close)

    def createView(self):
        cadInputLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("cadInputPath"))
        cadInputLabel.place(x=10, y =30)
        self.cadInputEntry = VisionEntry(self)
        self.cadInputEntry.place(relx=0.25, y=30, relwidth=0.5, height=25)

        self.btnSelectCADPath = VisionButton(self, text=self.mainWindow.languageManager.localized("btnFileSelect"), command=self.clickBtnSelectInputPath)
        self.btnSelectCADPath.place(relx=0.8, y=30, relwidth=0.15, height=25)

        csvOutputLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("csvOutputPath"))
        csvOutputLabel.place(x=10, y=70)
        self.csvOutputEntry = VisionEntry(self)
        self.csvOutputEntry.place(relx=0.25, y=70, relwidth=0.5, height=25)

        self.btnSelectOutputPath = VisionButton(self, text=self.mainWindow.languageManager.localized("btnFileSelect"), command=self.clickBtnSelectOutputPath)
        self.btnSelectOutputPath.place(relx=0.8, y=70, relwidth=0.15, height=25)

        self.btnConvert = VisionButton(self, text=self.mainWindow.languageManager.localized("convert"), command=self.clickBtnConvert)
        self.btnConvert.place(relx= 0.25, y=120, relwidth=0.18, height=40)

        self.btnSave = SaveButton(self, command=self.clickBtnSave)
        self.btnSave.place(relx=0.55, y=120, relwidth=0.18, height=40)

    def clickBtnConvert(self):
        try:
            filePath = self.cadInputEntry.get()
            if filePath == "":
                messagebox.showerror("Input CAD File", self.mainWindow.languageManager.localized("msg_noCADFile"))
                return
            cadFile = TextFile(filePath)
            dataList = cadFile.readFile()
            listPointData = []
            listCoordinate = []
            listPoint = []

            self.listPointRefactor = []
            for index in range(len(dataList)):
                if dataList[index] == "TEXT\n":
                    pointData = []
                    for i in range(36):
                        pointData.append(dataList[index + i])
                    listPointData.append(pointData)
                    print(pointData)
                index += 19
            for pointData in listPointData:
                try:
                    x1 = x2 = y1 = y2 = 0
                    text = ""
                    for i in range(len(pointData)):
                        if pointData[i].__contains__("10\n") and pointData[i + 2].__contains__("20\n"):
                            x1 = abs(float(pointData[i + 1]))
                            y1 = abs(float(pointData[i + 3]))
                        if pointData[i].__contains__("11\n") and pointData[i + 2].__contains__("21\n"):
                            x2 = abs(float(pointData[i + 1]))
                            y2 = abs(float(pointData[i + 3]))

                        if pointData[i].__contains__("40\n"):
                            text = pointData[i + 3]

                    listCoordinate.append([x1, y1, x2, y2, text])
                except:
                    pass

            xList = []
            yList = []
            for pointCoordinate in listCoordinate:
                try:
                    orderIndex = int(pointCoordinate[4])
                    # x = (pointCoordinate[0] + pointCoordinate[2]) / 2
                    # y = (pointCoordinate[1] + pointCoordinate[3]) / 2
                    x = pointCoordinate[2]
                    y = pointCoordinate[3]
                    listPoint.append([x, y , orderIndex])
                    xList.append(x)
                    yList.append(y)
                except:
                    pass

            minX = int(min(xList))
            minY = int(min(yList))
            changeX = minX - 10
            changeY = minY - 10

            print(changeX, changeY)
            for point in listPoint:
                xRefactor = point[0] - changeX
                yRefactor = point[1] - changeY
                self.listPointRefactor.append([xRefactor, yRefactor, point[2]])

            for pointRefactor in self.listPointRefactor:
                print(pointRefactor)

            if len(self.listPointRefactor) > 0:
                messagebox.showinfo("Convert position from CAD", self.mainWindow.languageManager.localized("msg_convertSuccessfully"))
            print(len(self.listPointRefactor))
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Convert position from CAD: {}".format(error))
            messagebox.showerror("Convert position from CAD", "{}".format(error))

    def clickBtnSave(self):
        try:
            filePath = self.csvOutputEntry.get()
            if filePath == "":
                messagebox.showerror("Output File", self.mainWindow.languageManager.localized("msg_noFileCSVOutput"))
                return

            if len(self.listPointRefactor) <= 0:
                msg=str(self.mainWindow.languageManager.localized("msg_noPointConverted"))
                messagebox.showerror("Save Data", msg)
                return

            self.listPointRefactor.insert(0, ["X", "Y"])

            fileData = CsvFile(filePath)
            fileData.dataList = self.listPointRefactor
            fileData.saveFile()
            messagebox.showinfo("Save Data", self.mainWindow.languageManager.localized("msg_saveDataSuccessfully"))
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Data: {}".format(error))
            messagebox.showerror("Save Data", "{}".format(error))

    def clickBtnSelectInputPath(self):
        filePath = tkinter.filedialog.askopenfilename(title="Select CAD file",
                                                      filetypes=(('CAD Design file', '*.dwg *.dxf'), ('All files', '*.*')),
                                                      initialdir="/áéá")
        self.cadInputEntry.delete(0, END)
        self.cadInputEntry.insert(0, filePath)
        self.cadInputEntry.xview(END)

    def clickBtnSelectOutputPath(self):
        filePath = tkinter.filedialog.asksaveasfilename(title="Select Output file",
                                                      filetypes=(
                                                      ('CSV file', '*.csv'), ('All files', '*.*')),
                                                        initialdir="/áéá")
        if not filePath.endswith(".csv"):
            filePath += ".csv"
        self.csvOutputEntry.delete(0, END)
        self.csvOutputEntry.insert(0, filePath)
        self.csvOutputEntry.xview(END)

