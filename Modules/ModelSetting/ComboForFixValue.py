from View.Common.VisionUI import *

class ComboForFixValue(VisionFrame):
    label: VisionLabel
    comboBox: ttk.Combobox
    valueList = []
    xDistance = 150

    def __init__(self, master, lblText, yPos, height, codeList):

        VisionFrame.__init__(self, master)
        self.codeList = codeList
        self.lblText = lblText
        self.yPos = yPos
        self.setupView()
        self.place(x=0, y=yPos, relwidth=1, height=height)

    def setupView(self):
        self.valueList = []
        for name, member in self.codeList.__members__.items():
            self.valueList.append(name)

        label = VisionLabel(self, text=self.lblText)
        label.place(x=5, y=0)
        self.comboBox = ttk.Combobox(self, state="readonly", value=self.valueList, cursor="hand2")
        self.comboBox.place(x=self.xDistance, y=0, width=150, height=20)

    def getValue(self):
        ret = None
        for name, member in self.codeList.__members__.items():
            if name == self.comboBox.get():
                ret = member.value
                break
        return ret

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
        for name, member in self.codeList.__members__.items():
            if member.value == value:
                self.comboBox.current(self.valueList.index(name))
                break

