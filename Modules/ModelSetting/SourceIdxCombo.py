from View.Common.VisionUI import *
from Modules.ModelSetting.ComboForFlexibleValue import ComboForFlexibleValue

class SourceIdxCombo(ComboForFlexibleValue):
    show_button: VisionButton
    showSourceImage = None
    def __init__(self, master, lblText, yPos, height, valueList,sourceImageName=None, command=None):
        ComboForFlexibleValue.__init__(self, master, lblText, yPos, height, valueList)
        self.showSourceImage = command
        self.sourceImageName = sourceImageName
        self.setupSourceIdxComboView()

    def setupSourceIdxComboView(self):
        self.show_button = VisionButton(self, text="Show", font=VisionFont.stepSettingFont(), command=self.clickBtnShow)
        self.show_button.place(x=2*self.xDistance + 10, y=0, width=100, height=25)

    def clickBtnShow(self):
        if self.showSourceImage is None:
            return
        else:
            self.showSourceImage(self.getPosValue() - 4, self.sourceImageName)

# class ComboForFixValue(VisionFrame):
#     label: VisionLabel
#     comboBox: ttk.Combobox
#     valueList = []
#     xDistance = 150
#
#     def __init__(self, master, lblText, yPos, height, codeList):
#
#         VisionFrame.__init__(self, master)
#         self.codeList = codeList
#         self.lblText = lblText
#         self.yPos = yPos
#         self.setupView()
#         self.place(x=0, y=yPos, relwidth=1, height=height)
#
#     def setupView(self):
#         self.valueList = []
#         for name, member in self.codeList.__members__.items():
#             self.valueList.append(name)
#
#         label = VisionLabel(self, text=self.lblText)
#         label.place(x=5, y=0)
#         self.comboBox = ttk.Combobox(self, state="readonly", value=self.valueList)
#         self.comboBox.place(x=self.xDistance, y=0, width=150, height=20)
#
#     def getValue(self):
#         ret = None
#         for name, member in self.codeList.__members__.items():
#             if name == self.comboBox.get():
#                 ret = member.value
#                 break
#         return ret
#
#     def getPosValue(self):
#         try:
#             return self.comboBox.current()
#         except:
#             return 0
#
#     def setPosValue(self, value):
#         try:
#             self.comboBox.current(value)
#         except:
#             pass
#
#     def setStringValue(self, value):
#         for name, member in self.codeList.__members__.items():
#             if member.value == value:
#                 self.comboBox.current(self.valueList.index(name))
#                 break

