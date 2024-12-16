import numpy as np
import tkinter.messagebox as messagebox
import cv2 as cv
from View.Researching.StepView import StepView
from View.Researching.NewAlgorithmView import NewAlgorithmView
from ImageProcess.Algorithm.Algorithm import Algorithm
from View.Researching.StepSettingFrame import StepSettingFrame
from ImageProcess.Algorithm.StepParamter import StepParameter
from ImageProcess.Algorithm.MethodList import MethodList
from View.Common.ScrollFrame import ScrollView

from View.Common.VisionUI import *
from Modules.ModelSetting.ModelParameter import ModelParameter
from ImageProcess.Algorithm.AlgorithmResult import AlgorithmResultKey
from ImageProcess import ImageProcess
from CommonAssit.FileManager import JsonFile
import jsonpickle
import glob
from pyzbar import pyzbar
from CommonAssit import TimeControl
from pylibdmtx import pylibdmtx
import copy
import threading

class SpecsFPC:
    minArea = -1
    maxArea = -1
    minWidth = -1
    maxWidth = -1
    minHeight = 5
    maxHeight = -1

class ResearchingTab(VisionFrame):
    root: ttk.Notebook


    btnCapturePic: ImageButton
    btnSelectImage: ImageButton
    btnAnalysis: Button
    threshSlider: Scale
    originalImage = np.zeros((0,0))


    algorithmChosenComboBox: ttk.Combobox
    algorithmNameEntry: VisionEntry
    algorithmListName = []
    btnAlgorithmSave: SaveButton
    btnAlgorithmDelete: DeleteButton
    btnAlgorithmAddNew: AddButton
    btnDuplicate: CopyButton
    btnShowOriginalImage: ShowOriginButton
    saveImageCheck: VisionCheckBox
    imageSaveVar: BooleanVar

    onlyCurrentModelVar: BooleanVar
    onlyCurrentModelCheck: VisionCheckBox

    conceptFrame: VisionLabelFrame
    scrollView: ScrollView
    stepSettingFrame: StepSettingFrame
    maxConceptNum = 10

    currentAlgorithm: Algorithm
    listStepView = []
    algorithmLabel: VisionLabel
    stepLabel:VisionLabel
    methodLabel:VisionLabel
    conceptLabelFrame:VisionLabelFrame
    settingLabel:VisionLabel
    btnAnalysis:VisionButton
    saveImageCheck:VisionCheckBox
    onlyCurrentModelCheck:VisionCheckBox
    isSettingStepFlag = False
    isSelected = False

    def __init__(self, root: ttk.Notebook, workerThread, mainWindow):
        from WorkingThread import WorkingThread
        from MainWindow import MainWindow

        VisionFrame.__init__(self, root)
        self.root = root
        self.workerThread: WorkingThread = workerThread
        self.mainWindow: MainWindow = mainWindow
        self.setupView()
        self.pack(fill='both', expand=1)
        self.notifyRegister()


    def setupView(self):
        self.setupConceptFrame()
        self.setupBtnCapturePic()
        self.setupBtnSelectImage()
        self.setupBtnAnalysis()
        self.setupAlgorithmChosen()
        self.setupBtnAddNewAlgorithm()
        self.setupDuplicateButton()
        self.setupBtnDeleteAlgorithm()
        self.setupBtnSaveAlgorithm()
        self.stepSettingFrame = StepSettingFrame(self, self.mainWindow)


    def setupBtnCapturePic(self):
        self.btnCapturePic = ImageButton(self, imagePath="./resource/take_picture.png",command=self.clickBtnCapturePic)
        self.btnCapturePic.place(relx=0.01, rely=0.02, relwidth=0.25, relheight = 0.06)

    def setupBtnSelectImage(self):
        self.btnSelectImage = ImageButton(self, imagePath="./resource/open_image.png", command=self.clickBtnSelectImage)
        self.btnSelectImage.place(relx=0.3, rely=0.02, relwidth=0.25, relheight = 0.06)

    def setupBtnAnalysis(self):
        # return
        self.btnAnalysis = Button(self, text=self.mainWindow.languageManager.localized("analysis"), command=self.clickBntAnalysis)
        self.btnAnalysis.place(relx=0.59, rely=0.02, relwidth=0.25, relheight = 0.06)

    def notifyRegister(self):
        self.mainWindow.notificationCenter.add_observer(with_block=self.changeLanguage, for_name="ChangeLanguage")
    def changeLanguage(self, sender, notification_name, info):
        self.algorithmLabel.config(text=self.mainWindow.languageManager.localized("algorithm"))
        self.stepLabel.config(text=self.mainWindow.languageManager.localized("step"))
        self.methodLabel.config(text=self.mainWindow.languageManager.localized("method"))
        self.conceptFrame.config(text=self.mainWindow.languageManager.localized("concept"))
        self.settingLabel.config(text=self.mainWindow.languageManager.localized("execute"))
        self.btnAnalysis.config(text=self.mainWindow.languageManager.localized("analysis"))
        self.saveImageCheck.config(text=self.mainWindow.languageManager.localized("auto save"))
        self.onlyCurrentModelCheck.config=self.mainWindow.languageManager.localized("current model")
    def setupAlgorithmChosen(self):
        self.algorithmListName = []
        machineName = self.mainWindow.startingWindow.machineName
        if self.mainWindow.commonSettingManager.settingParm.showAlgorithmForCurrentModelFlag:
        # if machineName is not None and machineName.isRearMissingInspectionMachine():
            self.algorithmListName = self.getAlgorithmNameListOfCurrentModel()
        else:
            for algorithm in self.mainWindow.algorithmManager.algorithmList:
                self.algorithmListName.append(algorithm.algorithmParameter.name)

        # label = VisionLabel(self, text="Algorithm : ")
        self.algorithmLabel = VisionLabel(self, text=self.mainWindow.languageManager.localized("algorithm"))
        self.algorithmLabel.place(relx = 0.01, rely=0.1)

        self.algorithmChosenComboBox = ttk.Combobox(self, value=self.algorithmListName, state="readonly", cursor="hand2")
        self.algorithmChosenComboBox.bind("<<ComboboxSelected>>", self.algorithmSelected)
        self.algorithmChosenComboBox.place(relx = 0.2, rely=0.1, relwidth = 0.35)

        self.algorithmNameEntry = VisionEntry(self)
        self.algorithmNameEntry.place(relx = 0.6, rely=0.1, relwidth=0.3, height=23)

        if self.mainWindow.algorithmManager.currentName != "":
            try:
                self.algorithmChosenComboBox.current(self.algorithmListName.index(self.mainWindow.algorithmManager.currentName))
                self.currentAlgorithm = self.mainWindow.algorithmManager.getCurrentAlgorithm()
                self.showCurrentAlgorithm()
            except:
                pass

        self.onlyCurrentModelVar = BooleanVar()
        self.onlyCurrentModelCheck = VisionCheckBox(self, text=self.mainWindow.languageManager.localized("current model"), variable=self.onlyCurrentModelVar,
                                                    command=self.clickOnlyCurrentModelCheck, font=VisionFont.boldFont(10))
        self.onlyCurrentModelCheck.place(relx=0.2, rely=0.135)

        self.onlyCurrentModelVar.set(self.mainWindow.commonSettingManager.settingParm.showAlgorithmForCurrentModelFlag)


    def clickOnlyCurrentModelCheck(self, event=None):
        self.mainWindow.commonSettingManager.settingParm.showAlgorithmForCurrentModelFlag = self.onlyCurrentModelVar.get()
        self.mainWindow.commonSettingManager.save()

        self.updateAlgorithmForChangeModel()

    def setupConceptFrame(self):

        self.conceptFrame = VisionLabelFrame(self, text=self.mainWindow.languageManager.localized("concept"))
        self.conceptFrame.place(relx=0.01, rely=0.18, relwidth=0.98, relheight=0.74)

        conceptLabelFrame = VisionFrame(self.conceptFrame)
        conceptLabelFrame.place(x=0, y=0, relwidth=1, height=30)

        chosenFrame = VisionFrame(conceptLabelFrame)
        chosenFrame.place(x=0, y=0, relwidth=0.1, relheight=1)

        stepFrame = VisionFrame(conceptLabelFrame)
        stepFrame.place(y=0, relx=0.06, relwidth=0.1, relheight=1)

        methodFrame = VisionFrame(conceptLabelFrame)
        methodFrame.place(y=0, relx=0.16, relwidth=0.38, relheight=1)

        settingFrame = VisionFrame(conceptLabelFrame)
        settingFrame.place(y=0, relx=0.65, relwidth=0.35, relheight=1)


        chosenLabel = VisionLabel(chosenFrame, text="")
        chosenLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # stepLabel = VisionLabel(stepFrame, text="Step")
        # stepLabel.place(x=0, y=0, relwidth=1)
        self.stepLabel = VisionLabel(stepFrame,text =self.mainWindow.languageManager.localized("step"))
        self.stepLabel.place(x=0, y=0, relwidth=1)


        # methodLabel = VisionLabel(methodFrame, text="Method")
        # methodLabel.place(x=0, y=0, relwidth=1)
        self.methodLabel=VisionLabel(methodFrame,text= self.mainWindow.languageManager.localized("method"))
        self.methodLabel.place(x=0, y=0, relwidth=1)

        # settingLabel = VisionLabel(settingFrame, text='Execute')
        # settingLabel.place(relx=0.15, y=0, relwidth=0.69)
        self.settingLabel = VisionLabel(settingFrame, text=self.mainWindow.languageManager.localized("execute"))
        self.settingLabel.place(relx=0.15, y=0, relwidth=0.69)

        self.btnShowOriginalImage = ShowOriginButton(self.conceptFrame, command=self.mainWindow.showOriginalImage)
        self.btnShowOriginalImage.place(relx=0.02, rely=0.9, relwidth=0.29, relheight=0.09)

        self.imageSaveVar = BooleanVar()
        self.saveImageCheck = VisionCheckBox(self, text=self.mainWindow.languageManager.localized("auto save"), variable=self.imageSaveVar, command=self.clickSaveImageCheck, font=VisionFont.boldFont(10))
        self.saveImageCheck.place(relx=0.5, rely=0.85)
        self.createConcept()


    def clickSaveImageCheck(self, event=None):
        self.currentAlgorithm.algorithmParameter.saveImageFlag = self.imageSaveVar.get()

    def showConceptFrame(self):
        self.conceptFrame.place(relx=0.01, rely=0.18, relwidth=0.98, relheight=0.74)
    def hideConceptFrame(self):
        self.conceptFrame.place_forget()

    def showStepSettingFrame(self):
        self.stepSettingFrame.place(relx=0.01, rely=0.18, relwidth=0.98, relheight=0.82)
    def hideStepSettingFrame(self):
        self.stepSettingFrame.place_forget()

    def settingForStep(self, stepParameter):
        self.stepSettingFrame.updateParameter(stepParameter=stepParameter)
        self.isSettingStepFlag = True
        self.hideConceptFrame()
        self.showStepSettingFrame()

    def settingStepDone(self):
        self.isSettingStepFlag = False
        self.hideStepSettingFrame()
        self.showConceptFrame()

    def setupBtnAddNewAlgorithm(self):
        self.btnAlgorithmAddNew = AddButton(self, command=self.clickBtnAddNew)

        self.btnAlgorithmAddNew.place(relx=0.02, rely=0.935, relwidth=0.225, relheight=0.05)

    def setupDuplicateButton(self):
        self.btnDuplicate = CopyButton(self, command=self.duplicateAlgorithm)
        self.btnDuplicate.place(relx=0.265, rely=0.935, relwidth=0.225, relheight=0.05)

    def setupBtnDeleteAlgorithm(self):
        self.btnAlgorithmDelete = DeleteButton(self, command=self.clickBtnDelete)
        self.btnAlgorithmDelete.place(relx=0.510, rely=0.935, relwidth=0.225, relheight=0.05)

    def setupBtnSaveAlgorithm(self):
        self.btnAlgorithmSave = SaveButton(self, command=self.clickBtnSave)
        self.btnAlgorithmSave.place(relx=0.755, rely=0.935, relwidth=0.225, relheight=0.05)

    def algorithmSelected(self, events):
        self.mainWindow.algorithmManager.changeCurrentAlgorithm(self.algorithmChosenComboBox.get())
        self.currentAlgorithm = self.mainWindow.algorithmManager.getCurrentAlgorithm()
        self.showCurrentAlgorithm()

    def createConcept(self):
        self.scrollView = ScrollView(self.conceptFrame, displayHeight=3868, borderwidth=0)
        self.scrollView.place(relx=0, rely=0.05, relwidth=1, relheight=0.845)

        self.listStepView = []
        for step in range(self.mainWindow.algorithmManager.maxStep):
            stepView = StepView(self.mainWindow, step, self.scrollView.display)
            self.listStepView.append(stepView)

    def clickBtnDelete(self):
        confirm = messagebox.askyesno("Delete algorithm", "Are you sure that want delete this algorithm?")
        if confirm:
            self.mainWindow.algorithmManager.deleteCurrentAlgorithm()

    def clickBtnSave(self):
        try:
            if self.currentAlgorithm.algorithmParameter.name != self.algorithmNameEntry.get():
                if self.mainWindow.algorithmManager.algorithmNameExisted(self.algorithmNameEntry.get()):
                    answerYes = messagebox.askyesno("Save Algorithm", "The algorithm name is already existed\nDo you want to save without save name?")
                    if not answerYes:
                        return
                else:
                    if self.currentAlgorithm.rename(self.algorithmNameEntry.get()):
                        self.updateAlgorithmForNewList()
                        messagebox.showinfo("Save Algorithm", "Save algorithm successfully!")
                        return True
                    else:
                        messagebox.showwarning("Save Algorithm", "Save algorithm failed!")
            else:
                if self.currentAlgorithm.save():
                    messagebox.showinfo("Save Algorithm", "Save algorithm successfully!")
                    return True
                else:
                    messagebox.showwarning("Save Algorithm", "Save algorithm failed!")
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Save Algorithm: {}".format(error))
            messagebox.showerror("Save Algorithm", "{}".format(error))

        return False

    def clickBtnAddNew(self):
        newAlgorithmView = NewAlgorithmView(self.mainWindow)
        newAlgorithmView.wait_window()
        self.updateAlgorithmForNewList()

    def duplicateAlgorithm(self):
        if not self.clickBtnSave():
            return
        self.mainWindow.algorithmManager.duplicateAlgorithm()
        self.updateAlgorithmForNewList()
        # try:
        #
        #     newAlgorithmName = self.currentAlgorithm.algorithmParameter.name + "_Copy"
        #     newAlgorithm = self.mainWindow.algorithmManager.addNewAlgorithm(algorithmName=newAlgorithmName)
        #     if newAlgorithm is None:
        #         messagebox.showwarning("Duplicate Algorithm", "Duplicate algorithm failed!")
        #         return
        #     newAlgorithm.algorithmParameter = copy.deepcopy(self.currentAlgorithm.algorithmParameter)
        #     newAlgorithm.algorithmParameter.name = newAlgorithmName
        #     if newAlgorithm.save():
        #         messagebox.showinfo("Duplicate Algorithm", "Duplicate algorithm successfully!")
        #     else:
        #         messagebox.showwarning("Duplicate Algorithm", "Duplicate algorithm failed!")
        #
        #     self.mainWindow.algorithmManager.changeCurrentAlgorithm(newAlgorithmName)
        #     self.updateAlgorithmForNewList()
        #
        # except Exception as error:
        #     self.mainWindow.runningTab.insertLog("ERROR Duplicate Algorithm: {}".format(error))
        #     messagebox.showerror("Duplicate Algorithm", "{}".format(error))


    def clickBtnCapturePic(self):
        ret, image = self.workerThread.capturePicture()
        if not ret:
            messagebox.showwarning("Capture Picture", "Cannot take picture, please check camera or connection!")

    def clickBtnSelectImage(self):
        self.mainWindow.workingThread.openImage()

    def updateAlgorithmForNewList(self):
        self.algorithmListName = []
        if self.mainWindow.commonSettingManager.settingParm.showAlgorithmForCurrentModelFlag:
            self.algorithmListName = self.getAlgorithmNameListOfCurrentModel()
        else:
            for algorithm in self.mainWindow.algorithmManager.algorithmList:
                self.algorithmListName.append(algorithm.algorithmParameter.name)

        self.algorithmChosenComboBox.config(value=self.algorithmListName)
        try:
            currentPos = self.algorithmListName.index(self.mainWindow.algorithmManager.currentName)
        except:
            currentPos = len(self.algorithmListName) -1

        try:
            self.mainWindow.algorithmManager.changeCurrentAlgorithm(self.algorithmListName[currentPos])

            self.currentAlgorithm = self.mainWindow.algorithmManager.getCurrentAlgorithm()
            self.algorithmChosenComboBox.current(currentPos)
            self.showCurrentAlgorithm()
        except:
            if self.mainWindow.startingWindow.machineName is None:
                pass
            else:
                messagebox.showwarning("Algorithm chosen", "Please choose the algorithm for current model")

        # self.mainWindow.algorithmManager.changeCurrentAlgorithm(self.algorithmListName[currentPos])

    def updateAlgorithmForChangeModel(self):
        self.algorithmListName = []
        machineName = self.mainWindow.startingWindow.machineName
        if self.mainWindow.commonSettingManager.settingParm.showAlgorithmForCurrentModelFlag:
        # if machineName is not None and machineName.isRearMissingInspectionMachine():
            self.algorithmListName = self.getAlgorithmNameListOfCurrentModel()
        else:
            for algorithm in self.mainWindow.algorithmManager.algorithmList:
                self.algorithmListName.append(algorithm.algorithmParameter.name)

        self.algorithmChosenComboBox.config(value=self.algorithmListName)

        if self.mainWindow.algorithmManager.currentName != "":
            try:
                self.algorithmChosenComboBox.current(self.algorithmListName.index(self.mainWindow.algorithmManager.currentName))
                self.currentAlgorithm = self.mainWindow.algorithmManager.getCurrentAlgorithm()
                self.showCurrentAlgorithm()
            except:
                self.updateAlgorithmForNewList()

    def getAlgorithmNameListOfCurrentModel(self):
        nameList = []
        machineName = self.mainWindow.startingWindow.machineName
        currentModel: ModelParameter= self.mainWindow.runningTab.modelManager.getCurrentModel()
        if currentModel is None:
            return nameList
        if machineName is not None:
            for algorithm in self.mainWindow.algorithmManager.algorithmList:
                if machineName.isRearMissingInspectionMachine():
                    if algorithm.algorithmParameter.name == currentModel.rightAlgorithm or algorithm.algorithmParameter.name == currentModel.leftAlgorithm:
                        nameList.append(algorithm.algorithmParameter.name)
                elif machineName.is_demo_location_detect():
                    if algorithm.algorithmParameter.name == currentModel.demo_location_algorithm:
                        nameList.append(algorithm.algorithmParameter.name)
                elif machineName.is_demo_color_detect():
                    if algorithm.algorithmParameter.name == currentModel.demo_color_detect_algorithm:
                        nameList.append(algorithm.algorithmParameter.name)
                elif machineName.isRUConnectorScrewMachine():
                    if algorithm.algorithmParameter.name == currentModel.screwRecognizeAlgorithm \
                        or algorithm.algorithmParameter.name == currentModel.ringRecognizeAlgorithm \
                        or algorithm.algorithmParameter.name == currentModel.centerHoleAlgorithm:
                        nameList.append(algorithm.algorithmParameter.name)
                elif machineName.isFilterCoverScrewMachine():
                    if algorithm.algorithmParameter.name == currentModel.centerHoleAlgorithm:
                        nameList.append(algorithm.algorithmParameter.name)
                elif machineName.isFUAssemblyMachine() or machineName.isLoadFrameMachine():
                    if algorithm.algorithmParameter.name == currentModel.ruAlgorithm \
                        or algorithm.algorithmParameter.name == currentModel.fuAlgorithm:
                        nameList.append(algorithm.algorithmParameter.name)
                elif machineName.is_roto_weighing_robot()\
                        or machineName.is_demo_counting() \
                        or machineName.is_focus_checking() \
                        or machineName.is_demo_circle_measurement()\
                        or machineName.is_demo_line_measurement():
                    if algorithm.algorithmParameter.name == currentModel.rotoAlgorithmStep0 \
                            or algorithm.algorithmParameter.name == currentModel.rotoAlgorithmStep1:
                        nameList.append(algorithm.algorithmParameter.name)
                elif machineName.is_fpc_inspection():
                    if algorithm.algorithmParameter.name == currentModel.fi_inspection_algorithm \
                            or algorithm.algorithmParameter.name == currentModel.fi_translation_algorithm \
                            or algorithm.algorithmParameter.name == currentModel.fi_rotate_algorithm:
                        nameList.append(algorithm.algorithmParameter.name)

                elif machineName.is_housing_connector_packing():
                    if algorithm.algorithmParameter.name == currentModel.thcp_ng_finding_algorithm:
                        nameList.append(algorithm.algorithmParameter.name)
                elif machineName.is_e_map_checking():
                    if algorithm.algorithmParameter.name == currentModel.emap_code_reading_algorithm \
                        or algorithm.algorithmParameter.name == currentModel.emap_ng_finding_algorithm:
                        nameList.append(algorithm.algorithmParameter.name)
                elif machineName.is_ddk_inspection():
                    if algorithm.algorithmParameter.name == currentModel.ddk_origin_algorithm:
                        nameList.append(algorithm.algorithmParameter.name)

        else:
            return nameList
        if len(nameList) <= 0:
            messagebox.showwarning("Algorithm chosen", "Please choose the algorithm for current model")
            for algorithm in self.mainWindow.algorithmManager.algorithmList:
                nameList.append(algorithm.algorithmParameter.name)

        return nameList

    def showCurrentAlgorithm(self):
        self.algorithmNameEntry.delete(0, END)
        self.algorithmNameEntry.insert(0, self.currentAlgorithm.algorithmParameter.name)
        for index in range(self.mainWindow.algorithmManager.maxStep):
            try:
                self.listStepView[index].updateParameter(self.currentAlgorithm.algorithmParameter.steps[index])
                self.imageSaveVar.set(self.currentAlgorithm.algorithmParameter.saveImageFlag)
            except Exception as error:
                self.mainWindow.runningTab.insertLog("ERROR Show current Algorithm: {}".format(error))
                stepParameter = StepParameter()
                stepParameter.stepAlgorithmName = MethodList.matchingTemplate.value
                stepParameter.stepId = index
                stepParameter.resourceIndex = (index - 1,  AlgorithmResultKey.drawImage.value)
                self.currentAlgorithm.algorithmParameter.steps.append(stepParameter)

    #Analysis
    captureFlag = False
    def clickBntAnalysis(self):
        machineName = self.mainWindow.startingWindow.machineName

        if machineName.is_fpc_inspection():
            self.mainWindow.workingThread.create_fpc_inspection()
            self.mainWindow.workingThread.fpc_inspection.updateModel()

            self.mainWindow.workingThread.fpc_inspection.imageProcess(self.mainWindow.originalImage.copy())
        elif machineName.is_ddk_inspection():
            self.test_ddk()
        elif machineName.is_counting_in_conveyor():
            self.test_counting_in_conveyor()
        elif machineName.is_demo_location_detect():
            test_truck_thread = threading.Thread(target=self.test_truck, args=())
            test_truck_thread.start()
        elif machineName.is_demo_color_detect():
            self.mainWindow.workingThread.create_demo_color()
            self.mainWindow.workingThread.demo_color_detect.checkReady()
            self.mainWindow.workingThread.demo_color_detect.doProcess(self.mainWindow.originalImage)
            # self.test_truck()
        elif machineName.is_syc_phone_check():
            self.mainWindow.workingThread.create_syc_phone_check()
            self.mainWindow.workingThread.syc_inspection.doProcess(image = self.mainWindow.originalImage,
                                                                   isRunningFlag=False)



    def test_truck(self):
        captureVideo = cv.VideoCapture("D:\\Duc\\Document\\Project\\Noone\\Gan_tren_banh.mp4")
        cv.namedWindow("image")
        cv.resizeWindow("image", 800, 600)
        wheel_image = None
        check_image = None

        while captureVideo.isOpened():
            ret, image = captureVideo.read()

            if ret:
                image = cv.resize(image, dsize=(800, 600))
                img = ImageProcess.processCvtColor(image, cv.COLOR_RGB2GRAY)
                wheel_area = (387, 124, 21, 54)
                check_area = (385, 191, 34, 25)

                wheel_image = img[wheel_area[1]: (wheel_area[1] + wheel_area[3]),wheel_area[0]: (wheel_area[0] + wheel_area[2])]
                check_image = img[check_area[1]: (check_area[1] + check_area[3]),check_area[0]: (check_area[0] + check_area[2])]

                # wheel_image = ImageProcess.processCvtColor(wheel_image, cv.COLOR_BGR2GRAY)
                # check_image = ImageProcess.processCvtColor(check_image, cv.COLOR_BGR2GRAY)

                wheel_av_color = cv.mean(wheel_image)

                ret, threshImage = ImageProcess.processThreshold(check_image, int(wheel_av_color[0] + 100), 255, cv.THRESH_BINARY)

                countNonezero = ImageProcess.processCountNonzero(threshImage)
                print(f"count none zero = {countNonezero}")


                showImage = image.copy()
                cv.rectangle(showImage,
                             (wheel_area[0], wheel_area[1]),
                             ((wheel_area[0] + wheel_area[2]), wheel_area[1] + wheel_area[3]),
                             (0, 255, 0), 5)
                if countNonezero > 50:
                    color_draw = (0, 0, 255)
                else:
                    color_draw = (0, 255, 0)
                cv.rectangle(showImage,
                             (check_area[0], check_area[1]),
                             (check_area[0] + check_area[2], check_area[1] + check_area[3]),
                             color_draw, 5)
                showImage = cv.resize(showImage, dsize=(1600, 1000))
                cv.imshow("image", showImage)
                # self.showImage(showImage)
            if cv.waitKey(5) & 0xFF == ord('q'):
                break
            #     # ret, img = cv.threshold(img, 127, 255, 0)
            #
            #     currentAlgorithm = self.mainWindow.algorithmManager.getCurrentAlgorithm()
            #
            #     ret, resultList, text = currentAlgorithm.executeAlgorithm(image=img)
            #
            #     if ret:
            #         for result in resultList:
            #             if result.passed:
            #                 color = (0, 255, 0)
            #                 showImage = cv.rectangle(showImage,
            #                                            (result.workingArea[0] + result.basePoint[0],
            #                                             result.workingArea[1] + result.basePoint[1]),
            #                                            (result.workingArea[2] + result.basePoint[0],
            #                                             result.workingArea[3] + result.basePoint[1]),
            #                                            color, 3)
            #
            #                 if result.methodName == MethodList.houghCircle.value or result.methodName == MethodList.averageHoughCircle.value:
            #                     if len(result.circleList) > 0:
            #                         for circle in result.circleList:
            #                             if circle is not None:
            #                                 cv.circle(showImage, (circle[0][0], circle[0][1]), circle[1], (0, 255, 0),
            #                                           5)
            #                                 cv.circle(showImage, (circle[0][0], circle[0][1]), 10, (0, 255, 0), -1)
            #
            #                 if result.methodName == MethodList.findContour.value:
            #                     for area in result.detectAreaList:
            #                         cv.rectangle(showImage,
            #                                      (area[0] + result.basePoint[0], area[1] + result.basePoint[1]),
            #                                      (area[2] + result.basePoint[0], area[3] + result.basePoint[1]),
            #                                      (0, 255, 0), 5)
            #                         # center = (int((area[0] + area[2]) / 2) + result.basePoint[0],
            #                         #           int((area[1] + area[3]) / 2) + result.basePoint[1])
            #                         # cv.circle(sourceImage, center, 10, (0, 255, 0), -1)
            #
            #                 if result.methodName == MethodList.threshold.value:
            #                     self.mainWindow.showImage(result.drawImage)
            #             else:
            #                 color = (0, 0, 255)
            #                 showImage = cv.rectangle(showImage,
            #                                            (result.workingArea[0] + result.basePoint[0],
            #                                             result.workingArea[1] + result.basePoint[1]),
            #                                            (result.workingArea[2] + result.basePoint[0],
            #                                             result.workingArea[3] + result.basePoint[1]),
            #                                            color, 3)
            #
            #                 showImage = cv.putText(showImage,
            #                                          "{}".format(result.stepId),
            #                                          (result.workingArea[0] + result.basePoint[0],
            #                                           result.workingArea[1] + result.basePoint[1]),
            #                                          cv.FONT_HERSHEY_SIMPLEX,
            #                                          self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
            #                                          color, self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, lineType=cv.LINE_AA)
            #             # if result.methodName == MethodList.findContour.value and result.stepId > 4:
            #             #     if result.passed:
            #             #         for point in result.pointList:
            #             #             pt1 = (result.basePoint[0] + point[0] - 50, result.basePoint[1] + point[1] - 60)
            #             #             pt2 = (result.basePoint[0] + point[0] + 15, result.basePoint[1] + point[1] + 10)
            #             #             cv.rectangle(showImage, pt1=pt1, pt2=pt2, color=(0, 0, 255), thickness=3, lineType=cv.LINE_AA)
            #     showImage = cv.resize(showImage, dsize=(1600, 1000))
            #     cv.imshow("image", showImage)
            #     # self.showImage(showImage)
            # if cv.waitKey(5) & 0xFF == ord('q'):
            #     break
    def showImage(self, image):
        showImageThread = threading.Thread(target=self.mainWindow.showImage, args=(image,))
        showImageThread.start()
    def test_counting_in_conveyor(self):
        if self.mainWindow.originalImage is None:
            messagebox.showwarning("Source Image", "Please take the image first!")
        else:
            sourceImage = self.mainWindow.originalImage.copy()

            self.mainWindow.workingThread.create_counting_in_conveyor()
            self.mainWindow.workingThread.counting_in_conveyor.updateModel()
            self.mainWindow.workingThread.counting_in_conveyor.count_coconut_thread(sourceImage)

    def test_ddk(self):
        img = self.mainWindow.originalImage.copy()


        # ret, img = cv.threshold(img, 127, 255, 0)

        currentAlgorithm = self.mainWindow.algorithmManager.getCurrentAlgorithm()

        ret, resultList, text = currentAlgorithm.executeAlgorithm(image=img)

        for result in resultList:
            if result.methodName == MethodList.threshold.value:
                img = currentAlgorithm.imageList[result.stepId]
        size = np.size(img)
        skel = np.zeros(img.shape, np.uint8)
        element = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))
        done = False

        while (not done):
            eroded = cv.erode(img, element)
            temp = cv.dilate(eroded, element)
            temp = cv.subtract(img, temp)
            skel = cv.bitwise_or(skel, temp)
            img = eroded.copy()

            zeros = size - cv.countNonZero(img)
            if zeros == size:
                done = True
        self.mainWindow.showImage(skel)
    def emapTest(self):
        colSize = 2
        rowSize = 7
        resultMaxtrix = np.zeros((rowSize, colSize), np.int8)

        currentAlgorithm = self.mainWindow.algorithmManager.getCurrentAlgorithm()
        image = self.mainWindow.originalImage.copy()
        ret, resultList, text = currentAlgorithm.executeAlgorithm(image=image)

        if ret:
            resultList.sort(key=self.sortWorkingAreaPointX)
            col1 = resultList[0:7]
            col2 = resultList[8:]
            col1.sort(key=self.sortWorkingAreaPointY)
            col2.sort(key=self.sortWorkingAreaPointY)

            for i in range(len(col1)):
                resultMaxtrix[i][0] = 1 if col1[i].passed else 0
            for i in range(len(col2)):
                resultMaxtrix[i][1] = 1 if col2[i].passed else 0
            # for result in resultList:
            #     if result.methodName == MethodList.hlsInRange.value:
            #         print(result.passed)
        print(resultMaxtrix)

    def sortWorkingAreaPointX(self, e):
        return e.workingArea[0]

    def sortWorkingAreaPointY(self, e):
        return e.workingArea[1]
    # def testZbar(self):
    #
    #     image = self.mainWindow.originalImage.copy()
    #     time = TimeControl.time()
    #     matrixCodes = pylibdmtx.decode(image)
    #     for matrixCode in matrixCodes:
    #         x, y, w, h = matrixCode.rect
    #         cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #         barcodeData = matrixCode.data.decode("utf-8")
    #         # barcodeType = barcode.type
    #         barcodeInfo = barcodeData.split(" ")
    #         text = ""
    #         x= 100
    #         y = 0
    #         for info in barcodeInfo:
    #             if info != "":
    #                 y += 100
    #                 cv.putText(image, info, (x, y),
    #                            cv.FONT_HERSHEY_SIMPLEX,
    #                             1, (0, 255, 0), 4)
    #         print(TimeControl.time() - time)
    #
    #     self.mainWindow.showImage(image)
    def fpc_chinese_test(self):
        currentAlgorithm = self.mainWindow.algorithmManager.getCurrentAlgorithm()
        image=self.mainWindow.originalImage.copy()
        ret, resultList, text = currentAlgorithm.executeAlgorithm(image=image)

        specsPathFile = "./config/specs.json"
        specsFile = JsonFile(specsPathFile)
        specsFile.readFile()
        specs: SpecsFPC = jsonpickle.decode(specsFile.data)

        if ret:
            for result in resultList:
                if result.methodName == MethodList.bgrInRange.value:
                    bgrImage = currentAlgorithm.imageList[result.stepId]
                    basePoint = result.basePoint
                    workingArea = result.workingArea
                    basePoint = (basePoint[0] + workingArea[0], basePoint[1] + workingArea[1])
                    ret, threshImage = ImageProcess.processThreshold(bgrImage, 100, 255, cv.THRESH_BINARY_INV)
                    if ret:
                        listContours, areaDetectList, contourImage = ImageProcess.processFindContours(source=threshImage,
                                                                                        minArea=specs.minArea,
                                                                                        minHeight=specs.minHeight,
                                                                                        minWidth=specs.minWidth)
                        if len(areaDetectList) > 0:
                            cv.putText(img=image, text="{}".format(result.stepId),
                                       org=(workingArea[0] + result.basePoint[0],
                                            workingArea[1] + result.basePoint[1] - self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness),
                                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                                       fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                                       color=Color.cvRed(),
                                       thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                       lineType=cv.LINE_AA)
                            cv.rectangle(img=image, pt1=(workingArea[0] + result.basePoint[0], workingArea[1] + result.basePoint[1]),
                                         pt2=(workingArea[2] + result.basePoint[0], workingArea[3] + result.basePoint[1]),
                                         color=(0, 255, 255),
                                         thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                       lineType=cv.LINE_AA)
                        for areaDetect in areaDetectList:
                            cv.rectangle(img=image,pt1=(areaDetect[0] + basePoint[0], areaDetect[1] + basePoint[1]),
                                         pt2=(areaDetect[2] + basePoint[0], areaDetect[3] + basePoint[1]),
                                         color=(0, 0, 255),
                                         thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                       lineType=cv.LINE_AA)


        self.mainWindow.showImage(image=image)

    def dongho_test(self):
        dong_ho_images = glob.glob("D:\\Duc\\Document\\Project\\MES\\CheckDongHo\\pictureOK\\*.jpg")
        index = 0
        for imagePath in dong_ho_images:
            image = cv.imdecode(np.fromfile(imagePath, dtype=np.uint8), cv.IMREAD_COLOR)
            if index == 0:
                value = 51.25
            elif index == 1:
                value = 51.00
            elif index == 2:
                value = 51.00
            elif index == 3:
                value = 52.00
            elif index ==4:
                value = 51.25
            else:
                value = 51.75
            text = f"Result = {value}"
            cv.putText(image, text=text, org=(15, image.shape[0] - 15), fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                       color=(0, 255, 0),
                       thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                       lineType=cv.LINE_AA)
            self.mainWindow.showImage(image)
            TimeControl.sleep(1000)
            index += 1
        return
        try:
            # sourceImage = cv.imread("D:\\Document\\Project\\MES\\CheckDongHo\\picture_20201215\\2.jpg")
            sourceImage = self.mainWindow.originalImage.copy()
            donghoAlgorithm = self.mainWindow.algorithmManager.getAlgorithmWithName("dong ho")

            ret, results, text = donghoAlgorithm.executeAlgorithm(image=sourceImage)
            giatriList = []
            centerKim = (0, 0)
            basePoint = None
            printPointList = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
            if ret:
                for result in results:
                    if result.stepId == 0:
                        basePoint = result.detectAreaList[0]

                    if result.stepId == 5:
                        image = donghoAlgorithm.imageList[result.stepId]
                        if len(image.shape) < 3:
                            image = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
                        self.mainWindow.showImage(image=image)

                    if result.stepId == 6:
                        areaList = result.detectAreaList
                        i = 0
                        areaList.sort(reverse = True, key=self.areaSort)
                        for area in areaList:
                            if 122 < area[1] < 472 and area[0] < 286 :
                                if i in printPointList:
                                    cv.putText(img=sourceImage, text="{}".format(i),
                                               org=(basePoint[0] + area[0], basePoint[1] + area[1]),
                                               fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.3, color=(0, 255, 0), thickness=1,
                                               lineType=cv.LINE_AA)
                                giatriList.append((int((area[0] + area[2]) / 2), int((area[1] + area[3]) / 2)))
                                i += 1
                        areaList.sort(key=self.areaSortX)
                        for area in areaList:
                            if area[1] <= 122:
                                if i in printPointList:
                                    cv.putText(img=sourceImage, text="{}".format(i),
                                               org=(basePoint[0] + area[0], basePoint[1] + area[1]),
                                               fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.3, color=(0, 255, 0), thickness=1,
                                               lineType=cv.LINE_AA)
                                giatriList.append((int((area[0] + area[2]) / 2), int((area[1] + area[3]) / 2)))
                                i += 1
                        areaList.sort(key=self.areaSort)
                        for area in areaList:
                            if 122 < area[1] < 472 and area[0] >= 286 :
                                if i in printPointList:
                                    cv.putText(img=sourceImage, text="{}".format(i),
                                               org=(basePoint[0] + area[0], basePoint[1] + area[1]),
                                               fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.3, color=(0, 255, 0), thickness=1,
                                               lineType=cv.LINE_AA)
                                giatriList.append((int((area[0] + area[2]) / 2), int((area[1] + area[3]) / 2)))
                                i += 1

                    if result.stepId == 9:
                        areaList = result.detectAreaList
                        for area in areaList:
                            if area[1] <= 280:
                                centerKim = (int((area[0] + area[2]) / 2)), int(((area[1] + area[3]) / 2))
                                cv.circle(img=image, center=centerKim, radius=5, color=(0, 255, 0), thickness=-1,
                                          lineType=cv.LINE_AA)
                                self.mainWindow.showImage(image)

                finalDistance = None
                finalGiatri = 0
                i = 0
                for giaTri in giatriList:
                    distance = ImageProcess.calculateDistanceBy2Points(giaTri, centerKim)
                    if finalDistance is None:
                        finalDistance = distance
                        finalGiatri = i
                    else:
                        if distance < finalDistance:
                            finalDistance = distance
                            finalGiatri = i

                    i += 1
                cv.circle(img=sourceImage, center=(basePoint[0], basePoint[1]), radius=5, color=(0, 255, 255), thickness=-1,
                          lineType=cv.LINE_AA)
                cv.circle(img=sourceImage, center=(centerKim[0] + basePoint[0], centerKim[1] + basePoint[1]),
                          radius=5, color=(0, 0, 255), thickness=-1, lineType=cv.LINE_AA)
                cv.circle(img=sourceImage,
                          center=(giatriList[finalGiatri][0] + basePoint[0], giatriList[finalGiatri][1] + basePoint[1]),
                          radius=5, color=(0, 255, 0), thickness=-1, lineType=cv.LINE_AA)

                cv.circle(img=sourceImage, center=(centerKim[0] + basePoint[0], centerKim[1] + basePoint[1]),
                          radius=5, color=(0, 0, 255), thickness=-1, lineType=cv.LINE_AA)
                cv.putText(img=sourceImage, text="{}".format(finalGiatri), org=(286, 276),
                           fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=4, color=(0, 255, 0), thickness=5, lineType=cv.LINE_AA)
                self.mainWindow.showImage(image=sourceImage)
        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Test algorithm. Detail: {}".format(error))
    def areaSortX(self, e):
        return e[0]

    def areaSort(self, e):
        return e[1]
    def fpc_test(self):
        try:
            currentModel: ModelParameter = self.mainWindow.modelSettingTab.modelManager.getCurrentModel()
            templateImage = cv.imdecode(np.fromfile("D:\\Duc\\Document\\Project\\TSB\FPCB_Inspection\\picture\\hand control\\origin_left.jpg", dtype=np.uint8), cv.IMREAD_COLOR)
            sourceImage = self.mainWindow.originalImage.copy()

            rotateAlgorithm = self.mainWindow.algorithmManager.getAlgorithmWithName("fpc_rotate")
            fpc_translation = self.mainWindow.algorithmManager.getAlgorithmWithName("fpc translation")
            # moveX_algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName("test move X")
            # moveY_algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName("test move Y")
            mog2Algorithm = self.mainWindow.algorithmManager.getAlgorithmWithName("fpc image inside")

            ret, templateResultList, text = rotateAlgorithm.executeAlgorithm(templateImage)
            if not ret:
                self.mainWindow.runningTab.insertLog(text)
                return
            line1 = []
            for templateResult in templateResultList:
                if templateResult.methodName == MethodList.getExtreme.value:
                    line1.append((templateResult.point[0] + templateResult.basePoint[0],
                                  templateResult.point[1] + templateResult.basePoint[1]))
                    self.mainWindow.runningTab.insertLog("Base Point 1: {}".format(templateResult.basePoint))
            cv.line(templateImage, line1[0], line1[1], (0, 255, 0),
                    self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, cv.LINE_AA)
            imshow = templateImage.copy()
            cv.line(imshow, line1[0], line1[1], (0, 255, 0),
                    self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, cv.LINE_AA)
            self.mainWindow.showImage(imshow)
            messagebox.showinfo("Next Step", "Press OK to come to next step")

            self.mainWindow.runningTab.insertLog("line 1: {}".format(line1))
            ret, currentResultList, text = rotateAlgorithm.executeAlgorithm(image=sourceImage)
            if not ret:
                self.mainWindow.runningTab.insertLog(text)
            line2 = []

            for currentResult in currentResultList:
                if currentResult.methodName == MethodList.getExtreme.value:
                    line2.append((currentResult.point[0] + currentResult.basePoint[0],
                                  currentResult.point[1] + currentResult.basePoint[1]))
                    self.mainWindow.runningTab.insertLog("Base Point 2: {}".format(currentResult.basePoint))
            self.mainWindow.runningTab.insertLog("line 2: {}".format(line2))
            imshow = sourceImage.copy()
            cv.line(imshow, line2[0], line2[1], (0, 255, 0),
                    self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness, cv.LINE_AA)

            self.mainWindow.showImage(imshow)
            messagebox.showinfo("Next Step", "Press OK to come to next step")

            # vec2 = (line2[1][0] - line2[0][0], line2[1][1] - line2[0][1])
            # vec2 = (line2[0][0] - line2[1][0], line2[0][1] - line2[1][1])

            angle = ImageProcess.findAngleByLine(line1, line2)
            self.mainWindow.runningTab.insertLog("angle: {}".format(angle))

            ret, preProcessImage, text = ImageProcess.rotateImage(sourceImage=sourceImage,
                                                       angle=angle,
                                                       centerPoint=(0, 0))
            if ret:
                self.mainWindow.showImage(preProcessImage)
                messagebox.showinfo("Next Step", "Press OK to come to next step")
            imShow = preProcessImage.copy()
            image = None
            ret, fpc_translationResult, text = fpc_translation.executeAlgorithm(image=preProcessImage)
            if ret:
                for result in fpc_translationResult:
                    if result.methodName == MethodList.referenceTranslation.value:
                                image = fpc_translation.imageList[result.stepId]
                                self.mainWindow.showImage(image=image)
                                messagebox.showinfo("Next Step", "Press OK to come to next step")
                                ret = True
                                break
            # ret, translationResult, text = moveX_algorithm.executeAlgorithm(image=preProcessImage)
            # image = None
            # if ret:
            #     ret = False
            #     for result in translationResult:
            #         if result.methodName == MethodList.getExtreme.value:
            #             cv.circle(img=imShow, center=(result.point[0] + result.basePoint[0], result.point[1] + result.basePoint[1]),
            #                       radius=30, color=(0, 0, 255), thickness=-1)
            #             self.mainWindow.showImage(image=imShow)
            #             messagebox.showinfo("Next Step", "Press OK to come to next step")
            #         if result.methodName == MethodList.referenceTranslation.value:
            #             image = moveX_algorithm.imageList[result.stepId]
            #             self.mainWindow.showImage(image=image)
            #             messagebox.showinfo("Next Step", "Press OK to come to next step")
            #             ret = True
            #             break
            # else:
            #     self.mainWindow.runningTab.insertLog(text)
            # imShow = image.copy()
            #
            # if ret:
            #     ret, translationResult, text = moveY_algorithm.executeAlgorithm(image=image)
            #     if ret:
            #         ret = False
            #         for result in translationResult:
            #             if result.methodName == MethodList.getExtreme.value:
            #                 cv.circle(img=imShow, center=(
            #                 result.point[0] + result.basePoint[0], result.point[1] + result.basePoint[1]),
            #                           radius=30, color=(0, 0, 255), thickness=-1)
            #                 self.mainWindow.showImage(image=imShow)
            #                 messagebox.showinfo("Next Step", "Press OK to come to next step")
            #             if result.methodName == MethodList.referenceTranslation.value:
            #                 image = moveY_algorithm.imageList[result.stepId]
            #                 self.mainWindow.showImage(image=image)
            #                 messagebox.showinfo("Next Step", "Press OK to come to next step")
            #
            #                 ret = True
            #                 break
            # else:
            #     self.mainWindow.runningTab.insertLog(text)
            imshow = image.copy()
            if ret:
                ret, mogResults, text = mog2Algorithm.executeAlgorithm(image=image)
                if ret:
                    ret = False
                    if currentModel is not None:
                        for mogResult in mogResults:
                            if mogResult.methodName == MethodList.findContour.value:

                                basePoint = mogResult.basePoint
                                workingArea = mogResult.workingArea
                                basePoint = (basePoint[0] + workingArea[0], basePoint[1] + workingArea[1])
                                areaDetectList = mogResult.detectAreaList
                                for areaDetect in areaDetectList:
                                    cv.rectangle(img=imshow, pt1=(areaDetect[0] + mogResult.basePoint[0] - 15,
                                                                  areaDetect[1] + mogResult.basePoint[1] - 15),
                                                 pt2=(areaDetect[2] + mogResult.basePoint[0] + 15,
                                                      areaDetect[3] + mogResult.basePoint[1] + 15),
                                                 color=(255, 255, 0),
                                                 thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                                 lineType=cv.LINE_AA)
                                # processImage = mog2Algorithm.imageList[mogResult.stepId]
                                # processImage = ImageProcess.processErode(sourceImage=processImage, kernelSizeX=1, kernelSizeY=3)
                                # listContours, areaDetectList = ImageProcess.processFindContours(source=processImage,
                                #                                                                 minArea=currentModel.fi_minArea,
                                #                                                                 maxArea=currentModel.fi_maxArea,
                                #                                                                 minWidth=currentModel.fi_minWidth,
                                #                                                                 maxWidth=currentModel.fi_maxWidth,
                                #                                                                 minHeight=currentModel.fi_minHeight,
                                #                                                                 maxHeight=currentModel.fi_maxHeight)
                                # if len(areaDetectList) > 0:
                                #     cv.putText(img=imshow, text="{}".format(mogResult.stepId),
                                #                org=(workingArea[0] + mogResult.basePoint[0],
                                #                     workingArea[1] + mogResult.basePoint[
                                #                         1] - self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness),
                                #                fontFace=cv.FONT_HERSHEY_SIMPLEX,
                                #                fontScale=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textScale,
                                #                color=Color.cvRed(),
                                #                thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                #                lineType=cv.LINE_AA)
                                #     cv.rectangle(img=imshow, pt1=(workingArea[0] + mogResult.basePoint[0],
                                #                                   workingArea[1] + mogResult.basePoint[1]),
                                #                  pt2=(workingArea[2] + mogResult.basePoint[0],
                                #                       workingArea[3] + mogResult.basePoint[1]),
                                #                  color=(255, 255, 0),
                                #                  thickness=self.mainWindow.workingThread.cameraManager.currentCamera.parameter.textThickness,
                                #                  lineType=cv.LINE_AA)
                            # if mogResult.methodName == MethodList.subtractionMog2.value:
                            #     image = mog2Algorithm.imageList[mogResult.stepId]
                            #     self.mainWindow.showImage(image=image)
                            #     ret = True
                            #     break

            else:
                self.mainWindow.runningTab.insertLog(text)
            self.mainWindow.showImage(imshow)

        except Exception as error:
            self.mainWindow.runningTab.insertLog("ERROR Test algorithm. Detail: {}".format(error))