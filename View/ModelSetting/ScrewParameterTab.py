from tkinter import messagebox
from View.ModelSetting.VisionSettingWindow import VisionSettingWindow
from View.ModelSetting.ActivePointAdvanceSettingView import ActivePointAdvanceSettingView
from View.ModelSetting.ModelSettingTab import NumOfRefPoint
from Modules.ModelSetting.ModelParameter import ModelParameter
import tkinter.filedialog
from View.Common.VisionUI import *
from ImageProcess import ImageProcess
import math

class ScrewParameterTab(VisionFrame):

    numOfRefPointList = []

    screwParameterFrame: VisionFrame
    numOfRefPointCombo: ttk.Combobox
    ref1Lbl: VisionLabel
    refPoint1xEntry: VisionEntry
    btnRef1Select: Button
    refPoint1yEntry: VisionEntry
    ref2Lbl: VisionLabel
    refPoint2xEntry: VisionEntry
    refPoint2yEntry: VisionEntry
    btnRef2Select: Button
    ref3Lbl: VisionLabel
    refPoint3xEntry: VisionEntry
    refPoint3yEntry: VisionEntry
    btnRef3Select: Button
    offsetPointLbl: VisionLabel
    offsetPointXEntry: VisionEntry
    offsetPointYEntry: VisionEntry
    btnOffsetPointSelect: Button
    offsetParmLbl: VisionLabel
    offsetXEntry: VisionEntry
    offsetYEntry: VisionEntry
    offsetZEntry: VisionEntry
    btnCaliOffset: Button
    btnGetOffset: Button
    conversionLbl: VisionLabel
    conversionCoefficientEntry: VisionEntry
    btnTakeCoefficient: Button
    designPathLbl: VisionLabel
    filePathEntry: VisionEntry
    btnSelectDesignFile: Button
    activePointFromLbl: VisionLabel
    activeFromEntry: VisionEntry
    activePointToLbl: VisionLabel
    activeToEntry: VisionEntry
    btnActiveAdvanceSetting: Button
    threshLbl: VisionLabel
    threshEntry: VisionEntry
    btnVisionSetting: Button

    def __init__(self, master, mainWindow, modelParameter):
        from Modules.ModelSetting.ModelParameter import ModelParameter
        from View.ModelSetting.ModelSettingTab import ModelSettingTab
        VisionFrame.__init__(self, master)
        self.modelSettingTab: ModelSettingTab = master
        self.mainWindow = mainWindow
        self.modelParameter: ModelParameter = modelParameter
        self.setupView()

    def changeModel(self, modelParameter):
        self.modelParameter = modelParameter

        self.refPoint1xEntry.delete(0, END)
        self.refPoint1yEntry.delete(0, END)
        self.refPoint2xEntry.delete(0, END)
        self.refPoint2yEntry.delete(0, END)
        self.refPoint3xEntry.delete(0, END)
        self.refPoint3yEntry.delete(0, END)
        self.offsetPointXEntry.delete(0, END)
        self.offsetPointYEntry.delete(0, END)
        self.offsetXEntry.delete(0, END)
        self.offsetYEntry.delete(0, END)
        self.offsetZEntry.delete(0, END)
        self.conversionCoefficientEntry.delete(0, END)
        self.filePathEntry.delete(0, END)
        self.activeFromEntry.delete(0, END)
        self.activeToEntry.delete(0, END)
        self.threshEntry.delete(0, END)

        self.numOfRefPointCombo.current(self.numOfRefPointList.index(modelParameter.numOfRefPoint))
        self.refPoint1xEntry.insert(0, "{}".format(modelParameter.refPoint1[0]))
        self.refPoint1yEntry.insert(0, "{}".format(modelParameter.refPoint1[1]))
        self.refPoint2xEntry.insert(0, "{}".format(modelParameter.refPoint2[0]))
        self.refPoint2yEntry.insert(0, "{}".format(modelParameter.refPoint2[1]))
        self.refPoint3xEntry.insert(0, "{}".format(modelParameter.refPoint3[0]))
        self.refPoint3yEntry.insert(0, "{}".format(modelParameter.refPoint3[1]))
        self.offsetPointXEntry.insert(0, "{}".format(modelParameter.offsetPoint[0]))
        self.offsetPointYEntry.insert(0, "{}".format(modelParameter.offsetPoint[1]))
        self.offsetXEntry.insert(0, "{}".format(modelParameter.offset[0]))
        self.offsetYEntry.insert(0, "{}".format(modelParameter.offset[1]))
        self.offsetZEntry.insert(0, "{}".format(modelParameter.offset[2]))
        self.conversionCoefficientEntry.insert(0, "{}".format(modelParameter.conversionCoef))
        self.activeFromEntry.insert(0, "{}".format(modelParameter.activeFrom))
        self.activeToEntry.insert(0, "{}".format(modelParameter.activeTo))
        self.threshEntry.insert(0, "{}".format(modelParameter.threshValue))
        self.filePathEntry.insert(0, "{}".format(modelParameter.designFilePath))
        self.filePathEntry.xview(len(modelParameter.designFilePath) - 1)

    def save(self, modelParameter: ModelParameter):
        try:
            modelParameter.refPoint1 = ((float(self.refPoint1xEntry.get())), (float(self.refPoint1yEntry.get())))
            modelParameter.refPoint2 = ((float(self.refPoint2xEntry.get())), (float(self.refPoint2yEntry.get())))
            modelParameter.refPoint3 = ((float(self.refPoint3xEntry.get())), (float(self.refPoint3yEntry.get())))
            modelParameter.offsetPoint = ((float(self.offsetPointXEntry.get())), (float(self.offsetPointYEntry.get())))
            modelParameter.offset = (int(float(self.offsetXEntry.get())), int(float(self.offsetYEntry.get())), int(float(self.offsetZEntry.get())))
            modelParameter.conversionCoef = float(self.conversionCoefficientEntry.get())
            modelParameter.designFilePath = self.filePathEntry.get()
            modelParameter.activeFrom = int(float(self.activeFromEntry.get()))
            modelParameter.activeTo = int(float(self.activeToEntry.get()))
            modelParameter.threshValue = int(float(self.threshEntry.get()))

            if modelParameter.activeTo < modelParameter.activeFrom:
                messagebox.showerror("Save Model", "Activated end point is grater than start point")
                return False

            modelParameter.numOfRefPoint = self.numOfRefPointCombo.get()
            if modelParameter.numOfRefPoint == NumOfRefPoint._2RefPoint.value:
                try:
                    coeff = 10000000000
                    ref1 = (int(coeff*modelParameter.refPoint1[0]), int(coeff*modelParameter.refPoint1[1]))
                    ref2 = (int(coeff*modelParameter.refPoint2[0]), int(coeff*modelParameter.refPoint2[1]))

                    ret, ref3 = ImageProcess.equilateralTriangleFrom2Points(ref1, ref2)
                    if ret:
                        modelParameter.refPoint3 = (ref3[0] / coeff, ref3[1] / coeff)

                        self.refPoint3xEntry.delete(0, END)
                        self.refPoint3yEntry.delete(0, END)

                        self.refPoint3xEntry.insert(0, modelParameter.refPoint3[0])
                        self.refPoint3yEntry.insert(0, modelParameter.refPoint3[1])
                    else:
                        messagebox.showerror("Number Of Reference Points",
                                             "Cannot Calculate the Reference point 3\nPlease check the Ref point 1 and Ref point 2")

                except Exception as error:
                    self.mainWindow.runningTab.insertLog("ERROR Number Of Reference Points : {}".format(error))
                    messagebox.showerror("Number Of Reference Points", "Cannot Calculate the Reference point 3\nPlease check the Ref point 1 and Ref point 2" )


            self.modelList[self.modelManager.currentModelPos] = modelParameter
            self.modelNameList[self.modelManager.currentModelPos] = modelParameter.name
            self.modelComboBox.config(value=self.modelNameList)

            self.rearCheckMissingFrame.save(model=self.currentModelParameter)
        except:
            messagebox.showerror("Save model", "Cannot not save Model")
            return False

    def setupView(self):
        self.screwParameterFrame = VisionLabelFrame(self, text="thiss iss")
        self.screwParameterFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Name entry
        distanceY = 0.07

        for numOfRefPoint in NumOfRefPoint:
            self.numOfRefPointList.append(numOfRefPoint.value)
        self.numOfRefPointCombo = ttk.Combobox(self.screwParameterFrame, state='readonly', value=self.numOfRefPointList, cursor="hand2")
        self.numOfRefPointCombo.place(relx=0.02, rely=distanceY, relwidth=0.22)

        # reference points
        nameLabel = VisionLabel(self.screwParameterFrame, text="X")
        nameLabel.place(relx=0.3, rely=distanceY + 0.02)

        nameLabel = VisionLabel(self.screwParameterFrame, text="Y")
        nameLabel.place(relx=0.6, rely=distanceY + 0.02)

        # reference point 1
        self.ref1Lbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("ref1Lbl"))
        self.ref1Lbl.place(relx=0.02, rely=2 * distanceY)

        self.refPoint1xEntry = VisionEntry(self.screwParameterFrame)
        self.refPoint1xEntry.place(relx=0.22, rely=2 * distanceY, relwidth=0.2, relheight=0.045)

        self.refPoint1yEntry = VisionEntry(self.screwParameterFrame)
        self.refPoint1yEntry.place(relx=0.52, rely=2 * distanceY, relwidth=0.2, relheight=0.045)

        self.btnRef1Select = VisionButton(self.screwParameterFrame,
                                    text=self.mainWindow.languageManager.localized("ref1SelectBtn"),
                                    command=self.clickBtnRef1Select)
        self.btnRef1Select.place(relx=0.83, rely=2 * distanceY, relwidth=0.15, relheight=0.05)

        # reference point 2
        self.ref2Lbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("ref2Lbl"))
        self.ref2Lbl.place(relx=0.02, rely=3 * distanceY)

        self.refPoint2xEntry = VisionEntry(self.screwParameterFrame)
        self.refPoint2xEntry.place(relx=0.22, rely=3 * distanceY, relwidth=0.2, relheight=0.045)

        self.refPoint2yEntry = VisionEntry(self.screwParameterFrame)
        self.refPoint2yEntry.place(relx=0.52, rely=3 * distanceY, relwidth=0.2, relheight=0.045)

        self.btnRef2Select = VisionButton(self.screwParameterFrame,
                                    text=self.mainWindow.languageManager.localized("ref2SelectBtn"),
                                    command=self.clickBtnRef2Select)
        self.btnRef2Select.place(relx=0.83, rely=3 * distanceY, relwidth=0.15, relheight=0.05)

        # reference point 3
        self.ref3Lbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("ref3Lbl"))
        self.ref3Lbl.place(relx=0.02, rely=4 * distanceY)

        self.refPoint3xEntry = VisionEntry(self.screwParameterFrame)
        self.refPoint3xEntry.place(relx=0.22, rely=4 * distanceY, relwidth=0.2, relheight=0.045)

        self.refPoint3yEntry = VisionEntry(self.screwParameterFrame)
        self.refPoint3yEntry.place(relx=0.52, rely=4 * distanceY, relwidth=0.2, relheight=0.045)

        self.btnRef3Select = VisionButton(self.screwParameterFrame,
                                    text=self.mainWindow.languageManager.localized("ref3SelectBtn"),
                                    command=self.clickBtnRef3Select)
        self.btnRef3Select.place(relx=0.83, rely=4 * distanceY, relwidth=0.15, relheight=0.05)

        # offset position
        self.offsetPointLbl = VisionLabel(self.screwParameterFrame,
                                    text=self.mainWindow.languageManager.localized("offsetPointLbl"))
        self.offsetPointLbl.place(relx=0.02, rely=5 * distanceY)

        self.offsetPointXEntry = VisionEntry(self.screwParameterFrame)
        self.offsetPointXEntry.place(relx=0.22, rely=5 * distanceY, relwidth=0.2, relheight=0.045)

        self.offsetPointYEntry = VisionEntry(self.screwParameterFrame)
        self.offsetPointYEntry.place(relx=0.52, rely=5 * distanceY, relwidth=0.2, relheight=0.045)

        self.btnOffsetPointSelect = VisionButton(self.screwParameterFrame,
                                           text=self.mainWindow.languageManager.localized("offsetPointSelectBtn"),
                                           command=self.clickBtnOffsetPointSelect)
        self.btnOffsetPointSelect.place(relx=0.83, rely=5 * distanceY, relwidth=0.15, relheight=0.05)

        # Offset
        self.offsetParmLbl = VisionLabel(self.screwParameterFrame,
                                   text=self.mainWindow.languageManager.localized("offsetParmLbl"))
        self.offsetParmLbl.place(relx=0.02, rely=6 * distanceY)

        self.offsetXEntry = VisionEntry(self.screwParameterFrame)
        self.offsetXEntry.place(relx=0.22, rely=6 * distanceY, relwidth=0.18, relheight=0.045)

        self.offsetYEntry = VisionEntry(self.screwParameterFrame)
        self.offsetYEntry.place(relx=0.46, rely=6 * distanceY, relwidth=0.18, relheight=0.045)

        self.offsetZEntry = VisionEntry(self.screwParameterFrame)
        self.offsetZEntry.place(relx=0.70, rely=6 * distanceY, relwidth=0.18, relheight=0.045)

        self.btnCaliOffset = VisionButton(self.screwParameterFrame,
                                    text=self.mainWindow.languageManager.localized("calibrationOffsetBtn"),
                                    command=self.clickBtnCaliOffset)
        self.btnCaliOffset.place(relx=0.3, rely=7 * distanceY, relwidth=0.3)

        self.btnGetOffset = VisionButton(self.screwParameterFrame,
                                   text=self.mainWindow.languageManager.localized("getOffsetBtn"),
                                   command=self.clickBtnGetOffset)
        self.btnGetOffset.place(relx=0.65, rely=7 * distanceY, relwidth=0.25)
        # conversion coefficient

        self.conversionLbl = VisionLabel(self.screwParameterFrame,
                                   text=self.mainWindow.languageManager.localized("conversionLbl"))
        self.conversionLbl.place(relx=0.02, rely=8 * distanceY)

        self.conversionCoefficientEntry = VisionEntry(self.screwParameterFrame)
        self.conversionCoefficientEntry.place(relx=0.35, rely=8 * distanceY, relwidth=0.25, relheight=0.045)

        self.btnTakeCoefficient = VisionButton(self.screwParameterFrame,
                                         text=self.mainWindow.languageManager.localized("btnTakeCoefficient"),
                                         command=self.clickBtnTakeCoef)
        self.btnTakeCoefficient.place(relx=0.65, rely=7.9 * distanceY, relwidth=0.3)

        # Offset
        self.designPathLbl = VisionLabel(self.screwParameterFrame,
                                   text=self.mainWindow.languageManager.localized("designPathLbl"))
        self.designPathLbl.place(relx=0.02, rely=9 * distanceY)

        self.filePathEntry = VisionEntry(self.screwParameterFrame)
        self.filePathEntry.place(relx=0.3, rely=9 * distanceY, relwidth=0.55, relheight=0.045)

        self.btnSelectDesignFile = VisionButton(self.screwParameterFrame,
                                          text=self.mainWindow.languageManager.localized("designFileSelect"),
                                          command=self.clickBtnSelectFile)
        self.btnSelectDesignFile.place(relx=0.65, rely=9.9 * distanceY, relwidth=0.25)

        # Active positions
        self.activePointFromLbl = VisionLabel(self.screwParameterFrame,
                                        text=self.mainWindow.languageManager.localized("activeFromLbl"))
        self.activePointFromLbl.place(relx=0.02, rely=11 * distanceY)

        self.activeFromEntry = VisionEntry(self.screwParameterFrame)
        self.activeFromEntry.place(relx=0.36, rely=11 * distanceY, relwidth=0.1, relheight=0.045)

        self.activePointToLbl = VisionLabel(self.screwParameterFrame,
                                      text=self.mainWindow.languageManager.localized("activeToLbl"))
        self.activePointToLbl.place(relx=0.51, rely=11 * distanceY)

        self.activeToEntry = VisionEntry(self.screwParameterFrame)
        self.activeToEntry.place(relx=0.61, rely=11 * distanceY, relwidth=0.1, relheight=0.045)

        self.btnActiveAdvanceSetting = VisionButton(self.screwParameterFrame,
                                              text=self.mainWindow.languageManager.localized("advanceActiveBtn"),
                                              command=self.clickBtnActiveAdvance)
        self.btnActiveAdvanceSetting.place(relx=0.74, rely=10.9 * distanceY, relwidth=0.25)

        # Thresh setting
        self.threshLbl = VisionLabel(self.screwParameterFrame, text=self.mainWindow.languageManager.localized("threshLbl"))
        self.threshLbl.place(relx=0.02, rely=12 * distanceY)

        self.threshEntry = VisionEntry(self.screwParameterFrame)
        self.threshEntry.place(relx=0.3, rely=12 * distanceY, relwidth=0.2, relheight=0.045)

        self.btnVisionSetting = VisionButton(self.screwParameterFrame,
                                       text=self.mainWindow.languageManager.localized("visionSettingBtn"),
                                       command=self.clickBtnVisionSetting)
        self.btnVisionSetting.place(relx=0.6, rely=12 * distanceY, relwidth=0.3)


    def clickBtnVisionSetting(self):
        visionSettingWindow = VisionSettingWindow(self.mainWindow, self.modelParameter)
        visionSettingWindow.wait_window()
        if visionSettingWindow.saveFlag:
            self.modelParameter.screwRecognizeAlgorithm = visionSettingWindow.screwRecognizeAlgorithm
            self.modelParameter.ringRecognizeAlgorithm = visionSettingWindow.ringRecognizeAlgorithm


    def clickBtnRef1Select(self):
        if not self.pointExisted():
            return
        from View.ModelSetting.ReferencePositionSelectWindow import ReferencePositionSelectWindow
        referenceWindow1 = ReferencePositionSelectWindow(self.mainWindow)
        referenceWindow1.wait_window()
        if not referenceWindow1.isChosenFlag:
            return
        point = self.mainWindow.workingThread.adjustingScrewPos.originalPositions[referenceWindow1.posChosen]
        self.refPoint1xEntry.delete(0, END)
        self.refPoint1yEntry.delete(0, END)

        self.refPoint1xEntry.insert(0,"{}".format(point[0]))
        self.refPoint1yEntry.insert(0,"{}".format(point[1]))

        self.ref1Pos = referenceWindow1.posChosen

    def clickBtnRef2Select(self):
        if not self.pointExisted():
            return
        from View.ModelSetting.ReferencePositionSelectWindow import ReferencePositionSelectWindow
        referenceWindow2 = ReferencePositionSelectWindow(self.mainWindow)
        referenceWindow2.wait_window()
        if not referenceWindow2.isChosenFlag:
            return
        point = self.mainWindow.workingThread.adjustingScrewPos.originalPositions[referenceWindow2.posChosen]
        self.refPoint2xEntry.delete(0, END)
        self.refPoint2yEntry.delete(0, END)

        self.refPoint2xEntry.insert(0,"{}".format(point[0]))
        self.refPoint2yEntry.insert(0,"{}".format(point[1]))

        self.ref2Pos = referenceWindow2.posChosen

    def clickBtnRef3Select(self):
        if not self.pointExisted():
            return
        from View.ModelSetting.ReferencePositionSelectWindow import ReferencePositionSelectWindow
        referenceWindow3 = ReferencePositionSelectWindow(self.mainWindow)
        referenceWindow3.wait_window()
        if not referenceWindow3.isChosenFlag:
            return
        point = self.mainWindow.workingThread.adjustingScrewPos.originalPositions[referenceWindow3.posChosen]
        self.refPoint3xEntry.delete(0, END)
        self.refPoint3yEntry.delete(0, END)

        self.refPoint3xEntry.insert(0,"{}".format(point[0]))
        self.refPoint3yEntry.insert(0,"{}".format(point[1]))

        self.ref3Pos = referenceWindow3.posChosen

    def clickBtnOffsetPointSelect(self):
        if not self.pointExisted():
            return
        from View.ModelSetting.ReferencePositionSelectWindow import ReferencePositionSelectWindow
        offsetSelectWindow = ReferencePositionSelectWindow(self.mainWindow)
        offsetSelectWindow.wait_window()
        if not offsetSelectWindow.isChosenFlag:
            return
        point = self.mainWindow.workingThread.adjustingScrewPos.originalPositions[offsetSelectWindow.posChosen]
        self.offsetPointXEntry.delete(0, END)
        self.offsetPointYEntry.delete(0, END)

        self.offsetPointXEntry.insert(0,"{}".format(point[0]))
        self.offsetPointYEntry.insert(0,"{}".format(point[1]))

        self.offsetPos = offsetSelectWindow.posChosen


    def pointExisted(self):
        if len(self.mainWindow.workingThread.adjustingScrewPos.originalPositions) <= 0:
            messagebox.showerror(self.mainWindow.languageManager.localized("title_noPointExisted"),
                                 self.mainWindow.languageManager.localized("msg_title_noPointExisted"))
            return False
        else:
            return True


    def clickBtnActiveAdvance(self):
        activeAdvanceSetting = ActivePointAdvanceSettingView(self.mainWindow,
                                                             activeFrom=int(float(self.activeFromEntry.get())),
                                                             activeTo=int(float(self.activeToEntry.get())),
                                                             lastSetting=self.modelParameter.activePointsSetting)
        activeAdvanceSetting.wait_window()
        for state in activeAdvanceSetting.result:
            print(state)

        if activeAdvanceSetting.confirmYes:
            self.modelParameter.activePointsSetting = activeAdvanceSetting.result

    def clickBtnSelectFile(self):
        filePath = tkinter.filedialog.askopenfilename(title="Select design file",
                                                      filetypes=(('Csv file', '*.csv'), ('All files', '*.*')),
                                                      initialdir="/áéá")
        if filePath == "":
            return
        self.filePathEntry.delete(0, END)
        self.filePathEntry.insert(0, filePath)
        self.filePathEntry.xview(END)

        self.modelSettingTab.drawCurrentModelDesign()


    def clickBtnTakeCoef(self):
        return

    def clickBtnGetOffset(self):
        return

    def clickBtnCaliOffset(self):
        return