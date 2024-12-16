import copy
from View.Common.VisionUI import *

class ComboForFlexibleValue(VisionFrame):
    label: VisionLabel
    comboBox: ttk.Combobox
    valueList = []
    xDistance = 200
    selectChangeCommand = None
    cmb_label: VisionLabel

    def __init__(self, master, lblText, yPos, height, valueList, xDistance=200,
                 combo_width=200, selectChangeCommand=None):
        VisionFrame.__init__(self, master)
        self.lblText = lblText
        self.yPos = yPos
        self.xDistance = xDistance
        self.combo_width = combo_width
        self.valueList = valueList
        self.selectChangeCommand = selectChangeCommand
        self.setupView()
        self.place(x=0, y=yPos, relwidth=1, height=height)


    def setupView(self):
        self.cmb_label = VisionLabel(self, text=self.lblText) # Thằng này nó báo là không có- vì thừa chữ l kia kìa
        self.cmb_label.place(x=5, y=0)
        self.comboBox = ttk.Combobox(self, state="readonly", value=self.valueList, cursor="hand2")
        self.comboBox.bind("<<ComboboxSelected>>", self.selectChanged)
        self.comboBox.place(x=self.xDistance, y=0, width=self.combo_width, height=20)

    def updateLabelLanguage(self, new_lang_label):
        self.cmb_label.config(text=new_lang_label)



    def selectChanged(self, events):
        if self.selectChangeCommand is not None:
            self.selectChangeCommand(self.getPosValue())

    def getValue(self):
        return self.comboBox.get()

    def getPosValue(self):
        try:
            return self.comboBox.current()
        except:
            return 0

    def setPosValue(self, value):
        try:
            self.comboBox.current(value)
        except:
            pass

    def setStringValue(self, value):
        try:
            self.comboBox.current(self.valueList.index(value))
        except:
            self.comboBox.set("")
            pass

    def updateValueList(self, valueList):
        self.valueList = copy.deepcopy(valueList)
        self.comboBox.config(value = self.valueList)

        self.setStringValue(self.comboBox.get())