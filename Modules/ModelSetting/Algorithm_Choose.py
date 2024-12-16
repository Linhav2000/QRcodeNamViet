from Modules.ModelSetting.ComboForFlexibleValue import *
from View.Researching.NewAlgorithmView import NewAlgorithmView
from tkinter import messagebox

class Algorithm_Choose(ComboForFlexibleValue):
    add_new_done_cmd = None
    model_name = ""
    def __init__(self,  master, lblText, yPos, height, valueList, xDistance=100, selectChangeCommand=None,
                 combo_width=200, mainWindow=None, add_new_done_cmd=None):
        ComboForFlexibleValue.__init__(self,  master, lblText, yPos, height, valueList,
                                       xDistance=xDistance, combo_width=combo_width, selectChangeCommand=None)
        if mainWindow is None:
            try:
                self.mainWindow = self.master.mainWindow
            except:
                self.mainWindow = None
        else:
            self.mainWindow = mainWindow
        self.add_new_done_cmd = add_new_done_cmd
        self.setupButtonView()

    def setupButtonView(self):
        add_new_btn = VisionButton(self, text="Add new", command=self.add_new_algorithm)
        add_new_btn.place(x=self.xDistance + self.combo_width + 20, rely=0, width=80, height=23)

        go_btn = VisionButton(self, text="GO", command=self.go_to_researching)
        go_btn.place(x=self.xDistance + self.combo_width + 20 + 80 + 20, rely=0, width=60, height=23)

    def add_new_algorithm(self):
        if self.mainWindow is None:
            return
        try:
            defaultName = f"{self.model_name} - {self.lblText}"
        except:
            defaultName = self.lblText
        newAlgorithmView = NewAlgorithmView(self.mainWindow, default_name=defaultName)
        newAlgorithmView.wait_window()
        if self.add_new_done_cmd is not None:
            self.add_new_done_cmd()
        self.setStringValue(newAlgorithmView.save_name)
        self.mainWindow.researchingTab.updateAlgorithmForNewList()

    def go_to_researching(self):
        if self.mainWindow is None:
            return
        current_algorithm = self.getValue()
        if current_algorithm != "":
            self.mainWindow.tabBar.select(1)
            self.mainWindow.algorithmManager.changeCurrentAlgorithm(current_algorithm)
            self.mainWindow.researchingTab.updateAlgorithmForChangeModel()
        else:
            messagebox.showerror("Algorithm choosing", "Please choose the algorithm first!")
