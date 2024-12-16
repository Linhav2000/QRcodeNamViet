from View.Common.VisionUI import *
from tkinter import messagebox

class AdjustValueFrame(VisionFrame):
    value = 100
    btnUP: UpButton
    btnDown: DownButton
    valueEntry: VisionEntry
    minValue = 0
    maxValue = 255
    advancedCommand = None

    def __init__(self, master, minVal = 0, maxVal = 255, advancedCmd=None):
        VisionFrame.__init__(self, master=master)
        self.minValue = minVal
        self.maxValue = maxVal
        self.advancedCommand = advancedCmd
        self.setupView()

    def setupView(self):
        self.valueEntry = VisionEntry(self)
        self.valueEntry.place(relx =0.05, rely=0.05, relwidth=0.525, relheight=0.9)
        self.setValue(self.value)

        self.btnUP = UpButton(self, command=self.clickBtnUp)
        self.btnUP.place(relx =0.625, rely=0.05, relwidth=0.325, relheight=0.425)

        self.btnDown = DownButton(self, command=self.clickBtnDown)
        self.btnDown.place(relx =0.625, rely=0.525, relwidth=0.325, relheight=0.425)

    def clickBtnUp(self):
        currentValue = self.getValue()
        if currentValue == -1:
            return
        currentValue += 1
        self.setValue(currentValue)
        if self.advancedCommand is not None:
            self.advancedCommand()


    def clickBtnDown(self):
        currentValue = self.getValue()
        if currentValue == -1:
            return
        currentValue -= 1
        self.setValue(currentValue)
        if self.advancedCommand is not None:
            self.advancedCommand()

    def setValue(self, value):
        try:
            # if int(value) > self.maxValue or int(value) < self.minValue:
            #     messagebox.showwarning("Invalid range value", "Value cannot less than 0 or greater than 255")
            #     return
            self.valueEntry.delete(0, END)
            self.valueEntry.insert(0, value)
        except Exception as error:
            print("{}".format(error))

    def getValue(self):
        try:
            currentValue = int(float(self.valueEntry.get()))
            if currentValue > self.maxValue or currentValue < self.minValue:
                messagebox.showwarning("Invalid range value", "Value cannot less than 0 or greater than 255")
                return -1
            return currentValue
        except Exception as error:
            print("{}".format(error))
            return -1
