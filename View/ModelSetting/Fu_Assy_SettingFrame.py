from Modules.ModelSetting.ModelParameter import ModelParameter
from View.ModelSetting.VisionForFuAssyWindow import VisionForFuAssyWindow
from tkinter import messagebox
from CommonAssit import CommunicationReceiveAnalyze
import copy
from View.Common.VisionUI import *
import math

class Fu_Assy_Setting_Frame(VisionLabelFrame):

    distanceY = 0.08
    moveDistance = 2.5
    convertPointRU1 = None
    convertPointRU2 = None
    convertPointFU1 = None
    convertPointFU2 = None

    caliDesignRuRef1 = None
    caliRuPosition = None

    caliDesignFuRef1 = None
    caliFuPosition = None

    convertPoint1 = None
    def __init__(self, master, mainWindow, text=""):
        from View.ModelSetting.ModelSettingTab import ModelSettingTab
        from MainWindow import MainWindow
        VisionLabelFrame.__init__(self, master, text=text)
        self.modelSettingTab: ModelSettingTab = master
        self.mainWindow: MainWindow = mainWindow
        self.parameter = ModelParameter()
        self.setupView()


    def setupView(self):
        # RU reference point 1
        self.ruRef1Lbl = VisionLabel(self, text=self.mainWindow.languageManager.localized("ruRef1Lbl"))
        self.ruRef1Lbl.place(relx=0.02, y=5)

        self.ruRefPoint1xEntry = VisionEntry(self)
        self.ruRefPoint1xEntry.place(relx=0.22, y=5, relwidth=0.2, relheight=0.045)

        self.ruRefPoint1yEntry = VisionEntry(self)
        self.ruRefPoint1yEntry.place(relx=0.52, y=5, relwidth=0.2, relheight=0.045)

        # RU reference point 2
        self.ruRef2Lbl = VisionLabel(self, text=self.mainWindow.languageManager.localized("ruRef2Lbl"))
        self.ruRef2Lbl.place(relx=0.02, rely=self.distanceY)

        self.ruRefPoint2xEntry = VisionEntry(self)
        self.ruRefPoint2xEntry.place(relx=0.22, rely=self.distanceY, relwidth=0.2, relheight=0.045)

        self.ruRefPoint2yEntry = VisionEntry(self)
        self.ruRefPoint2yEntry.place(relx=0.52, rely=self.distanceY, relwidth=0.2, relheight=0.045)

        # FU reference point 1
        self.fuRef1Lbl = VisionLabel(self, text=self.mainWindow.languageManager.localized("fuRef1Lbl"))
        self.fuRef1Lbl.place(relx=0.02, rely=2*self.distanceY)

        self.fuRefPoint1xEntry = VisionEntry(self)
        self.fuRefPoint1xEntry.place(relx=0.22,rely=2*self.distanceY, relwidth=0.2, relheight=0.045)

        self.fuRefPoint1yEntry = VisionEntry(self)
        self.fuRefPoint1yEntry.place(relx=0.52, rely=2*self.distanceY, relwidth=0.2, relheight=0.045)

        # FU reference point 2
        self.fuRef2Lbl = VisionLabel(self, text=self.mainWindow.languageManager.localized("fuRef2Lbl"))
        self.fuRef2Lbl.place(relx=0.02, rely=3*self.distanceY)

        self.fuRefPoint2xEntry = VisionEntry(self)
        self.fuRefPoint2xEntry.place(relx=0.22, rely=3*self.distanceY, relwidth=0.2, relheight=0.045)

        self.fuRefPoint2yEntry = VisionEntry(self)
        self.fuRefPoint2yEntry.place(relx=0.52, rely=3*self.distanceY, relwidth=0.2, relheight=0.045)

        # conversion Ru coefficient

        self.conversionRuLbl = VisionLabel(self, text=self.mainWindow.languageManager.localized("conversionRuLbl"))
        self.conversionRuLbl.place(relx=0.02, rely=4 * self.distanceY)

        self.conversionRuEntry = VisionEntry(self)
        self.conversionRuEntry.place(relx=0.35, rely=4 * self.distanceY, relwidth=0.25, relheight=0.045)

        self.btnTakeRuCoefficient = VisionButton(self, text=self.mainWindow.languageManager.localized("btnTakeRuCoefficient"),
                                         command=self.clickBtnTakeRuCoef)
        self.btnTakeRuCoefficient.place(relx=0.65, rely=3.9 * self.distanceY, relwidth=0.3)

        # conversion Fu coefficient

        self.conversionFuLbl = VisionLabel(self, text=self.mainWindow.languageManager.localized("conversionFuLbl"))
        self.conversionFuLbl.place(relx=0.02, rely=5 * self.distanceY)

        self.conversionFuEntry = VisionEntry(self)
        self.conversionFuEntry.place(relx=0.35, rely=5 * self.distanceY, relwidth=0.25, relheight=0.045)

        self.btnTakeFuCoefficient = VisionButton(self, text=self.mainWindow.languageManager.localized("btnTakeFuCoefficient"),
                                           command=self.clickBtnTakeFuCoef)
        self.btnTakeFuCoefficient.place(relx=0.65, rely=4.9 * self.distanceY, relwidth=0.3)

        # offset value
        self.offsetParmLbl = VisionLabel(self, text=self.mainWindow.languageManager.localized("offsetParmLbl"))
        self.offsetParmLbl.place(relx=0.02, rely=6 * self.distanceY)

        self.offsetXEntry = VisionEntry(self)
        self.offsetXEntry.place(relx=0.22, rely=6 * self.distanceY, relwidth=0.18, relheight=0.045)

        self.offsetYEntry = VisionEntry(self)
        self.offsetYEntry.place(relx=0.46, rely=6 * self.distanceY, relwidth=0.18, relheight=0.045)

        self.offsetZEntry = VisionEntry(self)
        self.offsetZEntry.place(relx=0.70, rely=6 * self.distanceY, relwidth=0.18, relheight=0.045)

        self.btnRuCaliOffset = VisionButton(self, text=self.mainWindow.languageManager.localized("CaliRuOffsetBtn"),
                                      command=self.clickBtnRuCaliOffset)
        self.btnRuCaliOffset.place(relx=0.02, rely=7 * self.distanceY, relwidth=0.3)

        self.btnFuCaliOffset = VisionButton(self, text=self.mainWindow.languageManager.localized("CaliFuOffsetBtn"),
                                      command=self.clickBtnFuCaliOffset)
        self.btnFuCaliOffset.place(relx=0.36, rely=7 * self.distanceY, relwidth=0.3)

        self.btnGetOffset = VisionButton(self, text=self.mainWindow.languageManager.localized("getOffsetBtn"),
                                   command=self.clickBtnGetOffset)
        self.btnGetOffset.place(relx=0.70, rely=7 * self.distanceY, relwidth=0.25)

        self.btnVisionSetting = VisionButton(self, text=self.mainWindow.languageManager.localized("visionSettingBtn"),
                                       command=self.clickBtnVisionSetting)
        self.btnVisionSetting.place(relx=0.41, rely=8 * self.distanceY, relwidth=0.3)


    def clickBtnRuCaliOffset(self):
        if self.checkDeviceConnection():
            designOffsetPointX, designOffsetPointY = self.parameter.ruRef1Design

            caliDesignRuRef1X = int(self.mainWindow.workingThread.fu_assy_adjusting.plcLengthScale * (self.mainWindow.workingThread.fu_assy_adjusting.mirrorXValue - designOffsetPointX))
            caliDesignRuRef1Y = int(self.mainWindow.workingThread.fu_assy_adjusting.plcLengthScale * designOffsetPointY)

            self.caliDesignRuRef1 = (caliDesignRuRef1X, caliDesignRuRef1Y)
            self.modelSettingTab.startCaliRuOffsetFlag = True

    def clickBtnFuCaliOffset(self):
        if self.checkDeviceConnection():
            designOffsetPointX, designOffsetPointY = self.parameter.fuRef1Design

            caliDesignFuRef1X = int(self.mainWindow.workingThread.fu_assy_adjusting.plcLengthScale * (
                        self.mainWindow.workingThread.fu_assy_adjusting.mirrorXValue - designOffsetPointX))
            caliDesignFuRef1Y = int(self.mainWindow.workingThread.fu_assy_adjusting.plcLengthScale * designOffsetPointY)

            self.caliDesignFuRef1 = (caliDesignFuRef1X, caliDesignFuRef1Y)
            self.modelSettingTab.startCaliFuOffsetFlag = True

    def clickBtnTakeRuCoef(self):
        if self.checkDeviceConnection():
            self.modelSettingTab.startTakeRuCoefFlag = True

    def clickBtnTakeFuCoef(self):
        if self.checkDeviceConnection():
            self.modelSettingTab.startTakeFuCoefFlag = True

    def clickBtnGetOffset(self):
        if self.checkDeviceConnection():
            self.modelSettingTab.getOffsetFlag = True

    def clickBtnVisionSetting(self):
        visionSetting = VisionForFuAssyWindow(self.mainWindow, self.parameter)
        visionSetting.wait_window()
        if visionSetting.saveFlag:
            self.modelSettingTab.save()
    def checkDeviceConnection(self):
        if self.mainWindow.workingThread.fu_assy_adjusting.isReady():
            return True
        else:
            if self.mainWindow.workingThread.fu_assy_adjusting.startWorking():
                return True
            else:
                messagebox.showwarning("FU Adjusting", "Devices are still not ready\nCheck camera, light")
                return False

    def save(self, parameter: ModelParameter):
        try:
            parameter.ruCameraId = self.parameter.ruCameraId
            parameter.fuCameraId = self.parameter.fuCameraId
            parameter.ruAlgorithm = self.parameter.ruAlgorithm
            parameter.fuAlgorithm = self.parameter.fuAlgorithm
            parameter.ruLightId = self.parameter.ruLightId
            parameter.fuLightId = self.parameter.fuLightId
            parameter.plcFuRef1Pos = self.parameter.plcFuRef1Pos
            parameter.plcRuRef1Pos = self.parameter.plcRuRef1Pos
            parameter.plcRuCali = self.parameter.plcRuCali
            parameter.plcFuCali = self.parameter.plcFuCali

            parameter.ruConversionCoef = float(self.conversionRuEntry.get())
            parameter.fuConversionCoef = float(self.conversionFuEntry.get())

            parameter.ruRef1Design = (float(self.ruRefPoint1xEntry.get()), float(self.ruRefPoint1yEntry.get()))
            parameter.ruRef2Design = (float(self.ruRefPoint2xEntry.get()), float(self.ruRefPoint2yEntry.get()))
            parameter.fuRef1Design = (float(self.fuRefPoint1xEntry.get()), float(self.fuRefPoint1yEntry.get()))
            parameter.fuRef2Design = (float(self.fuRefPoint2xEntry.get()), float(self.fuRefPoint2yEntry.get()))

            parameter.offset = (int(float(self.offsetXEntry.get())),
                                int(float(self.offsetYEntry.get())),
                                int(float(self.offsetZEntry.get())))


            plcLengthScale = self.mainWindow.workingThread.fu_assy_adjusting.plcLengthScale
            deltaRuX = int(plcLengthScale * float(self.parameter.ruRef2Design[0])) - int(plcLengthScale * float(self.parameter.ruRef1Design[0]))
            deltaRuY = int(plcLengthScale * float(self.parameter.ruRef2Design[1])) - int(plcLengthScale * float(self.parameter.ruRef1Design[1]))

            parameter.plcRuRef2Pos = (int(float(self.parameter.plcRuRef1Pos[0]) + deltaRuX),
                                        int(float(self.parameter.plcRuRef1Pos[1]) + deltaRuY),
                                        int(float(self.parameter.plcRuRef1Pos[2])),
                                        int(float(self.parameter.plcRuRef1Pos[3])))

            deltaFuX = int(plcLengthScale * float(self.parameter.fuRef2Design[0])) - int(plcLengthScale * float(self.parameter.fuRef1Design[0]))
            deltaFuY = int(plcLengthScale * float(self.parameter.fuRef2Design[1])) - int(plcLengthScale * float(self.parameter.fuRef1Design[1]))

            parameter.plcFuRef2Pos = (int(float(self.parameter.plcFuRef1Pos[0]) - deltaFuX),
                                      int(float(self.parameter.plcFuRef1Pos[1]) - deltaFuY),
                                      int(float(self.parameter.plcFuRef1Pos[2])),
                                      int(float(self.parameter.plcFuRef1Pos[3])))

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save FU assy parameter: {}".format(error))
            print("Save FU assy parameter: {}".format(error))

    def isChanged(self, currentParameter: ModelParameter):
        ret = False
        ret = ret or currentParameter.ruCameraId != self.parameter.ruCameraId
        ret = ret or currentParameter.fuCameraId != self.parameter.fuCameraId
        ret = ret or currentParameter.ruAlgorithm != self.parameter.ruAlgorithm
        ret = ret or currentParameter.fuAlgorithm != self.parameter.fuAlgorithm
        ret = ret or currentParameter.ruLightId != self.parameter.ruLightId
        ret = ret or currentParameter.fuLightId != self.parameter.fuLightId
        ret = ret or currentParameter.plcFuRef1Pos != self.parameter.plcFuRef1Pos
        ret = ret or currentParameter.plcRuRef1Pos != self.parameter.plcRuRef1Pos
        ret = ret or currentParameter.plcRuCali != self.parameter.plcRuCali
        ret = ret or currentParameter.plcFuCali != self.parameter.plcFuCali

        ret = ret or currentParameter.ruConversionCoef != float(self.conversionRuEntry.get())
        ret = ret or currentParameter.fuConversionCoef != float(self.conversionFuEntry.get())

        ret = ret or currentParameter.ruRef1Design != (float(self.ruRefPoint1xEntry.get()), float(self.ruRefPoint1yEntry.get()))
        ret = ret or currentParameter.ruRef2Design != (float(self.ruRefPoint2xEntry.get()), float(self.ruRefPoint2yEntry.get()))
        ret = ret or currentParameter.fuRef1Design != (float(self.fuRefPoint1xEntry.get()), float(self.fuRefPoint1yEntry.get()))
        ret = ret or currentParameter.fuRef2Design != (float(self.fuRefPoint2xEntry.get()), float(self.fuRefPoint2yEntry.get()))

        ret = ret or currentParameter.offset != (int(float(self.offsetXEntry.get())),
                            int(float(self.offsetYEntry.get())),
                            int(float(self.offsetZEntry.get())))

        plcLengthScale = self.mainWindow.workingThread.fu_assy_adjusting.plcLengthScale
        deltaRuX = int(plcLengthScale * float(self.parameter.ruRef2Design[0])) - int(
            plcLengthScale * float(self.parameter.ruRef1Design[0]))
        deltaRuY = int(plcLengthScale * float(self.parameter.ruRef2Design[1])) - int(
            plcLengthScale * float(self.parameter.ruRef1Design[1]))

        ret = ret or currentParameter.plcRuRef2Pos != (int(float(self.parameter.plcRuRef1Pos[0]) + deltaRuX),
                                  int(float(self.parameter.plcRuRef1Pos[1]) + deltaRuY),
                                  int(float(self.parameter.plcRuRef1Pos[2])),
                                  int(float(self.parameter.plcRuRef1Pos[3])))

        deltaFuX = int(plcLengthScale * float(self.parameter.fuRef2Design[0])) - int(
            plcLengthScale * float(self.parameter.fuRef1Design[0]))
        deltaFuY = int(plcLengthScale * float(self.parameter.fuRef2Design[1])) - int(
            plcLengthScale * float(self.parameter.fuRef1Design[1]))

        ret = ret or currentParameter.plcFuRef2Pos != (int(float(self.parameter.plcFuRef1Pos[0]) - deltaFuX),
                                  int(float(self.parameter.plcFuRef1Pos[1]) - deltaFuY),
                                  int(float(self.parameter.plcFuRef1Pos[2])),
                                  int(float(self.parameter.plcFuRef1Pos[3])))

        return ret

    def updateParameter(self, parameter: ModelParameter):
        self.parameter = parameter
        try:
            self.ruRefPoint1xEntry.delete(0, END)
            self.ruRefPoint1yEntry.delete(0, END)
            self.ruRefPoint2xEntry.delete(0, END)
            self.ruRefPoint2yEntry.delete(0, END)
            self.fuRefPoint1xEntry.delete(0, END)
            self.fuRefPoint1yEntry.delete(0, END)
            self.fuRefPoint2xEntry.delete(0, END)
            self.fuRefPoint2yEntry.delete(0, END)
            self.conversionRuEntry.delete(0, END)
            self.conversionFuEntry.delete(0, END)
            self.offsetXEntry.delete(0, END)
            self.offsetYEntry.delete(0, END)
            self.offsetZEntry.delete(0, END)


            self.ruRefPoint1xEntry.insert(0, "{}".format(self.parameter.ruRef1Design[0]))
            self.ruRefPoint1yEntry.insert(0, "{}".format(self.parameter.ruRef1Design[1]))
            self.ruRefPoint2xEntry.insert(0, "{}".format(self.parameter.ruRef2Design[0]))
            self.ruRefPoint2yEntry.insert(0, "{}".format(self.parameter.ruRef2Design[1]))
            self.fuRefPoint1xEntry.insert(0, "{}".format(self.parameter.fuRef1Design[0]))
            self.fuRefPoint1yEntry.insert(0, "{}".format(self.parameter.fuRef1Design[1]))
            self.fuRefPoint2xEntry.insert(0, "{}".format(self.parameter.fuRef2Design[0]))
            self.fuRefPoint2yEntry.insert(0, "{}".format(self.parameter.fuRef2Design[1]))
            self.conversionRuEntry.insert(0, "{}".format(self.parameter.ruConversionCoef))
            self.conversionFuEntry.insert(0, "{}".format(self.parameter.fuConversionCoef))
            self.offsetXEntry.insert(0, "{}".format(self.parameter.offset[0]))
            self.offsetYEntry.insert(0, "{}".format(self.parameter.offset[1]))
            self.offsetZEntry.insert(0, "{}".format(self.parameter.offset[2]))

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Update fu assy parameter: {}".format(error))
            print("Update fu assy parameter: {}".format(error))


    def takeConvertRU1(self, plcRev):
        # "00000,00000,00000,00000,CONVERTA,1"
        try:
            ret, image = self.mainWindow.workingThread.fu_assy_adjusting.ruCamera.takePicture()
            if ret:
                ret, circle, _ = self.mainWindow.workingThread.fu_assy_adjusting.getRefPosition(image,
                                                                                                self.mainWindow.workingThread.fu_assy_adjusting.ruAlgorithm)
                if ret:
                    self.convertPoint1 = circle[0]
                    plcRevInfo = CommunicationReceiveAnalyze.getFuAssyInfo(plcRev)
                    plcConvertPoint1 = (plcRevInfo.x, plcRevInfo.y, plcRevInfo.z, plcRevInfo.u)

                    self.parameter.plcRuRef1Pos = plcConvertPoint1

                    plcConvertPoint2 = (plcConvertPoint1[0] + int(self.mainWindow.workingThread.fu_assy_adjusting.plcLengthScale * self.moveDistance),
                                        plcConvertPoint1[1],
                                        plcConvertPoint1[2],
                                        plcConvertPoint1[3])
                    return ret, plcConvertPoint2
                else:
                    messagebox.showerror("Conversion Coefficient", "Cannot detect the reference position!")
                    return ret, None
            else:
                messagebox.showerror("Conversion Coefficient", "Cannot detect the reference position!")
                return ret, None
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Conversion Coefficient: {}".format(error))
            messagebox.showerror("Conversion Coefficient", "{}".format(error))
            return False, None

    def takeConvertRU2(self):
        try:
            ret, image = self.mainWindow.workingThread.fu_assy_adjusting.ruCamera.takePicture()
            if ret:
                ret, circle, _  = self.mainWindow.workingThread.fu_assy_adjusting.getRefPosition(image,
                                                                                                self.mainWindow.workingThread.fu_assy_adjusting.ruAlgorithm)
                self.convertPoint2 = circle[0]
                if not ret:
                    messagebox.showerror("Conversion Coefficient", "Cannot detect the reference position!")
        except:
            return False
        res, coef = self.calculateConversionCoef()
        if res:
            self.conversionRuEntry.delete(0, END)
            self.conversionRuEntry.insert(0, "{}".format(coef))
        return res and ret

    def takeConvertFU1(self, plcRev):
        # "00000,00000,00000,00000,CONVERTA,1"
        try:
            ret, image = self.mainWindow.workingThread.fu_assy_adjusting.fuCamera.takePicture()
            if ret:
                ret, circle, _ = self.mainWindow.workingThread.fu_assy_adjusting.getRefPosition(image,
                                                                                                self.mainWindow.workingThread.fu_assy_adjusting.fuAlgorithm)
                if ret:
                    self.convertPoint1 = circle[0]
                    plcRevInfo = CommunicationReceiveAnalyze.getFuAssyInfo(plcRev)
                    plcConvertPoint1 = (plcRevInfo.x, plcRevInfo.y, plcRevInfo.z, plcRevInfo.u)

                    self.parameter.plcFuRef1Pos = plcConvertPoint1

                    plcConvertPoint2 = (plcConvertPoint1[0] + int(self.mainWindow.workingThread.fu_assy_adjusting.plcLengthScale * self.moveDistance),
                                        plcConvertPoint1[1],
                                        plcConvertPoint1[2],
                                        plcConvertPoint1[3])
                    return ret, plcConvertPoint2
                else:
                    messagebox.showerror("Conversion Coefficient", "Cannot detect the reference position!")
                    return ret, None
            else:
                messagebox.showerror("Conversion Coefficient", "Cannot detect the reference position!")
                return ret, None
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Conversion Coefficient: {}".format(error))
            messagebox.showerror("Conversion Coefficient", "{}".format(error))
            return False, None

    def takeConvertFU2(self):
        try:
            ret, image = self.mainWindow.workingThread.fu_assy_adjusting.fuCamera.takePicture()
            if ret:
                ret, circle, _  = self.mainWindow.workingThread.fu_assy_adjusting.getRefPosition(image,
                                                                                                self.mainWindow.workingThread.fu_assy_adjusting.fuAlgorithm)
                self.convertPoint2 = circle[0]
                if not ret:
                    messagebox.showerror("Conversion Coefficient", "Cannot detect the reference position!")
        except:
            return False
        res, coef = self.calculateConversionCoef()
        if res:
            self.conversionFuEntry.delete(0, END)
            self.conversionFuEntry.insert(0, "{}".format(coef))
        return res and ret

    def calculateConversionCoef(self):
        try:
            x1, y1 = self.convertPoint1
            x2, y2 = self.convertPoint2
            distance = math.sqrt((int(x2) - int(x1)) ** 2 + (int(y2) - int(y1)) ** 2)
            coefficient = math.fabs(self.moveDistance)/ distance

            return True, coefficient
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Calculate conversion coefficient: {}".format(error))
            messagebox.showerror("Calculate conversion coefficient", "{}".format(error))
            return False, None

    def caliOffsetRU(self, plcValue):
        # XXXXX,YYYYY,ZZZZZ,OFFSETC
        move = False
        caliPos = (0, 0)
        try:
            plcRevInfo = CommunicationReceiveAnalyze.getFuAssyInfo(plcValue)
            currentX = plcRevInfo.x
            currentY = plcRevInfo.y
            currentZ = plcRevInfo.z
            currentU = plcRevInfo.u
            caliPos = (currentX, currentY, currentZ, currentU)
            ret, image = self.mainWindow.workingThread.fu_assy_adjusting.ruCamera.takePicture()
            # image = ImageProcess.flipHorizontal(image.copy()) # because the origin of axis coordinates is different from machine axis coordinates

            centerImageY = int(image.shape[0]/2)
            centerImageX = int(image.shape[1]/2)
            if ret:
                ret, circle, _ = self.mainWindow.workingThread.fu_assy_adjusting.getRefPosition(image,
                                                                                                self.mainWindow.workingThread.fu_assy_adjusting.ruAlgorithm)
                (currentCoordinateX, currentCoordinateY) = circle[0]
                pixelDeltaX = currentCoordinateX - centerImageX
                pixelDeltaY = currentCoordinateY - centerImageY

                conversionCoef = float(self.conversionRuEntry.get())

                if pixelDeltaX > 10 or pixelDeltaY > 10 or pixelDeltaX < -10 or pixelDeltaY < -10:
                    deltaX = int(self.mainWindow.workingThread.fu_assy_adjusting.plcLengthScale * (pixelDeltaX * conversionCoef))
                    deltaY = int(self.mainWindow.workingThread.fu_assy_adjusting.plcLengthScale * (pixelDeltaY * conversionCoef))

                    caliPosX = currentX - deltaX
                    caliPosY = currentY + deltaY

                    self.caliDesignRuRef1 = (self.caliDesignRuRef1[0] + deltaX, self.caliDesignRuRef1[1] + deltaY)
                    caliPos = (caliPosX, caliPosY, currentZ, currentU)
                    self.caliRuPosition = caliPos
                    move = True
                else:
                    self.caliRuPosition = caliPos
                    self.btnGetOffset.config(state="normal")

                if not ret:
                    messagebox.showerror("Calibration Offset", "Cannot take find reference position!")
                    move = False
            else:
                messagebox.showerror("Calibration Offset", "Cannot take find reference position!")

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Calibrate Offset: {}".format(error))
            messagebox.showerror("Calibrate Offset", "{}".format(error))
        return move, caliPos

    def caliOffsetFU(self, plcValue):
        # XXXXX,YYYYY,ZZZZZ,OFFSETC
        move = False
        caliPos = (0, 0)
        try:
            plcRevInfo = CommunicationReceiveAnalyze.getFuAssyInfo(plcValue)
            currentX = plcRevInfo.x
            currentY = plcRevInfo.y
            currentZ = plcRevInfo.z
            currentU = plcRevInfo.u
            caliPos = (currentX, currentY, currentZ, currentU)
            ret, image = self.mainWindow.workingThread.fu_assy_adjusting.fuCamera.takePicture()
            centerImageY = int(image.shape[0]/2)
            centerImageX = int(image.shape[1]/2)
            if ret:
                ret, circle, _ = self.mainWindow.workingThread.fu_assy_adjusting.getRefPosition(image,
                                                                                                self.mainWindow.workingThread.fu_assy_adjusting.fuAlgorithm)
                (currentCoordinateX, currentCoordinateY) = circle[0]
                pixelDeltaX = currentCoordinateX - centerImageX
                pixelDeltaY = currentCoordinateY - centerImageY

                conversionCoef = float(self.conversionFuEntry.get())

                if pixelDeltaX > 10 or pixelDeltaY > 10 or pixelDeltaX < -10 or pixelDeltaY < -10:
                    deltaX = int(self.mainWindow.workingThread.fu_assy_adjusting.plcLengthScale * (pixelDeltaX * conversionCoef))
                    deltaY = int(self.mainWindow.workingThread.fu_assy_adjusting.plcLengthScale * (pixelDeltaY * conversionCoef))

                    caliPosX = currentX + deltaX
                    caliPosY = currentY - deltaY

                    self.caliDesignFuRef1 = (self.caliDesignFuRef1[0] + deltaX, self.caliDesignFuRef1[1] + deltaY)
                    caliPos = (caliPosX, caliPosY, currentZ, currentU)
                    self.caliFuPosition = caliPos
                    move = True
                else:
                    self.btnGetOffset.config(state="normal")

                if not ret:
                    messagebox.showerror("Calibration Offset", "Cannot take find reference position!")
                    move = False
            else:
                messagebox.showerror("Calibration Offset", "Cannot take find reference position!")
                move = False
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Calibrate Offset: {}".format(error))
            messagebox.showerror("Calibrate Offset", "{}".format(error))
        return move, caliPos

    def setOffsetValue(self, plcValue):
        try:
            plcRevInfo = CommunicationReceiveAnalyze.getFuAssyInfo(plcValue)
            offsetX = plcRevInfo.x
            offsetY = plcRevInfo.y
            offsetZ = plcRevInfo.z
            offsetU = plcRevInfo.u
            #
            # plcRuRef1X, plcRuRef1Y, plcRuRef1Z, plcRuRef1U = self.parameter.plcRuRef1Pos
            # plcFuRef1X, plcFuRef1Y, plcFuRef1Z, plcFuRef1U = self.parameter.plcFuRef1Pos
            #
            # caliRuRef1X,caliRuRef1Y,caliRuRef1Z,caliRuRef1U, = self.caliRuPosition
            # caliFuRef1X,caliFuRef1Y,caliFuRef1Z,caliFuRef1U, = self.caliFuPosition


            #
            # deltaRuX = caliRuRef1X - plcRuRef1X
            # deltaRuY = caliRuRef1Y - plcRuRef1Y
            # deltaRuZ = caliRuRef1Z - plcRuRef1Z
            # deltaRuU = caliRuRef1U - plcRuRef1U
            #
            # deltaFuX = caliFuRef1X - plcFuRef1X
            # deltaFuY = caliFuRef1Y - plcFuRef1Y
            # deltaFuZ = caliFuRef1Z - plcFuRef1Z
            # deltaFuU = caliFuRef1U - plcFuRef1U
            #
            # # = plcRuRef1X - plcFuRef1X
            # deltaMoveX = offsetX - caliRuRef1X - caliFuRef1X
            # deltaMoveY = offsetY - caliRuRef1Y - caliFuRef1Y

            self.parameter.plcRuCali = copy.deepcopy(self.caliRuPosition)
            self.parameter.plcFuCali = copy.deepcopy(self.caliFuPosition)

            self.offsetXEntry.delete(0, END)
            self.offsetYEntry.delete(0, END)
            self.offsetZEntry.delete(0, END)

            self.offsetXEntry.insert(0, offsetX)
            self.offsetYEntry.insert(0, offsetY)
            self.offsetZEntry.insert(0, offsetZ)

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Set offset: {}".format(error))
            messagebox.showerror("Set offset", "{}".format(error))