from ImageProcess.Algorithm.MethodList import MethodList
from ImageProcess.Algorithm.StepParamter import StepParameter
from View.Common.VisionUI import *
from tkinter import messagebox

class StepView(VisionFrame):
    chosenCheckBox: VisionCheckBox
    stepLabel: VisionLabel
    methodComboBox: VisionCheckBox
    optionComboBox: ttk.Combobox
    executeButton: VisionButton
    height = 39
    stepParameter: StepParameter = None
    optionMenu : VisionMenuButton
    chosenVar: BooleanVar


    METHOD_LIST = ['matching template',
                   'cvtcolor',
                   'dilate',
                   'erode',
                   ]
    OPTION_LIST = ["Setting",
                   "Up",
                   "Down"]

    def __init__(self, mainWindow, conceptStep, master):
        from MainWindow import MainWindow
        VisionFrame.__init__(self, master)
        self.mainWindow: MainWindow = mainWindow
        self.stepId =conceptStep
        self.createConcept()
        self.show()
        self.notifyRegister()
    def notifyRegister(self):
        self.mainWindow.notificationCenter.add_observer(with_block=self.changeLanguage, for_name="ChangeLanguage")
    def changeLanguage(self, sender, notification_name, info):
        self.optionMenu.config(text=self.mainWindow.languageManager.localized("option"))

    def createConcept(self):
        self.METHOD_LIST = []
        for method in MethodList:
            self.METHOD_LIST.append(method.value)
        self.METHOD_LIST.sort()
        chosenFrame =VisionFrame(self)
        chosenFrame.place(x=0, y=0, relwidth = 0.1, relheight=1)

        stepFrame =VisionFrame(self)
        stepFrame.place(y=0, relx=0.06, relwidth=0.1, relheight=1)

        methodFrame =VisionFrame(self)
        methodFrame.place(y=0, relx=0.18, relwidth=0.35, relheight=1)

        optionFrame =VisionFrame(self)
        optionFrame.place(y=0, relx=0.53, relwidth=0.28, relheight=1)

        executeFrame =VisionFrame(self)
        executeFrame.place(y=0, relx=0.75, relwidth=0.28, relheight=1)

        self.chosenVar = BooleanVar()
        self.chosenCheckBox = VisionCheckBox(chosenFrame, command=self.checkedChosenBox, variable=self.chosenVar)
        self.chosenCheckBox.deselect()
        self.chosenCheckBox.pack()
        # self.chosenCheckBox.place(relx=0, rely = 0, relwidth =1, relheight =1)

        self.stepLabel = VisionLabel(stepFrame, text=str(self.stepId))
        self.stepLabel.place(x=0, y=0, relwidth=1)

        self.methodComboBox = ttk.Combobox(methodFrame, value = self.METHOD_LIST, state='readonly')
        self.methodComboBox.unbind_class("TCombobox", "<MouseWheel>")
        self.methodComboBox.current(0)
        self.methodComboBox.bind("<<ComboboxSelected>>", self.methodSelected)
        self.methodComboBox.place(x=0, y=0, relwidth=1)

        self.optionMenu = VisionMenuButton(optionFrame, text=self.mainWindow.languageManager.localized("option"), anchor=CENTER)
        self.optionMenu.menu = VisionMenu(self.optionMenu, tearoff=0)
        self.optionMenu["menu"] = self.optionMenu.menu
        self.optionMenu.place(relx=0.2, y = 0, relwidth =0.8, relheight =1)
        self.optionMenu.menu.add_command(label=self.mainWindow.languageManager.localized("setting"), command=self.clickBtnSetting)
        self.optionMenu.menu.add_command(label=self.mainWindow.languageManager.localized("show erea"), command=self.clickBtnShowWorkingArea)
        self.optionMenu.menu.add_command(label=self.mainWindow.languageManager.localized("up"), command=self.clickBtnUp)
        self.optionMenu.menu.add_command(label=self.mainWindow.languageManager.localized("down"), command=self.clickBtnDown)
        self.optionMenu.menu.add_command(label=self.mainWindow.languageManager.localized("duplicate"), command=self.clickBtnDuplicate)
        self.optionMenu.menu.add_command(label=self.mainWindow.languageManager.localized("insert down"), command=self.clickBtnInsertDown)

        self.executeButton = VisionButton(executeFrame, text='Execute', command=self.clickBtnExecute)
        self.executeButton.place(relx = 0.15, y=0, relwidth=0.69)

    def show(self):
        self.place(x=0, y = (self.stepId * self.height), relwidth=1, height=self.height)

    def updateParameter(self, stepParameter):
        self.stepParameter = stepParameter
        self.chosenVar.set(self.stepParameter.activeFlag)
        self.methodComboBox.current(self.METHOD_LIST.index(self.stepParameter.stepAlgorithmName))

    def clickBtnShowWorkingArea(self):
        if self.stepParameter is None:
            messagebox.showwarning("Algorithm Setting", "There is no algorithm created\nPlease add one to setting!")
            return
        self.mainWindow.researchingTab.stepSettingFrame.clickBtnShowWorkingArea(stepParameter=self.stepParameter)

    def clickBtnSetting(self):
        if self.stepParameter is None:
            messagebox.showwarning("Algorithm Setting", "There is no algorithm created\nPlease add one to setting!")
            return
        self.mainWindow.researchingTab.settingForStep(stepParameter=self.stepParameter)
        # conceptSetting = ConceptSetting(self.mainWindow, self.stepParameter)
        # return
    def clickBtnExecute(self):
        if self.stepParameter is None:
            messagebox.showwarning("Algorithm Setting", "There is no algorithm created\nPlease add one to setting!")
            return
        self.mainWindow.researchingTab.currentAlgorithm.executeStep(self.stepId)

    def clickBtnUp(self):
        if self.stepParameter is None:
            messagebox.showwarning("Algorithm Setting", "There is no algorithm created\nPlease add one to setting!")
            return
        self.mainWindow.researchingTab.currentAlgorithm.stepUp(self.stepId)

    def clickBtnDown(self):
        if self.stepParameter is None:
            messagebox.showwarning("Algorithm Setting", "There is no algorithm created\nPlease add one to setting!")
            return
        self.mainWindow.researchingTab.currentAlgorithm.stepDown(self.stepId)

    def clickBtnInsertDown(self):
        if self.stepParameter is None:
            messagebox.showwarning("Algorithm Setting", "There is no algorithm created\nPlease add one to setting!")
            return
        self.mainWindow.researchingTab.currentAlgorithm.insertStepDown(self.stepId)

    def clickBtnDuplicate(self):
        if self.stepParameter is None:
            messagebox.showwarning("Algorithm Setting", "There is no algorithm created\nPlease add one to setting!")
            return
        self.mainWindow.researchingTab.currentAlgorithm.duplicateStep(self.stepId)

    def methodSelected(self, event):
        if self.stepParameter is None:
            messagebox.showwarning("Algorithm Setting", "There is no algorithm created\nPlease add one to setting!")
            return
        self.stepParameter.stepAlgorithmName = self.methodComboBox.get()

    def checkedChosenBox(self, event=None):
        if self.stepParameter is None:
            messagebox.showwarning("Algorithm Setting", "There is no algorithm created\nPlease add one to setting!")
            return
        self.stepParameter.activeFlag = self.chosenVar.get()
        print(self.chosenVar.get())
