from View.Common.VisionUI import *
from tkinter import filedialog

class Select_Path_File(VisionFrame):
    label: VisionLabel
    parameterEntry: VisionEntry
    btn_select_file: VisionButton
    xDistance = 150

    def __init__(self, master, lblText, yPos, height, width=250):
        VisionFrame.__init__(self, master)
        self.lblText = lblText
        self.yPos = yPos
        self.width = width
        self.setupView()
        self.place(x=0, y=yPos, relwidth=1, height=height)

    def setupView(self):
        self.label = VisionLabel(self, text=self.lblText)
        self.label.place(x=5, y=0)

        self.parameterEntry = VisionEntry(self)
        self.parameterEntry.place(x=self.xDistance, y=0, width= self.width, height=20)

        self.btn_select_file = VisionButton(self, text="Select", command=self.click_btn_select)
        self.btn_select_file.place(x=self.xDistance + self.width + 10, width=100)

    def click_btn_select(self):
        path = filedialog.askopenfilename(title='Select Image',
                                          filetypes=(('All files', '*.*'),),
                                          initialdir="/Ã¡Ã©Ã¡")

        if path != "":
            self.parameterEntry.setValue(path)

    def update_Language(self, new_text):
        self.label.config(text=new_text)

    def getValue(self):
        return self.parameterEntry.get()
    #
    # def getIntValue(self):
    #     try:
    #         return int(float(self.parameterEntry.get()))
    #     except:
    #         return 0
    #
    # def getFloatValue(self):
    #     try:
    #         return float(self.parameterEntry.get())
    #     except:
    #         return 0.0

    def setValue(self, value):
        self.parameterEntry.delete(0, END)
        self.parameterEntry.insert(0, "{}".format(value))
        self.parameterEntry.xview("end")